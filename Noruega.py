import folium

# Crear un mapa centrado en Noruega
mapa = folium.Map(location=[60.472, 8.4689], zoom_start=6)

# Datos de ejemplo: [nombre, latitud, longitud, tipo]
lugares = [
    ("Hotel en Oslo", 59.9139, 10.7522, "hospedaje"),
    ("Bergen", 60.3913, 5.3221, "pueblo"),
    ("Restaurante en Tromsø", 69.6496, 18.956, "restaurante"),
    ("Alesund", 62.4723, 6.1549, "pueblo"),
    ("Hotel en Trondheim", 63.4305, 10.3951, "hospedaje"),
]

# Colores según el tipo de lugar
colores = {
    "hospedaje": "blue",
    "pueblo": "green",
    "restaurante": "red",
}

# Agregar marcadores al mapa
for nombre, lat, lon, tipo in lugares:
    folium.Marker(
        location=[lat, lon],
        popup=nombre,
        icon=folium.Icon(color=colores[tipo])
    ).add_to(mapa)

# Guardar el mapa como HTML
mapa.save("mapa_noruega.html")

print("Mapa guardado como 'mapa_noruega.html'. Ábrelo en un navegador para verlo.")
