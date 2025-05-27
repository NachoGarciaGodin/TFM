import rasterio
import numpy as np
from scipy.ndimage import gaussian_filter, median_filter
from osgeo import gdal
from osgeo import ogr
import geopandas as gpd
from shapely.geometry import Polygon
import os

# Definir rutas
ruta_imagen_1 = "C:/Users/nacho/Desktop/MASCARA_FINAL/812T_NBR2.tif"
ruta_imagen_2 = "C:/Users/nacho/Desktop/MASCARA_FINAL/812T_NDVI.tif"
ruta_umbralizada_NBR2 = "C:/Users/nacho/Desktop/MASCARA_FINAL/umbralizada_NBR2.tif"
ruta_umbralizada_NDVI = "C:/Users/nacho/Desktop/MASCARA_FINAL/umbralizada_NDVI.tif"
ruta_and = "C:/Users/nacho/Desktop/MASCARA_FINAL/and.tif"
ruta_filtro_gaussiano = "C:/Users/nacho/Desktop/MASCARA_FINAL/filtro_gaussiano.tif"
ruta_binarizada = "C:/Users/nacho/Desktop/MASCARA_FINAL/binarizada.tif"
ruta_filtro_median_binarizada = "C:/Users/nacho/Desktop/MASCARA_FINAL/filtro_median_binarizada.tif"

# Función para cargar una imagen con rasterio
def cargar_imagen(ruta):
    with rasterio.open(ruta) as src:
        data = src.read(1)  # Leer solo la primera banda
        profile = src.profile  # Mantener metadatos
    return data, profile

# Función para umbralizar una imagen
def umbralizar(imagen, umbral_min, umbral_max, invertir=False):
    resultado = np.zeros_like(imagen, dtype=imagen.dtype)
    if invertir:
        mask = (imagen < umbral_min) | (imagen > umbral_max)
    else:
        mask = (imagen >= umbral_min) & (imagen <= umbral_max)
    resultado[mask] = imagen[mask]
    return resultado

# Función para realizar la operación AND
def operacion_and(imagen1, imagen2):
    return np.logical_and(imagen1, imagen2).astype(np.uint8)  # Resultado binario (0 o 1)

# Función para aplicar el filtro gaussiano
def aplicar_filtro_gaussiano(imagen, sigma=1):
    return gaussian_filter(imagen, sigma=sigma)  # Sigma controla el tamaño de la ventana gaussiana

# Función para binarizar una imagen manualmente usando un umbral
def binarizar(imagen, umbral):
    resultado = np.zeros_like(imagen, dtype=np.uint8)
    for i in range(imagen.shape[0]):
        for j in range(imagen.shape[1]):
            if imagen[i, j] >= umbral:
                resultado[i, j] = 1  # Asignar 1 si está por encima del umbral
            else:
                resultado[i, j] = 0  # Asignar 0 si está por debajo del umbral
    return resultado

# Función para aplicar el filtro mediano
def aplicar_filtro_median(imagen, tamaño_ventana=3):
    return median_filter(imagen, size=tamaño_ventana)  # Filtro mediano

# Función para guardar una imagen con rasterio
def guardar_imagen(ruta, data, profile):
    profile.update(dtype=data.dtype, count=1, compress='lzw')
    with rasterio.open(ruta, 'w', **profile) as dst:
        dst.write(data, 1)

# Paso 1: Cargar las imágenes
imagen_1, perfil_1 = cargar_imagen(ruta_imagen_1)
imagen_2, perfil_2 = cargar_imagen(ruta_imagen_2)

# Paso 2: Umbralizar la imagen de NBR2 con los valores negativos (-0.220 y -0.397)
umbral_min_NBR2 = -0.397
umbral_max_NBR2 = -0.220
umbral_min_NDVI = 0.0371
umbral_max_NDVI = 0.1072

imagen_1_umbralizada = umbralizar(imagen_1, umbral_min_NBR2, umbral_max_NBR2, invertir=False)
imagen_2_umbralizada = umbralizar(imagen_2, umbral_min_NDVI, umbral_max_NDVI)

# Paso 3: Invertir los signos de toda la imagen de NBR2 después de la umbralización
imagen_1_umbralizada = -imagen_1_umbralizada

# Paso 4: Realizar la operación AND entre ambas imágenes umbralizadas
imagen_and = operacion_and(imagen_1_umbralizada, imagen_2_umbralizada)

# Paso 5: Aplicar el filtro gaussiano
imagen_filtro_gaussiano = aplicar_filtro_gaussiano(imagen_1_umbralizada, sigma=1)  # Usando un sigma de 1

# Paso 6: Binarizar la imagen resultante del filtro gaussiano de forma manual
umbral_min = 0.2
umbral_max = 0.3868

# Binarizar: Los valores dentro del rango [umbral_min, umbral_max] se ponen a 1, y el resto a 0
imagen_binarizada = np.zeros_like(imagen_filtro_gaussiano, dtype=np.uint8)
imagen_binarizada[(imagen_filtro_gaussiano >= umbral_min) & (imagen_filtro_gaussiano <= umbral_max)] = 1

# Paso 7: Aplicar filtro mediano al resultado binarizado
imagen_filtro_median_binarizada = aplicar_filtro_median(imagen_binarizada, tamaño_ventana=8)

# Guardar las imágenes umbralizadas, la operación AND, el filtro gaussiano, la binarización y el filtro mediano
guardar_imagen(ruta_umbralizada_NBR2, imagen_1_umbralizada, perfil_1)
guardar_imagen(ruta_umbralizada_NDVI, imagen_2_umbralizada, perfil_2)
guardar_imagen(ruta_and, imagen_and, perfil_1)  # Usando perfil de la primera imagen para la salida
guardar_imagen(ruta_filtro_gaussiano, imagen_filtro_gaussiano, perfil_1)  # Guardando la imagen filtrada
guardar_imagen(ruta_binarizada, imagen_binarizada, perfil_1)  # Guardando la imagen binarizada
guardar_imagen(ruta_filtro_median_binarizada, imagen_filtro_median_binarizada, perfil_1)  # Guardando la imagen filtrada después del binarizado

# ---- Segunda parte (Polygonización) ----

# Ruta del raster
raster_path = "C:/Users/nacho/Desktop/MASCARA_FINAL/filtro_median_binarizada.tif"

# Abrir el raster con GDAL
raster_ds = gdal.Open(raster_path)

# Verificar que el raster se haya cargado correctamente
if not raster_ds:
    raise FileNotFoundError(f"No se pudo abrir el raster en la ruta: {raster_path}")

# Obtener la banda del raster (normalmente la primera banda)
raster_band = raster_ds.GetRasterBand(1)

# Crear una capa de memoria para los polígonos generados
driver = ogr.GetDriverByName('Memory')
polygon_ds = driver.CreateDataSource('memory')
layer = polygon_ds.CreateLayer('polygons', geom_type=ogr.wkbPolygon)

# Crear un campo para almacenar los valores del raster
field = ogr.FieldDefn('value', ogr.OFTInteger)
layer.CreateField(field)

# Polygonizar el raster
gdal.Polygonize(raster_band, None, layer, 0, [], callback=None)

# Convertir los resultados en un GeoDataFrame
polygons = []
values = []

# Recorrer las entidades de la capa
for feature in layer:
    geometry = feature.GetGeometryRef()
    if geometry is not None:
        # Comprobar si el polígono tiene al menos 4 puntos
        if geometry.GetGeometryCount() >= 4:
            # Convertir la geometría OGR a Shapely
            shapely_geom = Polygon([(geometry.GetX(i), geometry.GetY(i)) for i in range(geometry.GetGeometryCount())])
            polygons.append(shapely_geom)
            values.append(feature.GetField('value'))

# Crear un GeoDataFrame
gdf = gpd.GeoDataFrame({'geometry': polygons, 'value': values}, crs=raster_ds.GetProjection())

# Definir la ruta de salida
output_path = os.path.join(os.path.dirname(raster_path), "ARCHIVO.shp")

# Guardar el GeoDataFrame como Shapefile
gdf.to_file(output_path, driver="ESRI Shapefile")

print(f"Archivo guardado correctamente en: {output_path}")

# ---- Tercera parte (Intersección de Shapefiles) ----

# Cargar los shapefiles
shp2 = gpd.read_file("filtro_median_binarizada.shp")
shp1 = gpd.read_file("BA_2022_imagenes_NN.shp")

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
