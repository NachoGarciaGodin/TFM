import os
import rasterio

# Ruta de la carpeta que contiene las imágenes
input_folder = "C:/Users/nacho/Documents/TFM/imagenes/buenas/"
output_folder = os.path.join(input_folder, "bandas_separadas")

# Asegurarse de que la carpeta de salida existe
os.makedirs(output_folder, exist_ok=True)

# Mapeo de nombres de bandas para distintos números de bandas
band_names_by_count = {
    12: ["1", "2", "3", "4", "5", "6", "7", "8A", "9", "10", "11", "12"],
    13: ["1", "2", "3", "4", "5", "6", "7", "8", "8A", "9", "10", "11", "12"],
    11: ["1", "2", "3", "4", "5", "6", "7", "8A", "11", "12", "SCL"]
}

# Función para guardar una banda específica en un nuevo archivo .tif
def guardar_banda(input_tif, output_tif, band_number):
    with rasterio.open(input_tif) as src:
        # Leer la banda específica
        banda = src.read(band_number)

        # Crear un nuevo archivo .tif con la banda seleccionada
        profile = src.profile
        profile.update(count=1)  # Solo hay una banda en el nuevo archivo

        with rasterio.open(output_tif, 'w', **profile) as dst:
            dst.write(banda, 1)

# Procesar cada archivo en la carpeta de entrada
for filename in os.listdir(input_folder):
    if filename.endswith(".tif"):
        input_path = os.path.join(input_folder, filename)

        with rasterio.open(input_path) as src:
            # Obtener la cantidad de bandas
            num_bands = src.count

            # Determinar los nombres de bandas para este archivo
            band_names = band_names_by_count.get(num_bands, None)
            if band_names is None:
                print(f"Advertencia: la imagen {filename} tiene un número no estándar de bandas ({num_bands}). Se omitirá.")
                continue

            # Informar sobre las bandas de la imagen
            band_list_str = ", ".join(band_names)
            print(f"La imagen {filename} tiene {num_bands} bandas: {band_list_str}.")

            # Guardar cada banda con su nombre específico
            for band_number, band_name in enumerate(band_names, start=1):
                output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_banda{band_name}.tif")
                guardar_banda(input_path, output_path, band_number)

print("Las bandas se han guardado correctamente en la carpeta 'bandas_separadas'.")
