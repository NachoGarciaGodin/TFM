import numpy as np
import rasterio
from collections import Counter

# Ruta de la imagen
ruta = "C:/Users/nacho/Documents/TFM/ImageJ/812T_NBR2_NDVI_MEAN.tif"

# Parámetros iniciales
min_patch_size = 64
max_patch_size = 512
step_size = 64
min_overlap_ratio = 0.0
max_overlap_ratio = 0.5

# Cargar la imagen
with rasterio.open(ruta) as src:
    imagen = src.read(1).astype('float32')
    perfil = src.profile

# Contar valores de los píxeles
conteo_pixeles = Counter(imagen.flatten())
print(f"Distribución de los valores de píxeles: {conteo_pixeles}")

# Inicializar variables para el mejor patch y solapamiento
best_patch_size = None
best_overlap = None
best_coverage = 0

# Loop para probar distintos tamaños de patch y solapamiento
for patch_size in range(min_patch_size, max_patch_size + 1, step_size):
    for overlap_ratio in np.linspace(min_overlap_ratio, max_overlap_ratio, num=5):
        overlap = int(patch_size * overlap_ratio)
        total_patches = 0
        burned_pixel_count = 0

        for y in range(0, imagen.shape[0] - patch_size + 1, patch_size - overlap):
            for x in range(0, imagen.shape[1] - patch_size + 1, patch_size - overlap):
                patch = imagen[y:y + patch_size, x:x + patch_size]
                burned_pixels = np.sum(patch == 255)
                burned_pixel_count += burned_pixels
                total_patches += 1

        # Calcular el ratio de cobertura de píxeles quemados en este tamaño de patch
        coverage_ratio = burned_pixel_count / (total_patches * patch_size * patch_size)

        # Guardar el mejor tamaño de patch y solapamiento si es el mejor hasta ahora
        if coverage_ratio > best_coverage:
            best_coverage = coverage_ratio
            best_patch_size = patch_size
            best_overlap = overlap

if best_patch_size is None or best_overlap is None:
    raise ValueError("No se pudo determinar un tamaño de patch y solapamiento adecuados")

print(f"Tamaño recomendado de patch: {best_patch_size}")
print(f"Solapamiento recomendado: {best_overlap}")
print(f"Ratio de cobertura de píxeles quemados: {best_coverage:.4f}")
