import streamlit as st
import pandas as pd
from calculos import realizar_calculos, cargar_datos_muestra
from pdf_reporte import generar_pdf
from textos import teoria
from herramientas import marcar_dato_manual, toggle_units, confirmar_carga_muestra
# Soluciona los problemas de caché con los archivos auxiliares
import importlib
import textos
import pdf_reporte
importlib.reload(textos)
importlib.reload(pdf_reporte)

st.set_page_config(page_title="Calibración EPA Método 5 Patrón húmedo", layout="wide")


if 'unit_system' not in st.session_state:
    st.session_state.unit_system = 'metrico'
    st.session_state.is_sample_data = False

if 'num_corridas' not in st.session_state:
    st.session_state.num_corridas = 5

# Variables con las que trabajamos
columnas_base = [
    'delta_h', 'vol_húm', 'vol_m', 't_húm', 't_entrada', 't_salida', 't_prom',
    'theta', 'Y', 'delta_h_arroba'
]

col_titulo, col_advertencia, col_unidades, col_muestra, col_teoria = st.columns([2, 2, 1, 1, 1])

with col_titulo:
    st.title("Calibración de consola")

with col_advertencia:
    # Advertencia si está en sistema imperial y definiciones
    if st.session_state.unit_system == 'imperial':
        st.error("ADVERTENCIA: está configurado el Sistema Imperial de unidades.")
        u_vol, u_temp, u_pres, u_h2o, cau, Q_ref, t_ref, p_ref = "ft³", "°F", "in. Hg", "in. H₂O", "dcfm", "0.75", "68", "29.92"
    else:
        u_vol, u_temp, u_pres, u_h2o, cau, Q_ref, t_ref, p_ref = "m³", "°C", "mm Hg", "mm H₂O", "dscm", "0.02124", "20", "760"

with col_unidades:
    st.write("")
    # Botón para cambiar unidades
    if st.session_state.unit_system == 'metrico':
        st.button("Cambiar al sistema imperial", on_click=toggle_units, args=(columnas_base,), use_container_width=True)
    else:
        st.button("Cambiar al sistema internacional", on_click=toggle_units, args=(columnas_base,), use_container_width=True)

with col_muestra:
    st.write("")
    if st.button("Cargar datos de muestra", use_container_width=True):
        # Verifica si hay datos manuales (distintos de cero)
        hay_datos_manuales = False
        hay_datos_manuales = (
            'df_corridas' in st.session_state
            and not st.session_state.is_sample_data
            and (st.session_state.df_corridas >0).any().any()
        )
        if hay_datos_manuales:
            confirmar_carga_muestra(columnas_base) # Abre el Pop-out
        else:
            cargar_datos_muestra(columnas_base) # Carga directo
            st.rerun()

with col_teoria:
    st.write("") # Espacio para alinear el botón
    # Este botón llama a la función de la ventana emergente
    if st.button("Ver teoría", use_container_width=True):
        teoria()

# Condiciones iniciales
st.write(f"Método 5 utilizando patrón húmedo con condiciones de referencia de caudal {Q_ref} {cau}, presión {p_ref} {u_pres} y temperatura {t_ref} {u_temp}.")
col_subt, col_amb1, col_amb2, col_amb3, col_amb4 = st.columns([2, 1, 1, 1, 1])

with col_subt:
    st.markdown("")
    st.markdown("### Condiciones iniciales y corridas")
with col_amb1:
    temp_amb = st.number_input(f"Temperatura ambiente [{u_temp}]", format="%.2f", step=0.1, key="temp_amb", on_change=marcar_dato_manual)
with col_amb2:
    humedad = st.number_input("Humedad [%]", value=0.0, format="%.1f", step=1.0)
with col_amb3:
    p_bar = st.number_input(f"Presión barométrica ($P_{{bar}}$) [{u_pres}]", format="%.2f", step=1.0, key="p_bar", on_change=marcar_dato_manual)
with col_amb4:
    num_corridas = st.number_input("Cantidad de corridas:", min_value=3, value=5, key="num_corridas", step=1)

# Creamos la tabla
if 'df_corridas' not in st.session_state:
    st.session_state.df_corridas = pd.DataFrame([[0.0]*len(columnas_base) for _ in range(num_corridas)], columns=columnas_base)

# Redimensionamiento dinámico
filas_actuales = len(st.session_state.df_corridas)
if num_corridas > filas_actuales:
    # Si incrementaste el número, añade filas vacías al final conservando las de arriba
    filas_nuevas = pd.DataFrame([[0.0]*len(columnas_base) for _ in range(num_corridas - filas_actuales)], columns=columnas_base)
    st.session_state.df_corridas = pd.concat([st.session_state.df_corridas, filas_nuevas], ignore_index=True)
elif num_corridas < filas_actuales:
    # Si disminuiste el número, recorta desde el final manteniendo los datos superiores
    st.session_state.df_corridas = st.session_state.df_corridas.iloc[:num_corridas]

# Forzamos el índice visual de la tabla
st.session_state.df_corridas.index = range(1, num_corridas + 1)

# Configuramos la visualización de la tabla para que tenga las unidades y formato correcto
config_columnas = {
    "delta_h": st.column_config.NumberColumn(f"ΔH  [{u_h2o}]", format="%.2f"),
    "vol_húm": st.column_config.NumberColumn(f"Volumen patrón húmedo [{u_vol}]", format="%.4f"),
    "vol_m": st.column_config.NumberColumn(f"Volumen medidor [{u_vol}]", format="%.4f"),
    "t_húm": st.column_config.NumberColumn(f"Temperatura patrón húmedo [{u_temp}]", format="%.2f"),
    "t_entrada": st.column_config.NumberColumn(f"Temperatura entrada [{u_temp}]", format="%.1f"),
    "t_salida": st.column_config.NumberColumn(f"Temperatura salida [{u_temp}]", format="%.1f"),
    "t_prom": st.column_config.NumberColumn(f"Temperatura promedio [{u_temp}]", format="%.1f"),
    "theta": st.column_config.NumberColumn("Tiempo  [min]", format="%.2f"),
    "Y": st.column_config.NumberColumn(f"Y", format="%.4f"),
    "delta_h_arroba": st.column_config.NumberColumn(f"ΔH@ {u_h2o}]", format="%.4f")    
}

# Si el ususario cargó datos debemos guardarlos
if "editor_corridas" in st.session_state:
    ediciones = st.session_state["editor_corridas"].get("edited_rows", {})
    for row_idx, cambios in ediciones.items():
        for col_name, nuevo_valor in cambios.items():
            col_idx = st.session_state.df_corridas.columns.get_loc(col_name)
            st.session_state.df_corridas.iat[row_idx, col_idx] = nuevo_valor

Y_factor, delta_h_arroba = realizar_calculos(
    st.session_state.df_corridas, p_bar, st.session_state.unit_system
)

# st.data_editor es la tabla interactiva de Streamlit
tabla_excel = st.data_editor(
    st.session_state.df_corridas,
    column_config=config_columnas,
    num_rows="fixed",
    disabled=['t_prom', 'Y', 'delta_h_arroba'],
    use_container_width=True,
    hide_index=False,
    key="editor_corridas",
    on_change=marcar_dato_manual
)

# Guardamos los datos
st.session_state.df_corridas = tabla_excel

# Resultados
st.markdown("---")
col_final, col_res1, col_res2, _, col_exp = st.columns([1, 1, 1, 2, 1])

with col_final: 
    st.markdown("### Resultados")

with col_res1: 
    st.metric("Factor de calibración ($Y$)", f"{Y_factor:.4f}")

with col_res2:
    st.metric("Delta H@ ($\Delta H_@$)", f"{delta_h_arroba:.4f} {u_h2o}")

# Exportación
with col_exp:
    pdf_bytes = generar_pdf(tabla_excel, p_bar, Y_factor, delta_h_arroba, st.session_state.unit_system, temp_amb)

    st.download_button(
    label="Imprimir un PDF con toda la información",
    data=pdf_bytes,
    file_name="Reporte_Metodo5.pdf",
    mime="application/pdf"
    )