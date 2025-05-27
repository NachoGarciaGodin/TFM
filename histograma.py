import rasterio
import numpy as np
from collections import Counter

# Ruta de la imagen TIF
ruta_imagen = "C:/Users/nacho/Desktop/MASCARA_FINAL/and.tif"  # Cambia la ruta si es necesario

# Cargar la imagen
with rasterio.open(ruta_imagen) as src:
    imagen = src.read(1)  # Leer la primera banda

# Asegurar que no haya valores NaN
imagen = imagen[~np.isnan(imagen)]

# Contar los valores únicos
total_pixeles = imagen.size
valores, conteo = np.unique(imagen, return_counts=True)

# Mostrar el histograma en la terminal
print(f"{'Valor':<10}{'Frecuencia':<15}{'Porcentaje':<10}")
print("=" * 35)
for valor, num_pixeles in zip(valores, conteo):
    porcentaje = (num_pixeles / total_pixeles) * 100
    print(f"{valor:<10}{num_pixeles:<15}{porcentaje:.2f}%")
