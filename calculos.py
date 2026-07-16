# calculos.py
import streamlit as st
import pandas as pd
import numpy as np

def realizar_calculos(df, p_bar, unit_system):
    """Realiza los cálculos matemáticos procesando la tabla (DataFrame) completa con las nuevas columnas."""
    
    if unit_system == 'metrico':
        temp_add = 273.15
        k = 0.0011695
    else:
        temp_add = 460.0
        k= 0.0319

    total_Y, total_delta_h_arroba = 0.0, 0.0
    corridas_validas = 0

    # Iteramos fila por fila manteniendo tu estructura de bucle original
    for index, row in df.iterrows():
        delta_h = row['delta_h']
        vol_hum = row['vol_húm']
        vol_m = row['vol_m']
        t_hum = row['t_húm']
        t_entrada = row['t_entrada']
        t_salida = row['t_salida']
        theta = row['theta']

        # Evitamos divisiones por cero o filas vacías (control de celdas inicializadas en 0)
        if p_bar <= 0 or vol_hum <= 0 or vol_m <= 0 or t_hum <= 0:
            continue
        
        # Temperaturas promedio y absolutas
        t_prom = (t_entrada + t_salida) / 2 #= 21.5
        t_prom_abs = t_prom + temp_add #= 294.65
        t_hum_abs = t_hum + temp_add #= 294.15
        
        # Factor Y y Delta H@ de la corrida individual
        Y_numerador = vol_hum * p_bar * t_prom_abs #= 30678.958
        Y_denominador = vol_m * (p_bar + delta_h / 13.6) * t_hum_abs #= 30649.477040515
        Y_factor = Y_numerador / Y_denominador #= 1,000961875
        dHa_1 = k * delta_h / (p_bar * t_prom_abs) #= 0.00000004
        dHa_2 = (t_hum_abs * theta / vol_hum) ** 2 #= 1037239600.53812137
        delta_h_arroba = dHa_1 * dHa_2 #= 41.489584022

        # Guardamos los resultados calculados de vuelta en las celdas del DataFrame original
        df.at[index, 't_prom'] = round(t_prom, 3)
        df.at[index, 'Y'] = round(Y_factor, 4)
        df.at[index, 'delta_h_arroba'] = round(delta_h_arroba, 3)

        # Acumulamos los valores para calcular los promedios globales
        total_Y += Y_factor
        total_delta_h_arroba += delta_h_arroba
        corridas_validas += 1

    if corridas_validas > 0:
        return (
            total_Y / corridas_validas,
            total_delta_h_arroba / corridas_validas
        )
    else:
        return 0.0, 0.0

def cargar_datos_muestra(columnas):
    # Avisamos que se usó el botón automático
    st.session_state.is_sample_data = True  
    st.session_state.num_corridas = 5

    if st.session_state.unit_system == 'metrico':
        st.session_state.p_bar = 760.0
        st.session_state.temp_amb = 20.0
        datos_muestra = [
            [7.62, 0.137, 0.137, 21.0, 21.0, 22.0, 0.0, 15.0, 0.0, 0.0],
            [7.62, 0.137, 0.135, 21.0, 21.0, 22.0, 0.0, 15.0, 0.0, 0.0],
            [16.8, 0.195, 0.195, 21.0, 21.0, 22.0, 0.0, 15.0, 0.0, 0.0],
            [16.8, 0.196, 0.196, 21.0, 21.0, 22.0, 0.0, 15.0, 0.0, 0.0],
            [27.9, 0.247, 0.247, 21.0, 21.0, 22.0, 0.0, 15.0, 0.0, 0.0]
        ]
    else:
        st.session_state.p_bar = 29.921259843
        st.session_state.temp_amb = 68
        datos_muestra = [
            [0.3000, 4.8381, 4.8381, 69.8, 69.8, 71.6, 0.0, 15.0, 0.0, 0.0],
            [0.3000, 4.8381, 4.7675, 69.8, 69.8, 71.6, 0.0, 15.0, 0.0, 0.0],
            [0.6614, 6.8864, 6.8864, 69.8, 69.8, 71.6, 0.0, 15.0, 0.0, 0.0],
            [0.6614, 6.9217, 6.9217, 69.8, 69.8, 71.6, 0.0, 15.0, 0.0, 0.0],
            [1.0984, 8.7227, 8.7227, 69.8, 69.8, 71.6, 0.0, 15.0, 0.0, 0.0]
        ]
        
    # Guardamos la estructura completa en la tabla de la memoria
    st.session_state.df_corridas = pd.DataFrame(datos_muestra, columns=columnas)
    
    # Forzamos a que el índice de las filas de la muestra empiece en 1
    st.session_state.df_corridas.index = range(1, 6)