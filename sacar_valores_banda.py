import rasterio

# Ruta de la imagen .tif
image_path = "C:/Users/nacho/OneDrive - Universidad de Alcala/TFM/OneDrive_1_23-5-2024 (1)/T29TPG_20220822T112119_image.tif"

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
# Imprimir algunos valores de cada banda para verificar
print("Valores de la Banda 1:")
print(banda1)
print("\nValores de la Banda 2:")
print(banda2)
# Imprimir las dimensiones de cada banda
print(f"Dimensiones de la Banda 1: {banda1.shape}")
print(f"Dimensiones de la Banda 2: {banda2.shape}")



