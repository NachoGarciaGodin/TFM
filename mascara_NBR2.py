import numpy as np
import rasterio
from rasterio import open as rio_open

# Rutas de entrada y salida
ruta_bandas = "C:/Users/nacho/Documents/TFM/bandas_separadas/"
ruta_comb = "C:/Users/nacho/Documents/TFM/ImageJ/combinacion_lineal_827T.tif"
ruta_salida = "C:/Users/nacho/Documents/TFM/ImageJ/827T_mascara_nbr2.tif"

# Nombres de las bandas
banda7 = f"{ruta_bandas}827T_banda7.tif"  # Banda NIR
banda10 = f"{ruta_bandas}827T_banda10.tif"  # Banda SWIR1

# Cargar las bandas
with rio_open(banda7) as src7:
    banda7_data = src7.read(1).astype('float32')

with rio_open(banda10) as src10:
    banda10_data = src10.read(1).astype('float32')

# Verificar valores de las bandas
print(f"Estadísticas de Banda 7: Min: {banda7_data.min()}, Max: {banda7_data.max()}, NaNs: {np.isnan(banda7_data).sum()}")
print(f"Estadísticas de Banda 10: Min: {banda10_data.min()}, Max: {banda10_data.max()}, NaNs: {np.isnan(banda10_data).sum()}")

# Calcular el NBR2
nbr2 = np.where((banda7_data + banda10_data) != 0, (banda7_data - banda10_data) / (banda7_data + banda10_data), np.nan)

# Cargar la imagen de combinación lineal para aplicar la máscara
with rio_open(ruta_comb) as dst:
    datos_comb = dst.read(1).astype('float32')
    nodata_value = dst.nodata  # Obtener valor de no data

# Aplicar la máscara de "no data" donde el NBR2 indica presencia de áreas quemadas (ajusta el umbral según tus necesidades)
umbral_quemado = 0.1  # Este valor puede ser ajustado
datos_comb[nbr2 > umbral_quemado] = nodata_value

# Guardar la imagen con la máscara aplicada
with rio_open(ruta_salida, 'w', driver='GTiff', height=datos_comb.shape[0],
              width=datos_comb.shape[1], count=1, dtype=datos_comb.dtype,
              crs=dst.crs, transform=dst.transform) as dst_out:
    dst_out.write(datos_comb, 1)

print(f"Imagen guardada en: {ruta_salida}")
