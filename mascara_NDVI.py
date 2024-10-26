import numpy as np
import rasterio
from rasterio import open as rio_open

# Rutas de entrada y salida
ruta_bandas = "C:/Users/nacho/Documents/TFM/bandas_separadas/"
ruta_comb = "C:/Users/nacho/Documents/TFM/ImageJ/combinacion_lineal_827T.tif"
ruta_salida = "C:/Users/nacho/Documents/TFM/ImageJ/827T_mascara_ndvi.tif"

# Nombres de las bandas
banda4 = f"{ruta_bandas}827T_banda4.tif"  # Banda Verde
banda8A = f"{ruta_bandas}827T_banda8A.tif"  # Banda Infrarrojo de onda corta

# Cargar las bandas
with rio_open(banda4) as src3:
    banda4_data = src3.read(1).astype('float32')

with rio_open(banda8A) as src8A:
    banda8A_data = src8A.read(1).astype('float32')

# Verificar valores de las bandas
print(f"Estadísticas de Banda 3: Min: {banda4_data.min()}, Max: {banda4_data.max()}, NaNs: {np.isnan(banda4_data).sum()}")
print(f"Estadísticas de Banda 8A: Min: {banda8A_data.min()}, Max: {banda8A_data.max()}, NaNs: {np.isnan(banda8A_data).sum()}")

# Calcular el NDWI
ndwi = np.where((banda4_data + banda8A_data) != 0, (banda4_data - banda8A_data) / (banda4_data + banda8A_data), np.nan)

# Cargar la imagen de combinación lineal para aplicar la máscara
with rio_open(ruta_comb) as dst:
    datos_comb = dst.read(1).astype('float32')
    nodata_value = dst.nodata  # Obtener valor de no data

# Aplicar la máscara de "no data" donde el NDWI indica la presencia de agua
umbral_agua = 0.05
datos_comb[ndwi > umbral_agua] = nodata_value

# Guardar la imagen con la máscara aplicada
with rio_open(ruta_salida, 'w', driver='GTiff', height=datos_comb.shape[0],
              width=datos_comb.shape[1], count=1, dtype=datos_comb.dtype,
              crs=dst.crs, transform=dst.transform) as dst_out:
    dst_out.write(datos_comb, 1)

print(f"Imagen guardada en: {ruta_salida}")
