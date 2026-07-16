import streamlit as st
import pandas as pd
from calculos import cargar_datos_muestra

def marcar_dato_manual():
    """Si el usuario tipea un número, bajamos la bandera de datos de muestra"""
    st.session_state.is_sample_data = False

def toggle_units(columnas_base):
    # Cambiar el sistema
    st.session_state.unit_system = 'imperial' if st.session_state.unit_system == 'metrico' else 'metrico'
    
    # Si los datos actuales eran de muestra, los reseteamos a cero al cambiar unidad
    if st.session_state.is_sample_data:
        st.session_state.temp_amb = 0.0
        st.session_state.p_bar = 0.0
        st.session_state.df_corridas = pd.DataFrame([[0.0]*len(columnas_base) for _ in range(st.session_state.num_corridas)], columns=columnas_base)
        st.session_state.is_sample_data = False # Apagamos la bandera tras borrar

@st.dialog("Confirmar reemplazo")
def confirmar_carga_muestra(columnas_base):
    st.warning("Ya tenés datos cargados manualmente en la tabla, ¿querés borrarlos y cargar los datos de muestra?")
    c1, c2 = st.columns(2)
    if c1.button("Sí, cargar muestra.", use_container_width=True):
        cargar_datos_muestra(columnas_base)
        st.session_state.num_corridas = 5
        st.rerun()  # Recarga la app aplicando los cambios
    if c2.button("Cancelar.", use_container_width=True):
        st.rerun()  # Cierra la ventana sin hacer nada