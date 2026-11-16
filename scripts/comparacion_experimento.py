# comparacion_experimento.py — Comparación de grupos (Python)
# Completa los pasos marcados con TODO. Ejecuta desde la raíz del repositorio:
#   python scripts/comparacion_experimento.py

# TODO 1: carga plantillas/registro_experimento.csv con pandas
import pandas as pd
df = pd.read_csv("plantillas/registro_experimento.csv")

# TODO 2: calcula e imprime el promedio de ventas_producto por ubicacion
promedio_ventas = df.groupby("ubicacion")["ventas_producto"].mean()
print("Promedio de ventas por ubicación:")
print(promedio_ventas)
print("-" * 40)

# TODO 3: imprime el número de registros por grupo (value_counts)
conteo_grupos = df["ubicacion"].value_counts()
print("Número de registros por grupo:")
print(conteo_grupos)
print("-" * 40)

# TODO 4: escribe 2–3 líneas de interpretación (sección 9 de la plantilla):
#         por qué con 4 filas no se puede concluir y qué le faltaría al análisis
interpretacion = """
Interpretación:
Aunque el pasillo principal muestra un promedio mayor (1335.0 frente a 1040.0), con solo 4 registros 
(2 por grupo) la muestra es demasiado pequeña para tener validez estadística y descartar el azar. 
Además, existe una variable de confusión: la tienda 'Guayaquil Centro' tuvo una promoción simultánea ('si'), 
lo que infla las ventas del grupo 'pasillo_principal'. Para concluir con rigor se necesitarían más tiendas, 
mediciones durante varias semanas (incluyendo una línea base previa) y controlar factores externos como promociones o tamaño de tienda.
"""
print(interpretacion)

