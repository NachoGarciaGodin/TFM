#esto recorta un SHP con otro SHP

import geopandas as gpd

# Rutas de los shapefiles
ruta_shapefile_1 = "C:/Users/nacho/Desktop/MASCARA_FINAL/BA_2022_imagenes_NN.shp" 
ruta_shapefile_2 =  "C:/Users/nacho/Desktop/MASCARA_FINAL/ARCHIVO.shp"
ruta_shapefile_3 = "C:/Users/nacho/Desktop/MASCARA_FINAL/ARCHIVO2.shp"

# Cargar los shapefiles
shapefile_1 = gpd.read_file(ruta_shapefile_1)
shapefile_2 = gpd.read_file(ruta_shapefile_2)

# Asegurar que ambos shapefiles tengan el mismo sistema de coordenadas
if shapefile_1.crs != shapefile_2.crs:
    shapefile_2 = shapefile_2.to_crs(shapefile_1.crs)

# Realizar el recorte
shapefile_3 = gpd.overlay(shapefile_1, shapefile_2, how='intersection')

# Guardar el resultado como un nuevo shapefile
shapefile_3.to_file(ruta_shapefile_3)

print(f"Shapefile 3 guardado en {ruta_shapefile_3}")
