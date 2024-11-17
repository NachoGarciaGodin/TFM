import os
import numpy as np
from shutil import copy2
from PIL import Image

# Rutas a las carpetas de parches
output_img_dir = "C:/Users/nacho/Documents/TFM/red_prueba/output_patches/images/"
output_mask_dir = "C:/Users/nacho/Documents/TFM/red_prueba/output_patches/masks/"

# Rutas para guardar los datos divididos
train_img_dir = "C:/Users/nacho/Documents/TFM/red_prueba/dataset/train/images/"
train_mask_dir = "C:/Users/nacho/Documents/TFM/red_prueba/dataset/train/masks/"
val_img_dir = "C:/Users/nacho/Documents/TFM/red_prueba/dataset/val/images/"
val_mask_dir = "C:/Users/nacho/Documents/TFM/red_prueba/dataset/val/masks/"
test_img_dir = "C:/Users/nacho/Documents/TFM/red_prueba/dataset/test/images/"
test_mask_dir = "C:/Users/nacho/Documents/TFM/red_prueba/dataset/test/masks/"

# Crear las carpetas necesarias
for path in [train_img_dir, train_mask_dir, val_img_dir, val_mask_dir, test_img_dir, test_mask_dir]:
    os.makedirs(path, exist_ok=True)

# Función para cargar los parches
def load_patches(patch_dir):
    return sorted([os.path.join(patch_dir, filename) for filename in os.listdir(patch_dir) if filename.endswith(".tif")])

# Cargar imágenes y máscaras
image_patches = load_patches(output_img_dir)
mask_patches = load_patches(output_mask_dir)

# Verificar que el número de imágenes y máscaras coincide
if len(image_patches) != len(mask_patches):
    raise ValueError("El número de imágenes y máscaras no coincide.")
print(f"Total de parches de imágenes: {len(image_patches)}")
print(f"Total de parches de máscaras: {len(mask_patches)}")

# Función para calcular la proporción de píxeles quemados (valor 255)
def calculate_burn_ratio(mask_path):
    mask = np.array(Image.open(mask_path))
    burn_ratio = np.sum(mask == 255) / mask.size
    return burn_ratio

# Calcular proporciones y asociarlas con las imágenes/máscaras
patch_data = [
    (img, mask, calculate_burn_ratio(mask)) for img, mask in zip(image_patches, mask_patches)
]

# Ordenar los datos por proporción de quemado de mayor a menor
patch_data = sorted(patch_data, key=lambda x: x[2], reverse=True)

# Alternar la asignación con el patrón train, train, train, test, val
datasets = {"train": [], "val": [], "test": []}
dataset_order = ["train", "train", "train", "test", "val"]
left, right = 0, len(patch_data) - 1
index = 0

while left <= right:
    dataset = dataset_order[index % len(dataset_order)]
    datasets[dataset].append(patch_data[left])
    left += 1
    if left <= right:  # Asegurar que no haya duplicados
        datasets[dataset].append(patch_data[right])
        right -= 1
    index += 1

# Ajustar las cantidades finales (asegurar que son 720, 240, 240)
datasets["train"] = datasets["train"][:720]
datasets["test"] = datasets["test"][:240]
datasets["val"] = datasets["val"][:240]

# Función para copiar datos a carpetas
def copy_data(data, img_dest, mask_dest):
    for img, mask, _ in data:
        copy2(img, img_dest)
        copy2(mask, mask_dest)

# Copiar los datos a las carpetas correspondientes
copy_data(datasets["train"], train_img_dir, train_mask_dir)
copy_data(datasets["val"], val_img_dir, val_mask_dir)
copy_data(datasets["test"], test_img_dir, test_mask_dir)

# Resumen
print(f"Entrenamiento: {len(datasets['train'])} parches")
print(f"Validación: {len(datasets['val'])} parches")
print(f"Prueba: {len(datasets['test'])} parches")
