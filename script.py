import rasterio
import rasterio.mask
import fiona
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt

image_path = "C:/Users/nacho/OneDrive - Universidad de Alcala/TFM/OneDrive_1_23-5-2024 (1)/image_25830.tif"
shapefile_path = "C:/Users/nacho/OneDrive - Universidad de Alcala/TFM/shp/recorte2.shp"
puntos_shapefile_path = "C:/Users/nacho/OneDrive - Universidad de Alcala/TFM/shp/puntos2.shp"

# Abrir el shapefile y leer las geometrías
with fiona.open(shapefile_path, "r") as shapefile:
    # Extraer las geometrías del shapefile
    shapes = [feature["geometry"] for feature in shapefile]

# Abrir la imagen .tif y extraer los valores de las bandas
with rasterio.open(image_path) as src:
    # Inicializar variables para cada banda
    banda1 = src.read(1)
    banda2 = src.read(2)
    banda3 = src.read(3)
    banda4 = src.read(4)
    banda5 = src.read(5)
    banda6 = src.read(6)
    banda7 = src.read(7)
    banda8 = src.read(8)
    banda9 = src.read(9)
    banda10 = src.read(10)
    banda11 = src.read(11)
    banda12 = src.read(12)
    out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
    out_meta = src.meta

out_meta.update({"driver": "GTiff",
                 "height": out_image.shape[1],
                 "width": out_image.shape[2],
                 "transform": out_transform})

with rasterio.open("C:/Users/nacho/OneDrive - Universidad de Alcala/TFM/resultados/imagen_recortada.tif", "w", **out_meta) as dest:
    dest.write(out_image)

image_path2 = "C:/Users/nacho/OneDrive - Universidad de Alcala/TFM/resultados/imagen_recortada.tif"
# Leer el shapefile de puntos
puntos = gpd.read_file(puntos_shapefile_path)

# Crear una lista para almacenar los valores espectrales
valores_espectrales = []

# Obtener los valores de cada banda en los puntos del shapefile
with rasterio.open(image_path2) as src:
    for index, row in puntos.iterrows():
        x, y = row.geometry.x, row.geometry.y
        # Convertir las coordenadas del punto al sistema de referencia del raster
        px, py = src.index(x, y)
        # Extraer los valores de las 12 bandas en las coordenadas del punto
        if 0 <= px < src.width and 0 <= py < src.height:
            valores = [src.read(i)[py,px] for i in range(1, 13)]
            valores_espectrales.append(valores)

# Convertir los valores a un array de NumPy para facilitar el manejo
valores_espectrales = np.array(valores_espectrales)

# Crear un gráfico de la respuesta espectral
plt.figure(figsize=(10, 10))
for i in range(valores_espectrales.shape[1]):
    plt.plot(valores_espectrales[:, i], label=f'Banda {i+1}')

plt.xlabel('Puntos')
plt.ylabel('Valor de Reflectancia')
plt.title('Respuesta Espectral en los Puntos de Interés')
plt.legend()
plt.grid(True)

# Guardar el gráfico como una imagen PNG
plt.savefig("C:/Users/nacho/OneDrive - Universidad de Alcala/TFM/resultados/respuesta_espectral.png")

print("El gráfico de la respuesta espectral se ha guardado en resultados como respuesta_espectral.png")
