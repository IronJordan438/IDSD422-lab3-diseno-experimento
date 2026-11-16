# comparacion_experimento.R — Comparación de grupos (R)
# Completa los pasos marcados con TODO. Ejecuta desde la raíz del repositorio:
#   Rscript scripts/comparacion_experimento.R

# TODO 1: carga plantillas/registro_experimento.csv (read.csv)
datos <- read.csv("plantillas/registro_experimento.csv")

# TODO 2: calcula e imprime el promedio de ventas_producto por ubicacion
#         (aggregate)
promedio_ventas <- aggregate(ventas_producto ~ ubicacion, data = datos, FUN = mean)
cat("Promedio de ventas por ubicación:\n")
print(promedio_ventas)
cat("----------------------------------------\n")

# TODO 3: imprime el número de registros por grupo (table)
conteo_grupos <- table(datos$ubicacion)
cat("Número de registros por grupo:\n")
print(conteo_grupos)
cat("----------------------------------------\n")

# TODO 4: escribe 2–3 líneas de interpretación (sección 9 de la plantilla):
#         por qué con 4 filas no se puede concluir y qué le faltaría al análisis
cat("Interpretación:\n")
cat("Aunque el promedio en 'pasillo_principal' (1335) supera al de 'habitual' (1040), con apenas 4 observaciones\n")
cat("(2 por grupo) no existe potencia estadística para asegurar que la diferencia no se deba al azar.\n")
cat("Además, 'Guayaquil Centro' tuvo una promoción simultánea que sesga el resultado al alza. Para validar\n")
cat("el experimento falta ampliar la muestra, medir múltiples semanas (con línea base previa) y aislar promociones.\n")

