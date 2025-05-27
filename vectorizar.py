#esto pasa un TIF a SHP

import os
from osgeo import gdal, ogr
import geopandas as gpd
from shapely.geometry import shape
import json

# Configurar la variable de entorno GDAL_DATA
os.environ["GDAL_DATA"] = r"C:\Users\nacho\Miniconda3\Library\share\gdal"

# Ruta del raster
raster_path = "C:/Users/nacho/Desktop/MASCARA_FINAL/and.tif"

# Abrir el raster con GDAL
raster_ds = gdal.Open(raster_path)
if not raster_ds:
    raise FileNotFoundError(f"No se pudo abrir el raster en la ruta: {raster_path}")

# Obtener la banda del raster
raster_band = raster_ds.GetRasterBand(1)

# Crear una capa de memoria para los polígonos generados
driver = ogr.GetDriverByName('Memory')
polygon_ds = driver.CreateDataSource('memory')
layer = polygon_ds.CreateLayer('polygons', geom_type=ogr.wkbPolygon)

# Crear un campo para almacenar los valores del raster
layer.CreateField(ogr.FieldDefn('value', ogr.OFTInteger))

# Polygonizar el raster
gdal.Polygonize(raster_band, None, layer, 0, [], callback=None)

# Crear una lista para almacenar los polígonos válidos
polygons = []
values = []

# Recorrer las entidades y agregar solo aquellas que tengan valor distinto de 0
for feature in layer:
    value = feature.GetField('value')
    if value != 0:  # Solo guardar los polígonos con valor distinto de 0
        geometry = feature.GetGeometryRef()
        if geometry is not None and not geometry.IsEmpty():
            # Convertir la geometría a un objeto de Shapely
            geom_dict = json.loads(geometry.ExportToJson())
            shapely_geom = shape(geom_dict)
            if shapely_geom.is_valid:
                polygons.append(shapely_geom)
                values.append(value)

# Crear un GeoDataFrame solo con los polígonos válidos
gdf = gpd.GeoDataFrame({'geometry': polygons, 'value': values}, crs=raster_ds.GetProjection())

# Definir la ruta de salida del shapefile
output_shapefile_path = os.path.join(os.path.dirname(raster_path), "ARCHIVO.shp")

# Guardar el GeoDataFrame como un shapefile
gdf.to_file(output_shapefile_path, driver="ESRI Shapefile")

# Cerrar datasets
raster_ds = None
polygon_ds = None

print(f"Archivo shapefile guardado correctamente en: {output_shapefile_path}")
