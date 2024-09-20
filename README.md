# TFM
Evaluación de superficies de incendios mediante técnicas de Inteligencia Artificial

En 0rden.png están numeradas las 7 zonas de incendio que se van a estudiar. La zona 0 es uan zona de no incendio que se analizará para ver cómo varía de incendio a no incendio.

El archivo script.py contiene todo el código para representar la respuesta espectral y ver la información que nos aportan las bandas de las imágenes del Sentinel-2.

El código coge un .tiff en el elipsoide 25830, lo recorta según recorte.shp, extrae el valor de las 12 bandas para cada ROI (Puntos_Aleatorios_Incendios.shp). Luego calcula el valor máximo, mínimo y la media de los ROIs para cada banda y lo guarda en un png (respuesta_espectral). Este procedimiento se repite para las 7 zonas de incendio de un .tiff y para 3 .tiff distintos. Los 3 .tiff son de la misma zona pero a distintas horas.

Los resultados de la imágenes se guardan: respuesta_espectral_k_i.png. Siendo 'k' el .tiff (1, 2 ó 3) e 'i' la banda. Los _0 corresponden a la zona de no incendio.

En pruebaZona2.py está para la zona2 únicamente y en pruebaNOincendio.py está para una zona donde no hay incendio. Se utilizaron para comprobaciones de código y errores.

