import rasterio
import rasterio.mask
import fiona
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt

ruta1 = "C:/Users/nacho/OneDrive - Universidad de Alcala/TFM/imagenes/812T.tif"
ruta2 = "C:/Users/nacho/OneDrive - Universidad de Alcala/TFM/imagenes/822T.tif"
ruta3 = "C:/Users/nacho/OneDrive - Universidad de Alcala/TFM/imagenes/827T.tif"

for k in range (1,4):
    image_path = globals()[f"ruta{k}"]

    for i in range (1,8):
        
        shapefile_path = f"C:/Users/nacho/OneDrive - Universidad de Alcala/TFM/shp/recorte{i}.shp"
        puntos_shapefile_path = f"C:/Users/nacho/OneDrive - Universidad de Alcala/TFM/shp/puntos{i}.shp"

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

        with rasterio.open(f"C:/Users/nacho/OneDrive - Universidad de Alcala/TFM/resultados/imagen_recortada_{k}_{i}.tif", "w", **out_meta) as dest:
            dest.write(out_image)

        image_path2 = f"C:/Users/nacho/OneDrive - Universidad de Alcala/TFM/resultados/imagen_recortada_{k}_{i}.tif"
        # Leer el shapefile de puntos
        puntos = gpd.read_file(puntos_shapefile_path)

        # Crear una lista para almacenar los valores espectrales
        valores_espectrales = []

        # Obtener los valores de cada banda en los puntos del shapefile
        with rasterio.open(image_path2) as src:
            for index, row in puntos.iterrows():
                x, y = row.geometry.x, row.geometry.y
                # Convertir las coordenadas del punto al sistema de referencia del raster
                px, py = src.index(x, y)
                # Extraer los valores de las 12 bandas en las coordenadas del punto
                if 0 <= px < src.width and 0 <= py < src.height:
                    valores = [src.read(i)[py,px] for i in range(1, 13)]
                    valores_espectrales.append(valores)

        # Convertir los valores a un array de NumPy para facilitar el manejo
        valores_espectrales = np.array(valores_espectrales)

        # Calcular el valor máximo, mínimo y la media para cada banda
        valores_maximos = np.max(valores_espectrales, axis=0)
        valores_minimos = np.min(valores_espectrales, axis=0)
        valores_medios = np.mean(valores_espectrales, axis=0)

        # Longitudes de onda en micrómetros para las 12 bandas
        longitudes_de_onda = [0.443, 0.490, 0.560, 0.665, 0.705, 0.740, 0.783, 0.842, 0.945, 1.375, 1.610, 2.190]

        plt.plot(longitudes_de_onda, valores_maximos, marker='o', color='red', label='Máximo')
        plt.plot(longitudes_de_onda, valores_minimos, marker='o', color='red', label='Mínimo', linestyle='--')
        plt.plot(longitudes_de_onda, valores_medios, marker='o', color='blue', label='Media')

        plt.xlabel('Longitud de onda (micrómetros)')
        plt.ylabel('Reflectancia')
        plt.title('Respuesta Espectral en los Puntos de Interés')
        plt.grid(True)
        plt.legend()

        # Guardar el gráfico como una imagen PNG
        plt.savefig(f"C:/Users/nacho/OneDrive - Universidad de Alcala/TFM/resultados/respuesta_espectral_{k}_{i}.png")
        plt.close()
        print(f"El gráfico de la respuesta espectral se ha guardado en resultados como respuesta_espectral_{k}_{i}.png")
