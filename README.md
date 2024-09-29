# TFM
Evaluación de superficies de incendios mediante técnicas de Inteligencia Artificial

En 0rden.png están numeradas las 7 zonas de incendio que se van a estudiar. La zona 0 es uan zona de no incendio que se analizará para ver cómo varía de incendio a no incendio.

El archivo script.py contiene todo el código para representar la respuesta espectral y ver la información que nos aportan las bandas de las imágenes del Sentinel-2.

El código coge un .tiff en el elipsoide 25830, lo recorta según recorte.shp, extrae el valor de las 12 bandas para cada ROI (Puntos_Aleatorios_Incendios.shp). Luego calcula el valor máximo, mínimo y la media de los ROIs para cada banda y lo guarda en un png (respuesta_espectral). Este procedimiento se repite para las 7 zonas de incendio de un .tiff y para 3 .tiff distintos. Los 3 .tiff son de la misma zona pero a distintas horas.

Los resultados de la imágenes se guardan: respuesta_espectral_k_i.png. Siendo 'k' el .tiff (1, 2 ó 3) e 'i' la banda. Los _0 corresponden a la zona de no incendio. También se guarda en un .csv los valores medios de cada banda para cada incendio de cada imagen.

En pruebaZona2.py está para la zona2 únicamente y en pruebaNOincendio.py está para una zona donde no hay incendio. Se utilizaron para comprobaciones de código y errores.

Para verlo de manera más clara, en comparativa.png están los 4 incendios más grandes (1, 2, 4 y 5) junto con la zona de no incendio (la 0). De manera que cada fila es una de las 3 imágenes .tiff que hay y cada columna un incendio, siendo la primera columna la de no incendio.

Finalmente, en el .csv 'calculo' están los cálculos para justificar qué bandas seleccionar.  Se han escogido los 4 incendios más grandes y los valores medios de cada banda para los 3 .tiff. Lo primero, es hacer el promedio de valores de las bandas para los 4 incendios. A continuación, se hace la diferencia del promedio de cada banda en incendio con dicha banda en no incendio. Puesto que se tienen 3 imágenes .tiff, se hace el promedio de la diferencia de cada banda en las 3 imágenes .tiff para ver qué bandas son las que más difieren. El resultado son las bandas 6, 7 y 8.

En separacion_bandas.py está el código que separa las bandas 6,7 y 8 en un .tif cada una para poder abrirlas con ImageJ y poder comenzar con la segunda parte del proyecto.

La segunda parte del proyecto se basa en:
  - Combinación lineal de las capas seleccionadas.
  - Duplicar el resultado de la combinación lineal.
  - Aplicar a una el filtro exponencial y a la otra el filtro logarítmico.
  - Hacer la XOR entre el resultado de ambos filtros.

El resultado debería parecerse visualmente a la marca de incendios resaltada por expertos, de manera que este proceso sirva para entrenar una red neuronal.
