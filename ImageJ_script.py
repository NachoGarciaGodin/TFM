from ij import IJ

# Obtener la ruta actual de trabajo
ruta_actual = IJ.getDirectory("current")

# Nombres de las bandas
banda6 = ruta_actual  + "/bandas_separadas/827T_banda6.tif"
banda7 = ruta_actual  + "/bandas_separadas/827T_banda7.tif"
banda8A = ruta_actual + "/bandas_separadas/827T_banda8A.tif"
banda3 = ruta_actual  + "/bandas_separadas/827T_banda3.tif"
banda9 = ruta_actual  + "/bandas_separadas/827T_banda9.tif"
banda12 = ruta_actual + "/bandas_separadas/827T_banda12.tif"

# Cargar las imágenes
imp6 = IJ.openImage(banda6)
imp7 = IJ.openImage(banda7)
imp8A = IJ.openImage(banda8A)
imp3 = IJ.openImage(banda3)
imp9 = IJ.openImage(banda9)
imp12 = IJ.openImage(banda12)

# # Verificar si las imágenes se han cargado correctamente

if imp3 is None:
    print("Error: No se pudo cargar la imagen " + banda3 + ".")
else:
    print("Imagen " + banda3 + " cargada correctamente.")

if imp7 is None:
    print("Error: No se pudo cargar la imagen " + banda7 + ".")
else:
    print("Imagen " + banda7 + " cargada correctamente.")

if imp6 is None:
    print("Error: No se pudo cargar la imagen " + banda6 + ".")
else:
    print("Imagen " + banda6 + " cargada correctamente.")

if imp8A is None:
    print("Error: No se pudo cargar la imagen " + banda8A + ".")
else:
    print("Imagen " + banda8A + " cargada correctamente.")

if imp9 is None:
    print("Error: No se pudo cargar la imagen " + banda9 + ".")
else:
    print("Imagen " + banda9 + " cargada correctamente.")

if imp12 is None:
    print("Error: No se pudo cargar la imagen " + banda12 + ".")
else:
    print("Imagen " + banda12 + " cargada correctamente.")

#  Realizar combinación lineal entre las bandas 6, 7 y 8A 
IJ.run(imp6, "Multiply...", "value=0.4")
IJ.run(imp7, "Multiply...", "value=0.4")
IJ.run(imp8A, "Multiply...", "value=0.2")

IJ.run(imp3, "Multiply...", "value=50")
IJ.run(imp9, "Multiply...", "value=50")
IJ.run(imp12, "Multiply...", "value=500")

#----- Operación 6+7+8A ------
IJ.run(imp6, "Add...", imp7.getTitle())
IJ.run(imp6, "Add...", imp8A.getTitle())
#IJ.run(imp6, "Subtract...", imp3.getTitle())
#IJ.run(imp6, "Subtract...", imp9.getTitle())
#IJ.run(imp6, "Subtract...", imp12.getTitle())


#  Guardar la combinación
combinacion = imp6
IJ.save(combinacion, "C:/Users/nacho/Documents/TFM/ImageJ/combinacion_lineal_827T.tif")

# Duplicar la combinación para aplicar diferentes filtros
logar = combinacion.duplicate()
exponencial = combinacion.duplicate()

# Aplicar filtro logarítmico a la primera imagen duplicada
IJ.run(logar, "Log", "")

# Guardar la imagen logarítmica
IJ.save(logar, "C:/Users/nacho/Documents/TFM/ImageJ/logaritmico_827T.tif")

# Aplicar filtro exponencial a la segunda imagen duplicada
IJ.run(exponencial, "Exp", "")

# Guardar la imagen exponencial
IJ.save(exponencial, "C:/Users/nacho/Documents/TFM/ImageJ/exponencial_827T.tif")

print("Proceso completado. Las imágenes han sido guardadas.")


