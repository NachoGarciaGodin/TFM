import rasterio
import numpy as np
import shutil

# Rutas de las bandas y la imagen de combinación lineal
ruta_banda2 = 'C:/Users/nacho/Documents/TFM/bandas_separadas/812T_banda2.tif'
ruta_banda11 = 'C:/Users/nacho/Documents/TFM/bandas_separadas/812T_banda11.tif'
ruta_combinacion_lineal = 'C:/Users/nacho/Documents/TFM/ImageJ/combinacion_lineal_812T.tif'
ruta_mascara = 'C:/Users/nacho/Documents/TFM/ImageJ/812T_mascara_mndwi.tif'

# Crear una copia de la imagen de combinación lineal para aplicar la máscara
shutil.copy(ruta_combinacion_lineal, ruta_mascara)

# Leer las bandas
with rasterio.open(ruta_banda2) as src_banda2, rasterio.open(ruta_banda11) as src_banda11:
    banda2 = src_banda2.read(1).astype(float)
    banda11 = src_banda11.read(1).astype(float)

    # Manejo de valores nulos (opcional): reemplazar valores nulos o negativos
    banda2[banda2 < 0] = np.nan
    banda11[banda11 < 0] = np.nan

    # Diagnóstico: mostrar estadísticas
    print(f"Estadísticas de Banda 2: Min: {np.nanmin(banda2)}, Max: {np.nanmax(banda2)}, NaNs: {np.isnan(banda2).sum()}")
    print(f"Estadísticas de Banda 11: Min: {np.nanmin(banda11)}, Max: {np.nanmax(banda11)}, NaNs: {np.isnan(banda11).sum()}")

    # Calcular el MNDWI evitando la división por cero
    suma_bandas = banda2 + banda11
    mndwi = np.zeros_like(suma_bandas)

    # Solo calcular donde suma_bandas no es cero
    valid_mask = suma_bandas != 0
    mndwi[valid_mask] = (banda2[valid_mask] - banda11[valid_mask]) / suma_bandas[valid_mask]

    # Definir un umbral para detectar agua (ejemplo: MNDWI > 0 indica agua)
    umbral_agua = 0.025

    # Leer la imagen de combinación lineal para aplicar la máscara
    with rasterio.open(ruta_mascara, 'r+') as dst:
        # Leer la banda de datos de la imagen de combinación lineal
        datos = dst.read(1)

        # Definir un valor específico para 'no data'
        nodata_value = 0  # Cambiar este valor según sea necesario
        dst.nodata = nodata_value

        # Aplicar la máscara: convertir a 'no data' los píxeles que representan agua
        datos[mndwi > umbral_agua] = nodata_value

        # Guardar la imagen con la máscara aplicada
        dst.write(datos, 1)

print(f"Imagen guardada en: {ruta_mascara}")
