import rasterio

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

# Archivo de entrada (modifica con la ruta de tu archivo .tif)
input_tif = "C:/Users/nacho/OneDrive - Universidad de Alcala/TFM/imagenes/827T.tif"

# Guardar las bandas 6, 7 y 8 en archivos separados
guardar_banda(input_tif, '827T_banda6.tif', 6)
guardar_banda(input_tif, '827T_banda7.tif', 7)
guardar_banda(input_tif, '827T_banda8.tif', 8)

print("Las bandas se han guardado correctamente.")
