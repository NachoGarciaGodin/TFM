import geopandas as gpd

# Cargar los shapefiles
shp2 = gpd.read_file("ARCHIVO.shp")
shp1 = gpd.read_file("ARCHIVO2.shp")

# Verificar si el CRS está definido para shp1
if shp1.crs is None:
    print("El CRS no está definido en shp1. Asignando CRS...")
    shp1 = shp1.set_crs("EPSG:25830")  # Cambia EPSG:25830 al CRS correcto para tu shapefile

# Verificar si el CRS está definido para shp2
if shp2.crs is None:
    print("El CRS no está definido en shp2. Asignando CRS...")
    shp2 = shp2.set_crs("EPSG:25830")  # Cambia EPSG:25830 si es necesario

# Asegurarse de que ambos shapefiles tengan la misma proyección
shp2 = shp2.to_crs(shp1.crs)

# Calcular la intersección
intersect = gpd.overlay(shp1, shp2, how='intersection')

# Calcular áreas
shp1['area'] = shp1.geometry.area  # Área total de shp1
intersect['intersect_area'] = intersect.geometry.area  # Área de solapamiento

# Calcular el porcentaje de solapamiento
total_area_shp1 = shp1['area'].sum()
total_overlap_area = intersect['intersect_area'].sum()
overlap_percentage = (total_overlap_area / total_area_shp1) * 100

# Resultados
print(f"Área total de shp1: {total_area_shp1:.2f}")
print(f"Área total de intersección: {total_overlap_area:.2f}")
print(f"Porcentaje de solapamiento: {overlap_percentage:.2f}%")