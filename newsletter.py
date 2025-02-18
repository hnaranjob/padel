import streamlit as st
import pandas as pd

# Configurar la página
st.set_page_config(page_title="Explorador de Datos Comparativos", layout="wide")

st.title("Resultados de la Newsletter")

# Cargar archivo CSV automáticamente
DATA_PATH = "resultados_v6 (1).csv"  # Cambia esto por la ruta de tu archivo
df = pd.read_csv(DATA_PATH)

# Mostrar los primeros registros para tener una vista previa de los datos
st.write("### Vista previa de los datos:")
st.dataframe(df.head())

# Inicializar lista de tablas guardadas en session_state
if "saved_tables" not in st.session_state:
    st.session_state.saved_tables = []

# Seleccionar las variables de interés para el análisis
action_column = 'ACTION_NAME'  # Columna que contiene 'bestsellers', 'IA', etc.
numeric_columns = df.select_dtypes(include="number").columns

grouped_columns = st.multiselect("Selecciona las columnas para agrupar:", df.columns)

# Mostrar las opciones para filtrar los datos
filter_columns = st.multiselect("Selecciona las columnas para filtrar:", df.columns)

# Diccionario para almacenar los filtros
filters = {}

# Crear selectores para cada columna elegida
for col in filter_columns:
    unique_values = df[col].dropna().unique()
    selected_values = st.multiselect(f"Filtrar por {col}", unique_values)
    if selected_values:
        filters[col] = selected_values

# Aplicar los filtros
df_filtered = df.copy()
for col, values in filters.items():
    df_filtered = df_filtered[df_filtered[col].isin(values)]

# Seleccionar la columna para el cálculo
selected_column = st.selectbox("Selecciona la columna para el cálculo (clics, compras, etc.):", numeric_columns)

# Crear las columnas para el groupby dinámico
group_columns = [action_column] + list(filters.keys())  # Incluir 'action_name' y las columnas seleccionadas

# Agrupar los datos por 'action_name' y las columnas de filtro
df_grouped = df_filtered.groupby(grouped_columns, as_index=False).agg(
    {selected_column: 'sum'}  # Cambia la columna numérica seleccionada para calcular la suma
)

# Calcular los porcentajes para la columna seleccionada basado en el 'action_name'
df_grouped['% ' + selected_column] = round(df_grouped.groupby(action_column)[selected_column].transform(lambda x: (x / x.sum()) * 100),2)

# Mostrar la tabla con los resultados
st.subheader("Tabla Comparativa por Categoría y Clics")
st.dataframe(df_grouped)



# Campo para que el usuario asigne un nombre a la tabla
table_name = st.text_input("Nombre de la tabla guardada:", "")

# Botón para guardar la tabla en session_state con nombre
if st.button("Guardar Tabla"):
    if table_name.strip() == "":
        st.warning("Por favor, ingresa un nombre para la tabla antes de guardarla.")
    else:
        st.session_state.saved_tables.append({"name": table_name, "data": df_grouped})
        st.success(f"Tabla '{table_name}' guardada correctamente.")

# Mostrar todas las tablas guardadas con opción de eliminarlas
st.subheader("📌 Tablas Guardadas:")

# Mostrar cada tabla con su nombre y botón para eliminarla
for i, table_entry in enumerate(st.session_state.saved_tables):
    st.write(f"### {table_entry['name']}")
    st.dataframe(table_entry["data"])
    if st.button(f"Eliminar '{table_entry['name']}'", key=f"delete_{i}"):
        st.session_state.saved_tables.pop(i)
        st.experimental_rerun()
