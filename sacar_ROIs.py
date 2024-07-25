import geopandas as gpd
import matplotlib.pyplot as plt

# Ruta del shapefile de puntos
puntos_shapefile_path = "C:/Users/nacho/OneDrive - Universidad de Alcala/TFM/OneDrive_1_23-5-2024 (1)/BA_2022_NN/puntos1.shp"

# Leer el shapefile de puntos
puntos = gpd.read_file(puntos_shapefile_path)

# Mostrar los datos de los puntos
print("Datos de los puntos:")
print(puntos)

# Crear una figura para mostrar los puntos
plt.figure(figsize=(10, 10))
ax = puntos.plot(marker='o', color='red', markersize=5, alpha=0.7)
plt.title('Puntos de Interés')
plt.xlabel('Longitud')
plt.ylabel('Latitud')
plt.grid(True)

# Mostrar la figura
plt.show()
