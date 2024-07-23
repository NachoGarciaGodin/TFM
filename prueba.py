import fiona
import rasterio
import rasterio.mask

def recortar_bandas(image_path, shapefile_path):
    # Abrir el shapefile
    with fiona.open(shapefile_path, "r") as shapefile:
        shapes = [feature["geometry"] for feature in shapefile]

    # Abrir el raster y procesar cada banda
    bandas_recortadas = {}  # Diccionario para almacenar las bandas recortadas
    with rasterio.open(image_path) as src:
        print(f"CRS del raster: {src.crs}")
        print(f"Dimensiones del raster: {src.width} x {src.height}")

        for idx in range(1, src.count + 1):
            try:
                # Recortar la banda actual
                out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True, indexes=idx)
                
                # Almacenar la banda recortada en una variable
                bandas_recortadas[f'banda_{idx}'] = out_image
                
                print(f"Banda {idx} recortada, dimensiones: {out_image.shape}")

            except Exception as e:
                print(f"Error al recortar la banda {idx}: {e}")

    return bandas_recortadas

def main():
    # Definir rutas
    image_path = "C:/Users/nacho/OneDrive - Universidad de Alcala/TFM/OneDrive_1_23-5-2024 (1)/T29TPG_20220822T112119_image.tif"
    shapefile_path = "C:/Users/nacho/OneDrive - Universidad de Alcala/TFM/OneDrive_1_23-5-2024 (1)/BA_2022_NN/recorte1.shp"

    bandas_recortadas = recortar_bandas(image_path, shapefile_path)

    # Aquí puedes procesar las bandas recortadas como desees
    # Por ejemplo, puedes verificar las dimensiones de las bandas recortadas
    for banda, datos in bandas_recortadas.items():
        print(f"{banda}: dimensiones {datos.shape}")

if __name__ == "__main__":
    main()
