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
input_tif = "C:/Users/nacho/OneDrive - Universidad de Alcala/TFM/imagenes/812T.tif"

# Guardar las bandas 6, 7 y 8 en archivos separados
guardar_banda(input_tif, '812T_banda2.tif', 1)
guardar_banda(input_tif, '812T_banda3.tif', 2)
guardar_banda(input_tif, '812T_banda4.tif', 3)
guardar_banda(input_tif, '812T_banda5.tif', 4)
guardar_banda(input_tif, '812T_banda6.tif', 5)
guardar_banda(input_tif, '812T_banda7.tif', 6)
guardar_banda(input_tif, '812T_banda8.tif', 7)
guardar_banda(input_tif, '812T_banda8A.tif', 8)
guardar_banda(input_tif, '812T_banda9.tif', 9)
guardar_banda(input_tif, '812T_banda10.tif', 10)
guardar_banda(input_tif, '812T_banda11.tif', 11)
guardar_banda(input_tif, '812T_banda12.tif', 12)

print("Las bandas se han guardado correctamente.")
