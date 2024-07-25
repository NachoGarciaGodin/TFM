# import geopandas as gpd

# # Ruta del shapefile
# shapefile_path = "C:/Users/nacho/OneDrive - Universidad de Alcala/TFM/OneDrive_1_23-5-2024 (1)/BA_2022_NN/recorte1.shp"

# # Cargar el shapefile en una variable
# recorte1 = gpd.read_file(shapefile_path)

import fiona

# Ruta del shapefile
shapefile_path = "C:/Users/nacho/OneDrive - Universidad de Alcala/TFM/OneDrive_1_23-5-2024 (1)/BA_2022_NN/recorte1.shp"

# Abrir el shapefile y leer las geometrías
with fiona.open(shapefile_path, "r") as shapefile:
    # Extraer las geometrías del shapefile
    shapes = [feature["geometry"] for feature in shapefile]

# Mostrar las geometrías extraídas
for i, shape in enumerate(shapes):
    print(f"Geometría {i + 1}:")
    print(shape)
    print()


