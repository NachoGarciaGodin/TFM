# TFM
Evaluación de superficies de incendios mediante técnicas de Inteligencia Artificial

En 0rden.png están numeradas las zonas.
script.py contiene todo el código para representar la respuesta espectral y ver la información que nos aportan las bandas de las imágenes del Sentinel-2.

El código coge un .tiff en el elipsoide 25830, lo recorta según recorte.shp, extrae el valor de las 12 bandas para cada ROI (puntos.shp). Luego calcula el valor mázimo, mínimo y la media y lo muestra. Este procedimiento se repite para las 7 zonas de incendio de un .tiff y para 3 .tiff distintos. Los 3 .tiff son de la misma zona pero a distintas horas.

Los resultados de la imágenes se guardan: respuesta_espectral_k_i.png. Siendo 'k' el .tiff (1,2 o 3) e 'i' la banda.
