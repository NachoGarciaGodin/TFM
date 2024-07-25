import rasterio
import rasterio.mask
import fiona

# Ruta de la imagen .tif
image_path = "C:/Users/nacho/OneDrive - Universidad de Alcala/TFM/OneDrive_1_23-5-2024 (1)/T29TPG_20220822T112119_image.tif"
# Ruta del shapefile
shapefile_path = "C:/Users/nacho/OneDrive - Universidad de Alcala/TFM/OneDrive_1_23-5-2024 (1)/BA_2022_NN/recorte1.shp"

# Abrir el shapefile y leer las geometrías
with fiona.open(shapefile_path, "r") as shapefile:
    # Extraer las geometrías del shapefile
    shapes = [feature["geometry"] for feature in shapefile]

# Abrir la imagen .tif y extraer los valores de las bandas
with rasterio.open(image_path) as src:
    # Inicializar variables para cada banda
    banda1 = src.read(1)
    banda2 = src.read(2)
    banda3 = src.read(3)
    banda4 = src.read(4)
    banda5 = src.read(5)
    banda6 = src.read(6)
    banda7 = src.read(7)
    banda8 = src.read(8)
    banda9 = src.read(9)
    banda10 = src.read(10)
    banda11 = src.read(11)
    banda12 = src.read(12)
    out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
    out_meta = src.meta

out_meta.update({"driver": "GTiff",
                 "height": out_image.shape[1],
                 "width": out_image.shape[2],
                 "transform": out_transform})

with rasterio.open("C:/Users/nacho/OneDrive - Universidad de Alcala/TFM/OneDrive_1_23-5-2024 (1)/BA_2022_NN/imagen_recortada.tif", "w", **out_meta) as dest:
    dest.write(out_image)

# Imprimir algunos valores de cada banda para verificar
print("Valores de la Banda 1:")
print(banda1)
print("\nValores de la Banda 2:")
print(banda2)
# Imprimir las dimensiones de cada banda
print(f"Dimensiones de la Banda 1: {banda1.shape}")
print(f"Dimensiones de la Banda 2: {banda2.shape}")

# Mostrar las geometrías extraídas
for i, shape in enumerate(shapes):
    print(f"Geometría {i + 1}:")
    print(shape)
    print()
