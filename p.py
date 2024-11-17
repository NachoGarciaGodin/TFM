import os
import numpy as np
import rasterio

class PatchGenerator:
    def __init__(self, img_dir, mask_dir, patch_size=(448, 448), overlap=0.377):
        self.img_dir = img_dir
        self.mask_dir = mask_dir
        self.patch_size = patch_size
        self.overlap = overlap

    def generate_patches(self, output_img_dir, output_mask_dir):
        os.makedirs(output_img_dir, exist_ok=True)
        os.makedirs(output_mask_dir, exist_ok=True)

        for img_file in os.listdir(self.img_dir):
            if img_file.endswith('.tif'):
                mask_file = img_file.replace('.tif', '_mask.tif')
                img_path = os.path.join(self.img_dir, img_file)
                mask_path = os.path.join(self.mask_dir, mask_file)

                print(f"Processing image: {img_path}")
                print(f"Processing mask: {mask_path}")

                # Verifica si existen los archivos de imagen y máscara
                if not os.path.exists(mask_path):
                    print(f"Mask not found for {img_file}. Skipping.")
                    continue

                with rasterio.open(img_path) as img_src:
                    img = img_src.read()
                    height, width = img.shape[1], img.shape[2]
                    print(f"Image dimensions (HxW): {height}x{width}")

                with rasterio.open(mask_path) as mask_src:
                    mask = mask_src.read()

                # Calcula el paso en función del tamaño del patch y el solapamiento
                patch_num = 0
                step = int(self.patch_size[0] * (1 - self.overlap))
                if height < self.patch_size[0] or width < self.patch_size[1]:
                    print(f"Image {img_file} is too small for the patch size. Skipping.")
                    continue

                # Genera los patches de la imagen y la máscara
                for i in range(0, height - self.patch_size[0] + 1, step):
                    for j in range(0, width - self.patch_size[1] + 1, step):
                        img_patch = img[:, i:i + self.patch_size[0], j:j + self.patch_size[1]]
                        mask_patch = mask[:, i:i + self.patch_size[0], j:j + self.patch_size[1]]
                        
                        img_patch_path = os.path.join(output_img_dir, f'{img_file.replace(".tif", "")}_patch_{patch_num}.tif')
                        mask_patch_path = os.path.join(output_mask_dir, f'{mask_file.replace(".tif", "")}_patch_{patch_num}.tif')
                        
                        print(f"Saving patch {patch_num} to {img_patch_path} and {mask_patch_path}")

                        with rasterio.open(img_patch_path, 'w', 
                                           driver='GTiff', 
                                           height=self.patch_size[0], 
                                           width=self.patch_size[1], 
                                           count=img.shape[0], 
                                           dtype=img.dtype) as dst:
                            dst.write(img_patch)
                        
                        with rasterio.open(mask_patch_path, 'w', 
                                           driver='GTiff', 
                                           height=self.patch_size[0], 
                                           width=self.patch_size[1], 
                                           count=mask.shape[0], 
                                           dtype=mask.dtype) as dst:
                            dst.write(mask_patch)

                        patch_num += 1

                if patch_num == 0:
                    print(f"No patches generated for {img_file} due to insufficient size or other constraints.")

# Configura los directorios de entrada y salida
img_dir = "C:/Users/nacho/Documents/TFM/red_prueba/imagenes/"
mask_dir = "C:/Users/nacho/Documents/TFM/red_prueba/mascaras/"
output_img_dir = "C:/Users/nacho/Documents/TFM/red_prueba/output_patches/images/"
output_mask_dir = "C:/Users/nacho/Documents/TFM/red_prueba/output_patches/masks/"

# Genera y guarda los patches
patch_generator = PatchGenerator(img_dir, mask_dir)
patch_generator.generate_patches(output_img_dir, output_mask_dir)
