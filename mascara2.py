import rasterio
import numpy as np
from scipy.ndimage import median_filter

# Definir rutas
ruta_imagen_1 = "C:/Users/nacho/Desktop/MASCARA_FINAL/827T_NBR2.tif"
ruta_imagen_2 = "C:/Users/nacho/Desktop/MASCARA_FINAL/827T_NDVI.tif"
ruta_umbralizada_NBR2 = "C:/Users/nacho/Desktop/MASCARA_FINAL/umbralizada_NBR2.tif"
ruta_umbralizada_NDVI = "C:/Users/nacho/Desktop/MASCARA_FINAL/umbralizada_NDVI.tif"
ruta_and = "C:/Users/nacho/Desktop/MASCARA_FINAL/and.tif"
ruta_filtro_median_NBR2 = "C:/Users/nacho/Desktop/MASCARA_FINAL/filtro_median_NBR2.tif"
ruta_filtro_median_NDVI = "C:/Users/nacho/Desktop/MASCARA_FINAL/filtro_median_NDVI.tif"

# Función para cargar una imagen con rasterio
def cargar_imagen(ruta):
    with rasterio.open(ruta) as src:
        data = src.read(1)  # Leer solo la primera banda
        profile = src.profile  # Mantener metadatos
    return data, profile

# Función para umbralizar una imagen
def umbralizar(imagen, umbral_min, umbral_max, invertir=False):
    resultado = np.zeros_like(imagen, dtype=imagen.dtype)
    if invertir:
        mask = (imagen < umbral_min) | (imagen > umbral_max)
    else:
        mask = (imagen >= umbral_min) & (imagen <= umbral_max)
    resultado[mask] = imagen[mask]
    return resultado

# Función para realizar la operación AND
def operacion_and(imagen1, imagen2):
    return np.logical_and(imagen1 > 0, imagen2 > 0).astype(np.uint8)  # Resultado binario (0 o 1)

# Función para aplicar el filtro mediano
def aplicar_filtro_median(imagen, tamaño_ventana=4):
    return median_filter(imagen, size=tamaño_ventana)  # Filtro mediano

# Función para guardar una imagen con rasterio
def guardar_imagen(ruta, data, profile):
    profile.update(dtype=data.dtype, count=1, compress='lzw')
    with rasterio.open(ruta, 'w', **profile) as dst:
        dst.write(data, 1)

# Paso 1: Cargar las imágenes
imagen_1, perfil_1 = cargar_imagen(ruta_imagen_1)
imagen_2, perfil_2 = cargar_imagen(ruta_imagen_2)

# Paso 2: Umbralizar las imágenes
umbral_min_NBR2 = -0.42
umbral_max_NBR2 = -0.125
umbral_min_NDVI = 0.018
umbral_max_NDVI = 0.175

imagen_1_umbralizada = umbralizar(imagen_1, umbral_min_NBR2, umbral_max_NBR2, invertir=False)
imagen_2_umbralizada = umbralizar(imagen_2, umbral_min_NDVI, umbral_max_NDVI)
imagen_1_umbralizada = -imagen_1_umbralizada

# Paso 3: Aplicar filtro mediano a las imágenes umbralizadas
imagen_1_filtro_median = aplicar_filtro_median(imagen_1_umbralizada, tamaño_ventana=8)
imagen_2_filtro_median = aplicar_filtro_median(imagen_2_umbralizada, tamaño_ventana=8)

# Paso 4: Realizar la operación AND entre las imágenes filtradas
imagen_and = operacion_and(imagen_1_filtro_median, imagen_2_filtro_median)

# Guardar las imágenes resultantes
guardar_imagen(ruta_umbralizada_NBR2, imagen_1_umbralizada, perfil_1)
guardar_imagen(ruta_umbralizada_NDVI, imagen_2_umbralizada, perfil_2)
guardar_imagen(ruta_filtro_median_NBR2, imagen_1_filtro_median, perfil_1)
guardar_imagen(ruta_filtro_median_NDVI, imagen_2_filtro_median, perfil_2)
guardar_imagen(ruta_and, imagen_and, perfil_1)  # Usando perfil de la primera imagen para la salida