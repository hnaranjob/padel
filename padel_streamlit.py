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
        return pd.DataFrame(columns=["Jugador 1", "Jugador 2", "Resultado"])

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
    jugador1 = st.text_input("Jugador 1")
with col2:
    jugador2 = st.text_input("Jugador 2")
with col3:
    resultado = st.text_input("Resultado (Ej: 6-3, 4-6, 10-7)")

if st.button("Enviar"):
    if jugador1 and jugador2 and resultado:
        nuevo_resultado = pd.DataFrame([[jugador1, jugador2, resultado]], columns=df.columns)
        df = pd.concat([df, nuevo_resultado], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Resultado guardado!")
        st.rerun()
    else:
        st.error("Por favor, completa todos los campos.")

# Mostrar tabla con los resultados ingresados
st.header(f"Resultados - {opcion_copa}")
st.dataframe(df)

# Opción para borrar resultados
st.header("Borrar Resultado")
if not df.empty:
    resultado_a_borrar = st.selectbox("Selecciona un resultado para borrar", df.apply(lambda row: f"{row['Jugador 1']} vs {row['Jugador 2']} - {row['Resultado']}", axis=1))
    if st.button("Borrar"):
        df = df[df.apply(lambda row: f"{row['Jugador 1']} vs {row['Jugador 2']} - {row['Resultado']}" != resultado_a_borrar, axis=1)]
        df.to_csv(DATA_FILE, index=False)
        st.success("Resultado eliminado!")
        st.rerun()

# Procesar ranking
st.header(f"Ranking - {opcion_copa}")
ranking_dict = {}

for index, row in df.iterrows():
    jugador1, jugador2, resultado = row["Jugador 1"], row["Jugador 2"], row["Resultado"]
    sets = resultado.split(",")
    puntos_j1, puntos_j2 = 0, 0
    
    for set_score in sets:
        p1, p2 = map(int, set_score.strip().split("-"))
        puntos_j1 += p1
        puntos_j2 += p2
    
    ganador = jugador1 if puntos_j1 > puntos_j2 else jugador2
    perdedor = jugador2 if ganador == jugador1 else jugador1
    
    for jugador, puntos_favor, puntos_contra, victoria in [(ganador, puntos_j1, puntos_j2, 1), (perdedor, puntos_j2, puntos_j1, 0)]:
        if jugador not in ranking_dict:
            ranking_dict[jugador] = {"Victorias": 0, "Derrotas": 0, "Puntos Ganados": 0, "Puntos Perdidos": 0}
        ranking_dict[jugador]["Victorias"] += victoria
        ranking_dict[jugador]["Derrotas"] += 1 - victoria
        ranking_dict[jugador]["Puntos Ganados"] += puntos_favor
        ranking_dict[jugador]["Puntos Perdidos"] += puntos_contra

# Convertir ranking_dict a DataFrame
ranking_df = pd.DataFrame.from_dict(ranking_dict, orient="index")

# Verificar si hay datos antes de calcular la diferencia de puntos
if not ranking_df.empty and "Puntos Ganados" in ranking_df and "Puntos Perdidos" in ranking_df:
    ranking_df["Diferencia de Puntos"] = ranking_df["Puntos Ganados"] - ranking_df["Puntos Perdidos"]
    ranking_df = ranking_df.sort_values(by=["Victorias", "Puntos Ganados", "Diferencia de Puntos"], ascending=[False, False, False])
else:
    st.warning("No hay suficientes datos para generar el ranking.")
