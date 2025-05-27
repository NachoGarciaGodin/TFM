# import geopandas as gpd

# # Cargar los shapefiles
# shp1 = gpd.read_file("ARCHIVO2.shp")  # ARCHIVO2: Verdad del experto
# shp2 = gpd.read_file("ARCHIVO.shp")  # ARCHIVO: Clasificación

# # Verificar si el CRS está definido para shp1
# if shp1.crs is None:
#     print("El CRS no está definido en shp1. Asignando CRS...")
#     shp1 = shp1.set_crs("EPSG:25830")  # Cambia EPSG:25830 al CRS correcto para tu shapefile

# # Verificar si el CRS está definido para shp2
# if shp2.crs is None:
#     print("El CRS no está definido en shp2. Asignando CRS...")
#     shp2 = shp2.set_crs("EPSG:25830")  # Cambia EPSG:25830 si es necesario

# # Asegurarse de que ambos shapefiles tengan la misma proyección
# shp2 = shp2.to_crs(shp1.crs)

# # Calcular la intersección (True Positives)
# intersect = gpd.overlay(shp2, shp1, how='intersection')
# intersect['intersect_area'] = intersect.geometry.area  # Área de solapamiento

# # Calcular falsos positivos (False Positives)
# false_positives = gpd.overlay(shp2, shp1, how='difference')
# false_positives['false_positive_area'] = false_positives.geometry.area

# # Calcular falsos negativos (False Negatives)
# false_negatives = gpd.overlay(shp1, shp2, how='difference')
# false_negatives['false_negative_area'] = false_negatives.geometry.area

# # Calcular áreas totales
# total_area_shp1 = shp1.geometry.area.sum()  # Total de ARCHIVO
# total_area_shp2 = shp2.geometry.area.sum()  # Total de ARCHIVO2
# total_tp_area = intersect['intersect_area'].sum()  # True Positives (área de intersección)
# total_fp_area = false_positives['false_positive_area'].sum()  # False Positives
# total_fn_area = false_negatives['false_negative_area'].sum()  # False Negatives

# # Calcular porcentajes
# tp_percentage = (total_tp_area / total_area_shp2) * 100 if total_area_shp2 > 0 else 0  # TP como % de ARCHIVO2
# fp_percentage = (total_fp_area / total_area_shp1) * 100 if total_area_shp1 > 0 else 0  # FP como % de ARCHIVO
# fn_percentage = (total_fn_area / total_area_shp2) * 100 if total_area_shp2 > 0 else 0  # FN como % de ARCHIVO2

# # Métricas
# recall = tp_percentage  # Recall: TP como % de ARCHIVO2
# precision = (total_tp_area / (total_tp_area + total_fp_area)) * 100 if (total_tp_area + total_fp_area) > 0 else 0  # Precisión

# # Calcular el F1 Score
# f1_score = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

# # Resultados
# print(f"Área total de ARCHIVO (clasificación): {total_area_shp1:.2f}")
# print(f"Área total de ARCHIVO2 (verdad): {total_area_shp2:.2f}")
# print(f"True Positives (TP): {tp_percentage:.2f}% (porcentaje de ARCHIVO detectado como incendio correctamente)")
# print(f"False Positives (FP): {fp_percentage:.2f}% (porcentaje de ARCHIVO clasificado erróneamente como incendio)")
# print(f"False Negatives (FN): {fn_percentage:.2f}% (porcentaje de ARCHIVO2 no detectado como incendio)")
# print(f"Recall (detección correcta): {recall:.2f}%")
# print(f"Precisión (acierto en predicción): {precision:.2f}%")
# print(f"F1 Score (balance entre precisión y recall): {f1_score:.2f}")


#######################################
######################################


######################################
######################################



import geopandas as gpd
import pandas as pd

# Cargar los shapefiles
shp1 = gpd.read_file("ARCHIVO2.shp")  # ARCHIVO2: Verdad del experto
shp2 = gpd.read_file("ARCHIVO.shp")  # ARCHIVO: Clasificación

# Verificar si el CRS está definido para shp1
if shp1.crs is None:
    print("El CRS no está definido en shp1. Asignando CRS...")
    shp1 = shp1.set_crs("EPSG:25830")  # Cambia EPSG:25830 al CRS correcto para tu shapefile

# Verificar si el CRS está definido para shp2
if shp2.crs is None:
    print("El CRS no está definido en shp2. Asignando CRS...")
    shp2 = shp2.set_crs("EPSG:25830")  # Cambia EPSG:25830 si es necesario

# Asegurarse de que ambos shapefiles tengan la misma proyección
shp2 = shp2.to_crs(shp1.crs)

# Calcular la intersección (True Positives)
intersect = gpd.overlay(shp2, shp1, how='intersection')
intersect['intersect_area'] = intersect.geometry.area  # Área de solapamiento

# Calcular falsos positivos (False Positives)
false_positives = gpd.overlay(shp2, shp1, how='difference')
false_positives['false_positive_area'] = false_positives.geometry.area

# Calcular falsos negativos (False Negatives)
false_negatives = gpd.overlay(shp1, shp2, how='difference')
false_negatives['false_negative_area'] = false_negatives.geometry.area

# Calcular áreas totales
total_area_shp1 = shp1.geometry.area.sum()  # Total de ARCHIVO
total_area_shp2 = shp2.geometry.area.sum()  # Total de ARCHIVO2
total_tp_area = intersect['intersect_area'].sum()  # True Positives (área de intersección)
total_fp_area = false_positives['false_positive_area'].sum()  # False Positives
total_fn_area = false_negatives['false_negative_area'].sum()  # False Negatives

# Calcular porcentajes de FP y FN
fp_percentage = (total_fp_area / total_area_shp1) * 100 if total_area_shp1 > 0 else 0
fn_percentage = (total_fn_area / total_area_shp1) * 100 if total_area_shp1 > 0 else 0

# Métricas
recall = (total_tp_area / (total_tp_area + total_fn_area)) * 100 if (total_tp_area + total_fn_area) > 0 else 0  # Recall
precision = (total_tp_area / (total_tp_area + total_fp_area)) * 100 if (total_tp_area + total_fp_area) > 0 else 0  # Precisión

# Calcular el F1 Score
f1_score = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

# Matriz de Confusión
conf_matrix = pd.DataFrame({
    "Predicción Sí": [total_tp_area, total_fp_area],
    "Predicción No": [total_fn_area, "N/A"]
}, index=["Real Sí", "Real No"])

# Resultados
print(f"Área total de ARCHIVO (clasificación): {total_area_shp1:.2f}")
print(f"Área total de ARCHIVO2 (verdad): {total_area_shp2:.2f}")
print(f"Acertados en Archivo vs los reales del experto (TP): {total_tp_area:.2f}")
print(f"De más en Archivo vs los reales del experto (FP): {total_fp_area:.2f} ({fp_percentage:.2f}%)")
print(f"Expertos dicen que sí y Archivo dice que no (FN): {total_fn_area:.2f} ({fn_percentage:.2f}%)")
print(f"Recall (detección correcta): {recall:.2f}%")
print(f"Precisión (acierto en predicción): {precision:.2f}%")
print(f"F1 Score (balance entre precisión y recall): {f1_score:.2f}%")

print("\nMatriz de Confusión:")
print(conf_matrix)
