import numpy as np
import rasterio
from rasterio import open as rio_open

# Rutas de entrada y salida
ruta_bandas = "C:/Users/nacho/Documents/TFM/bandas_separadas/"
ruta_comb = "C:/Users/nacho/Documents/TFM/ImageJ/combinacion_lineal_827T.tif"
ruta_salida = "C:/Users/nacho/Documents/TFM/ImageJ/827T_mascara_NGDR_SAHM.tif"

# Nombres de las bandas (ajusta según las bandas que tengas)
banda2 = f"{ruta_bandas}827T_banda2.tif"  # Banda Azul
banda3 = f"{ruta_bandas}827T_banda3.tif"  # Banda Verde
banda4 = f"{ruta_bandas}827T_banda4.tif"  # Banda Rojo
banda11 = f"{ruta_bandas}827T_banda11.tif"  # Banda SWIR
banda12 = f"{ruta_bandas}827T_banda12.tif"  # Banda SWIR2

# Cargar las bandas
with rio_open(banda2) as src2:
    banda2_data = src2.read(1).astype('float32')
with rio_open(banda3) as src3:
    banda3_data = src3.read(1).astype('float32')
with rio_open(banda4) as src4:
    banda4_data = src4.read(1).astype('float32')
with rio_open(banda11) as src11:
    banda11_data = src11.read(1).astype('float32')
with rio_open(banda12) as src12:
    banda12_data = src12.read(1).astype('float32')

# Calcular los índices
ngdr = np.where((banda2_data + banda3_data) != 0, (banda2_data - banda3_data) / (banda2_data + banda3_data), np.nan)
inverse = np.where((banda2_data - 0.2) != 0, (banda2_data - 0.2) / (0.5 - 0.2), np.nan)
sahm_index = np.where((banda12_data + banda11_data) != 0, (banda12_data - banda11_data) / (banda12_data + banda11_data), np.nan)

# Cargar la imagen de combinación lineal para aplicar la máscara
with rio_open(ruta_comb) as dst:
    datos_comb = dst.read(1).astype('float32')
    nodata_value = dst.nodata  # Obtener valor de no data

# Aplicar las condiciones para detectar fuego y nubes
datos_comb[(inverse > 1) | ((inverse > 0) & (ngdr > 0))] = nodata_value
datos_comb[(sahm_index > 0.4) | (banda12_data > 1)] = nodata_value

# Guardar la imagen con la máscara aplicada
with rio_open(ruta_salida, 'w', driver='GTiff', height=datos_comb.shape[0],
              width=datos_comb.shape[1], count=1, dtype=datos_comb.dtype,
              crs=dst.crs, transform=dst.transform) as dst_out:
    dst_out.write(datos_comb, 1)

print(f"Imagen guardada en: {ruta_salida}")
