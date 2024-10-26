import numpy as np
import matplotlib.pyplot as plt
import rasterio
from rasterio.plot import show

# Ruta de la imagen TIFF
ruta = "C:/Users/nacho/Documents/TFM/ImageJ/812T_NBR2_NDVI_MEAN.tif"

# Cargar la imagen TIFF
with rasterio.open(ruta) as src:
    imagen = src.read(1).astype('float32')  # Leer la banda 1

# Función para dividir la imagen en patches
def dividir_en_patches(imagen, tamaño_patch, solapamiento=0):
    alto, ancho = imagen.shape
    step = tamaño_patch - solapamiento
    patches = []
    
    for y in range(0, alto, step):
        for x in range(0, ancho, step):
            patch = imagen[y:y + tamaño_patch, x:x + tamaño_patch]
            if patch.shape == (tamaño_patch, tamaño_patch):
                patches.append(patch)
    
    return patches

# Parámetros
tamaño_patch = 448  # Tamaño de cada patch
solapamiento = 168  # Solapamiento de 37,7%
num_patches_a_mostrar = 400  # Número total de patches a mostrar (21x21)

# Dividir la imagen en patches
patches = dividir_en_patches(imagen, tamaño_patch, solapamiento)

# Ajustar para mostrar exactamente 441 patches (21x21)
if len(patches) < num_patches_a_mostrar:
    num_patches_a_mostrar = len(patches)

# Mostrar los 441 patches en una cuadrícula de 21x21
fig, axs = plt.subplots(21, 21, figsize=(30, 30))  # Tamaño de la figura ajustado para mayor visibilidad
fig.suptitle(f"Visualización de 441 patches", fontsize=16)

for i, ax in enumerate(axs.flatten()):
    if i < num_patches_a_mostrar:
        ax.imshow(patches[i], cmap='viridis')
        ax.set_title(f'Patch {i + 1}', fontsize=8)
        ax.axis('off')
    else:
        ax.axis('off')  # Desactivar si no hay más patches

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
