import numpy as np
import rasterio
from rasterio import open as rio_open

# Rutas de entrada y salida
ruta_bandas = "C:/Users/nacho/Documents/TFM/imagenes/buenas/bandas_separadas/"
output_indices_folder = "C:/Users/nacho/Documents/TFM/imagenes/buenas/indices/"
output_umbral_folder = "C:/Users/nacho/Documents/TFM/imagenes/buenas/umbral/"

# Lista de imágenes base
base_names = ["29TPG", "29TPH", "30SXJ", "30SYJ", "628", "812T", "822T", "827T", "T29TNF_20171027T112139_image", "T29TPF_20171027T112139_image"]

# Función para calcular el NBR2
def calcular_nbr2(banda7_data, banda10_data):
    return np.where((banda7_data + banda10_data) != 0, (banda7_data - banda10_data) / (banda7_data + banda10_data), np.nan)

# Función para calcular el NDVI
def calcular_ndvi(banda3_data, banda8A_data):
    return np.where((banda8A_data + banda3_data) != 0, (banda8A_data - banda3_data) / (banda8A_data + banda3_data), np.nan)

# Función para umbralizar las imágenes
def umbralizar(imagen_data, umbral, nodata_value):
    """Umbraliza la imagen según el valor del umbral: valores por encima del umbral se ponen a NoData, el resto a 1"""
    imagen_umbralizada = np.where(imagen_data <= umbral, 1, nodata_value)
    return imagen_umbralizada

# Iterar sobre todas las imágenes base
for base_name in base_names:
    # Definir las rutas de las bandas para cada imagen
    banda7 = f"{ruta_bandas}{base_name}_banda7.tif"
    banda10 = f"{ruta_bandas}{base_name}_banda10.tif" if base_name not in ["29TPH", "30SXJ", "30SYJ"] else f"{ruta_bandas}{base_name}_banda11.tif"
    banda3 = f"{ruta_bandas}{base_name}_banda3.tif"
    banda8A = f"{ruta_bandas}{base_name}_banda8A.tif"
    
    # Cargar las bandas
    with rio_open(banda7) as src7:
        banda7_data = src7.read(1).astype('float32')
    with rio_open(banda10) as src10:
        banda10_data = src10.read(1).astype('float32')
    with rio_open(banda3) as src3:
        banda3_data = src3.read(1).astype('float32')
    with rio_open(banda8A) as src8A:
        banda8A_data = src8A.read(1).astype('float32')
    
    # Calcular NBR2 y NDVI
    nbr2 = calcular_nbr2(banda7_data, banda10_data)
    ndvi = calcular_ndvi(banda3_data, banda8A_data)

    # Guardar NBR2
    ruta_salida_nbr2 = f"{output_indices_folder}{base_name}_NBR2.tif"
    with rio_open(ruta_salida_nbr2, 'w', driver='GTiff', height=banda7_data.shape[0],
                  width=banda7_data.shape[1], count=1, dtype=nbr2.dtype,
                  crs=src7.crs, transform=src7.transform) as dst_nbr2:
        dst_nbr2.write(nbr2, 1)
    print(f"Imagen NBR2 guardada en: {ruta_salida_nbr2}")
    
    # Guardar NDVI
    ruta_salida_ndvi = f"{output_indices_folder}{base_name}_NDVI.tif"
    with rio_open(ruta_salida_ndvi, 'w', driver='GTiff', height=banda3_data.shape[0],
                  width=banda3_data.shape[1], count=1, dtype=ndvi.dtype,
                  crs=src3.crs, transform=src3.transform) as dst_ndvi:
        dst_ndvi.write(ndvi, 1)
    print(f"Imagen NDVI guardada en: {ruta_salida_ndvi}")
    
    # Umbralizar NBR2 (umbral -0.280)
    umbral_nbr2 = -0.280
    nodata_value = -9999  # Definir valor NoData (ajústalo si es necesario)
    nbr2_umbralizado = umbralizar(nbr2, umbral_nbr2, nodata_value)
    ruta_salida_nbr2_umbralizado = f"{output_umbral_folder}{base_name}_NBR2_umbralizado.tif"
    with rio_open(ruta_salida_nbr2_umbralizado, 'w', driver='GTiff', height=nbr2_umbralizado.shape[0],
                  width=nbr2_umbralizado.shape[1], count=1, dtype=nbr2_umbralizado.dtype,
                  crs=src7.crs, transform=src7.transform, nodata=nodata_value) as dst_nbr2_umbralizado:
        dst_nbr2_umbralizado.write(nbr2_umbralizado, 1)
    print(f"Imagen NBR2 umbralizado guardada en: {ruta_salida_nbr2_umbralizado}")
    
    # Umbralizar NDVI (umbral 0.1245)
    umbral_ndvi = 0.1245
    ndvi_umbralizado = umbralizar(ndvi, umbral_ndvi, nodata_value)
    ruta_salida_ndvi_umbralizado = f"{output_umbral_folder}{base_name}_NDVI_umbralizado.tif"
    with rio_open(ruta_salida_ndvi_umbralizado, 'w', driver='GTiff', height=ndvi_umbralizado.shape[0],
                  width=ndvi_umbralizado.shape[1], count=1, dtype=ndvi_umbralizado.dtype,
                  crs=src3.crs, transform=src3.transform, nodata=nodata_value) as dst_ndvi_umbralizado:
        dst_ndvi_umbralizado.write(ndvi_umbralizado, 1)
    print(f"Imagen NDVI umbralizado guardada en: {ruta_salida_ndvi_umbralizado}")
