import streamlit as st
import pandas as pd

# Archivo donde se guardan los resultados (puede ser un CSV o una base de datos)
DATA_FILE_ENJOY = "resultados_enjoy.csv"
DATA_FILE_ENERGY = "resultados_energy.csv"

# Función para cargar datos
def cargar_datos(file):
    try:
        return pd.read_csv(file)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Pareja 1", "Pareja 2", "Resultado"])

# Selección de copa
st.title("Torneo de Pádel 🏆")
opcion_copa = st.selectbox("Elige la copa:", ["Copa Enjoy", "Copa Energy"])

# Definir archivo según selección
if opcion_copa == "Copa Enjoy":
    DATA_FILE = DATA_FILE_ENJOY
else:
    DATA_FILE = DATA_FILE_ENERGY

df = cargar_datos(DATA_FILE)

# Formulario para ingresar resultados
st.header(f"Subir Resultado - {opcion_copa}")
col1, col2, col3 = st.columns(3)
with col1:
    pareja1 = st.text_input("Pareja 1")
with col2:
    pareja2 = st.text_input("Pareja 2")
with col3:
    resultado = st.text_input("Resultado (Ej: 6-3, 4-6, 10-7)")

if st.button("Enviar"):
    if pareja1 and pareja2 and resultado:
        nuevo_resultado = pd.DataFrame([[pareja1, pareja2, resultado]], columns=df.columns)
        df = pd.concat([df, nuevo_resultado], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Resultado guardado!")
        st.experimental_rerun()
    else:
        st.error("Por favor, completa todos los campos.")

# Mostrar tabla con los resultados ingresados
st.header(f"Resultados - {opcion_copa}")
st.dataframe(df)

# Procesar ranking
st.header(f"Ranking - {opcion_copa}")
ranking_dict = {}

for index, row in df.iterrows():
    pareja1, pareja2, resultado = row["Pareja 1"], row["Pareja 2"], row["Resultado"]
    sets = resultado.split(",")
    puntos_j1, puntos_j2 = 0, 0
    
    for set_score in sets:
        p1, p2 = map(int, set_score.strip().split("-"))
        puntos_j1 += p1
        puntos_j2 += p2
    
    ganador = pareja1 if puntos_j1 > puntos_j2 else pareja2
    perdedor = pareja2 if ganador == pareja1 else pareja1
    
    for pareja, puntos_favor, puntos_contra, victoria in [(ganador, puntos_j1, puntos_j2, 1), (perdedor, puntos_j2, puntos_j1, 0)]:
        if pareja not in ranking_dict:
            ranking_dict[pareja] = {"Victorias": 0, "Derrotas": 0, "Puntos Ganados": 0, "Puntos Perdidos": 0}
        ranking_dict[pareja]["Victorias"] += victoria
        ranking_dict[pareja]["Derrotas"] += 1 - victoria
        ranking_dict[pareja]["Puntos Ganados"] += puntos_favor
        ranking_dict[pareja]["Puntos Perdidos"] += puntos_contra
        
# Convertir a DataFrame y calcular diferencia de puntos
if not ranking_df.empty and "Puntos Ganados" in ranking_df and "Puntos Perdidos" in ranking_df:
    ranking_df["Diferencia de Puntos"] = ranking_df["Puntos Ganados"] - ranking_df["Puntos Perdidos"]
    ranking_df = ranking_df.sort_values(by=["Victorias", "Puntos Ganados", "Diferencia de Puntos"], ascending=[False, False, False])
else:
    st.warning("No hay suficientes datos para generar el ranking.")

# Ordenar por victorias, luego puntos ganados, luego diferencia de puntos
ranking_df = ranking_df.sort_values(by=["Victorias", "Puntos Ganados", "Diferencia de Puntos"], ascending=[False, False, False])

st.dataframe(ranking_df)
