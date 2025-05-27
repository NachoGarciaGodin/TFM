import rasterio
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from rasterio.mask import mask
from rasterio.transform import from_origin

# Rutas de los archivos
ruta_imagen = "C:/Users/nacho/Documents/TFM/imagenes/buenas/AND/812T_AND.tif"
ruta_shapefile = "C:/Users/nacho/Documents/TFM/OneDrive_1_23-5-2024 (1)/BA_2022_NN/BA_2022_imagenes_NN.shp"

# Cargar la imagen
with rasterio.open(ruta_imagen) as src:
    imagen = src.read(1)  # Leer la primera banda
    transform = src.transform
    width, height = src.width, src.height
    crs_imagen = src.crs

# Cargar el shapefile
shapefile = gpd.read_file(ruta_shapefile)

# Asegurarnos de que el CRS del shapefile es el mismo que el de la imagen
if shapefile.crs != crs_imagen:
    shapefile = shapefile.to_crs(crs_imagen)

# Crear una máscara binaria basada en el shapefile
mask_image = np.zeros((height, width), dtype=np.uint8)

# Iterar sobre las geometrías del shapefile y ponerlas en la máscara
for geom in shapefile.geometry:
    # Convertir geometrías a píxeles
    # Convertimos las coordenadas del shapefile a la resolución de la imagen
    minx, miny, maxx, maxy = geom.bounds
    col_start = int((minx - transform[2]) / transform[0])  # convertir X
    row_start = int((maxy - transform[5]) / transform[4])  # convertir Y
    col_end = int((maxx - transform[2]) / transform[0])  # convertir X
    row_end = int((miny - transform[5]) / transform[4])  # convertir Y
    
    # Asegurarnos de que no sobrepasamos los límites de la imagen
    col_start = max(0, col_start)
    row_start = max(0, row_start)
    col_end = min(width, col_end)
    row_end = min(height, row_end)
    
    # Rellenamos la máscara en el área correspondiente
    mask_image[row_start:row_end, col_start:col_end] = 1

# Visualización de la imagen y la máscara
fig, ax = plt.subplots(1, 2, figsize=(12, 6))

# Mostrar la imagen en el primer subplot
ax[0].imshow(imagen, cmap='gray')
ax[0].set_title('Imagen Original')

# Mostrar la máscara generada desde el shapefile en el segundo subplot
ax[1].imshow(mask_image, cmap='gray')
ax[1].set_title('Máscara del Shapefile')

# Mostrar la superposición en una sola imagen
fig, ax = plt.subplots(figsize=(8, 8))
ax.imshow(imagen, cmap='gray', alpha=0.5)  # Imagen con transparencia
ax.imshow(mask_image, cmap='Reds', alpha=0.5)  # Máscara del shapefile con rojo
ax.set_title('Superposición Imagen + Shapefile')

plt.show()
