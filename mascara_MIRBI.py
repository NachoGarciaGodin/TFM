import numpy as np
import rasterio
from rasterio import open as rio_open

# Rutas de entrada y salida
ruta_bandas = "C:/Users/nacho/Documents/TFM/bandas_separadas/"
ruta_comb = "C:/Users/nacho/Documents/TFM/ImageJ/combinacion_lineal_812T.tif"
ruta_salida = "C:/Users/nacho/Documents/TFM/ImageJ/812T_mascara_mirbi.tif"

# Nombres de las bandas
banda7 = f"{ruta_bandas}812T_banda7.tif"  # Banda NIR
banda11 = f"{ruta_bandas}812T_banda11.tif"  # Banda SWIR2

# Cargar las bandas
with rio_open(banda7) as src7:
    banda7_data = src7.read(1).astype('float32')

with rio_open(banda11) as src11:
    banda11_data = src11.read(1).astype('float32')

# Verificar valores de las bandas
print(f"Estadísticas de Banda 7: Min: {banda7_data.min()}, Max: {banda7_data.max()}, NaNs: {np.isnan(banda7_data).sum()}")
print(f"Estadísticas de Banda 11: Min: {banda11_data.min()}, Max: {banda11_data.max()}, NaNs: {np.isnan(banda11_data).sum()}")

# Calcular el MIRBI
mirbi = np.where((banda7_data + banda11_data) != 0, (banda7_data - banda11_data) / (banda7_data + banda11_data), np.nan)

# Cargar la imagen de combinación lineal para aplicar la máscara
with rio_open(ruta_comb) as dst:
    datos_comb = dst.read(1).astype('float32')
    nodata_value = dst.nodata  # Obtener valor de no data

# Aplicar la máscara de "no data" donde el MIRBI indica presencia de áreas quemadas (ajusta el umbral según tus necesidades)
umbral_quemado = 0.2  # Este valor puede ser ajustado
datos_comb[mirbi > umbral_quemado] = nodata_value

# Guardar la imagen con la máscara aplicada
with rio_open(ruta_salida, 'w', driver='GTiff', height=datos_comb.shape[0],
              width=datos_comb.shape[1], count=1, dtype=datos_comb.dtype,
              crs=dst.crs, transform=dst.transform) as dst_out:
    dst_out.write(datos_comb, 1)

print(f"Imagen guardada en: {ruta_salida}")
