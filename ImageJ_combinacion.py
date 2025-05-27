from ij import IJ

# Ruta de las imágenes y carpeta de salida
imagenes_folder = "C:/Users/nacho/Documents/TFM/imagenes/buenas/"
bandas_folder = imagenes_folder + "bandas_separadas/"
output_folder = "C:/Users/nacho/Documents/TFM/imagenes/buenas/combinacion_lineal/"

# Nombres de las imágenes
imagenes = ["29TPG", "29TPH", "30SXJ", "30SYJ", "628", "812T", "822T", "827T", "T29TNF_20171027T112139_image", "T29TPF_20171027T112139_image" ]

# Función para realizar la combinación lineal
def combinacion_lineal(base_name):
    # Nombres de las bandas
    banda6 = bandas_folder + base_name + "_banda6.tif"
    banda7 = bandas_folder + base_name + "_banda7.tif"
    banda8A = bandas_folder + base_name + "_banda8A.tif"
    
    # Cargar las bandas
    imp6 = IJ.openImage(banda6)
    imp7 = IJ.openImage(banda7)
    imp8A = IJ.openImage(banda8A)

    # Realizar la multiplicación de cada banda por su coeficiente
    IJ.run(imp6, "Multiply...", "value=0.4")
    IJ.run(imp7, "Multiply...", "value=0.4")
    IJ.run(imp8A, "Multiply...", "value=0.2")

    # Realizar la suma de las bandas multiplicadas
    IJ.run(imp6, "Add...", imp7.getTitle())
    IJ.run(imp6, "Add...", imp8A.getTitle())

    # Guardar la imagen combinada
    output_path = output_folder + base_name + "_combinacion_lineal.tif"
    IJ.save(imp6, output_path)
    print("Combinación lineal guardada: " + output_path)

# Procesar todas las imágenes específicas
for imagen in imagenes:
    combinacion_lineal(imagen)

print("Proceso completado. Las imágenes han sido guardadas.")
