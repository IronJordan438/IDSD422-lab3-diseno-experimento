# Plantilla de protocolo — Experimento de ubicación de producto

**Equipo:** 1 · **Integrantes:** Jordan Sangucho · **Fecha:** 27/10/2026

Completa cada sección. Usa commits por sección; la historia del repositorio se revisa.

## 1. Pregunta e hipótesis

El producto  en el pasillo principal vende mas en promedio que su ubicación habitual en ventas
semanales durante 4 semanas
- **Pregunta de investigación:** ¿Cambiar la ubicación del producto estrella desde su góndola habitual hacia el pasillo principal aumenta sus ventas semanales promedio en las tiendas de RetailAndina S.A. durante un período de 4 semanas?
- **Hipótesis nula (H 0):** El promedio de ventas semanales (en unidades vendidas y dólares) del producto estrella ubicado en el pasillo principal es igual o menor al promedio de ventas semanales en su ubicación habitual (pasillo\_principal) (habitual) durante las 4 semanas de evaluación.
- **Hipótesis alternativa (H 1):** El promedio de ventas semanales del producto estrella ubicado en el pasillo principal es significativamente mayor que el promedio de ventas semanales en su ubicación habitual (pasillo\_principal) > (habitual) durante las 4 semanas de evaluación.

## 2. Unidad experimental

*¿Qué recibe el tratamiento? ¿Cuántas unidades se incluyen?*

- Unidad: La combinación semana-tienda (observación semanal de cada sucursal bajo una ubicación asignada), organizada bajo un diseño cruzado (crossover) donde cada tienda recibe ambas condiciones en semanas alternas. 
- Número de Unidades y Justificación: Se incluyen 10 tiendas evaluadas durante 4 semanas, generando N = 40 unidades experimentales (semana-tienda) (20 en pasillo_principal y 20 en habitual). Al alternar la ubicación por semana dentro de cada tienda, cada sucursal actúa como su propio control, eliminando la variabilidad entre ciudades y reduciendo drásticamente el error estándar con menos tiendas operativas.

## 3. Factor, niveles y tratamiento

- **Factor** (variable manipulada): Ubicación física de exhibición del producto estrella dentro de la tienda (`ubicacion`).
- **Niveles** (valores del factor):
- 1. `pasillo_principal` (cabecera o isla de alto tráfico en el corredor central).
  2. `habitual` (góndola o estantería estándar de su categoría).
- **Tratamiento** (combinación asignada): Asignación activa de la exhibición del producto estrella en el nivel **`pasillo_principal`** durante 4 semanas completas sin alterar su precio ni su empaque. El nivel `habitual` corresponde a la condición de control (ausencia de intervención).

## 4. Grupo de control

*¿Cuál es la referencia sin tratamiento y qué rol cumple?*
Son las 20 observaciones semana-tienda en las que el producto permanece en su ubicación habitual (2 semanas por cada una de las 10 tiendas), funcionando como control interno pareado para cada sucursal.

## 5. Aleatorización

*¿Cómo se asignan las unidades a los grupos? ¿Por qué es necesaria?*
Se utiliza una aleatorización de la secuencia inicial mediante generador con semilla fija (np.random.default_rng(1234597)). Para cada una de las 10 tiendas se sortea al azar si inicia en la semana 1 en pasillo_principal (secuencia pasillo–habitual–pasillo–habitual) o en habitual (secuencia habitual–pasillo–habitual–pasillo). Este sorteo evita sesgos de selección y equilibra factores temporales desconocidos (como efecto quincena o aprendizaje del consumidor) entre ambos órdenes de exposición.


- **Línea de código de la asignación (Python o R):** escribe el comando que asigna al azar tus N unidades a los dos grupos (tratamiento y control) y ejecútalo con semilla. Incluye el resultado de una corrida y explica por qué el sorteo reparte los factores desconocidos entre los grupos.
- Linea de codigo vista en clases

```python
# Diseño del Experimento
import json
import pandas as pd
import numpy as np
from scipy import stats

tiendas = [
    "Quito Norte", "Quito Sur", "Guayaquil Centro", "Guayaquil Norte",
    "Cuenca Centro", "Cuenca Sur", "Ambato Centro", "Manta", "Loja", "Machala"
]
semanas = [1, 2, 3, 4]

# Sorteo de la condición inicial
rng = np.random.default_rng(1234597)
primera = rng.choice(["pasillo_principal", "habitual"], size=len(tiendas))

filas = []
for tienda, cond in zip(tiendas, primera):
    otra = "habitual" if cond == "pasillo_principal" else "pasillo_principal"
    for s in semanas:
        filas.append({
            "tienda": tienda,
            "semana": s,
            "ubicacion": cond if s % 2 == 1 else otra
        })

# print(json.dumps(filas))

diseno = pd.DataFrame(filas)
# print(diseno)

# Simulación de la Ejecución
rng = np.random.default_rng(1234598)

efecto_tienda = dict(zip(tiendas, rng.normal(1100, 120, len(tiendas))))
# print(efecto_tienda)

efecto_semana = {1: 0, 2: 30, 3: 60, 4: 90}
diseno["ventas_producto"] = (
    diseno["tienda"].map(efecto_tienda) +
    diseno["semana"].map(efecto_semana) +
    (diseno["ubicacion"] == "pasillo_principal") * 220 +
    rng.normal(0, 90, len(diseno))
).round(0).astype(int)

print(diseno)

# Promoción Simultánea Registrada
diseno["promocion_simultanea"] = "no"

diseno.loc[
    (diseno["tienda"] == "Guayaquil Centro") & (diseno["semana"] == 1),
    "promocion_simultanea"
] = "si"
diseno.loc[diseno["promocion_simultanea"] == "si", "ventas_producto"] += 180

diseno.to_csv("resultado_simulacion.csv", index=False)

# Análisis Pareado: Una Fila por Tienda con sus Condiciones
piv = diseno.groupby(["tienda", "ubicacion"])["ventas_producto"].mean().unstack()
piv["diferencia"] = piv["pasillo_principal"] - piv["habitual"]

media = piv["diferencia"].mean()
dev = piv["diferencia"].std(ddof=1)

print(media)
print(dev)
n = len(piv)

t_crict = stats.t.ppf(0.975, df=9)
# print(t_crict)
ic_inf = media - (t_crict * dev / n**0.5)
ic_sup = media + (t_crict * dev / n**0.5)
print(ic_inf)
print(ic_sup)

# Independiente del número de veces que se corra el experimento,
# podemos decir que con un 95% de certeza el valor promedio de la
# diferencia de ventas del producto entre el pasillo principal y el habitual
# va a caer en el rango:
print(f"IC 95%: [{ic_inf}, {ic_sup}]")

# Prueba p-value
prueba = stats.ttest_rel(piv["pasillo_principal"], piv["habitual"])
print(f"Prueba t: {prueba.pvalue:.10f}")

```

| tienda | semana | ubicacion | ventas_producto |
| :--- | :---: | :--- | :---: |
| Quito Norte | 1 | habitual | 979 |
| Quito Norte | 2 | pasillo_principal | 1380 |
| Quito Norte | 3 | habitual | 1055 |
| Quito Norte | 4 | pasillo_principal | 1259 |
| Quito Sur | 1 | pasillo_principal | 1158 |
| Quito Sur | 2 | habitual | 978 |
| Quito Sur | 3 | pasillo_principal | 1359 |
| Quito Sur | 4 | habitual | 1058 |
| Guayaquil Centro | 1 | habitual | 1227 |
| Guayaquil Centro | 2 | pasillo_principal | 1569 |
| Guayaquil Centro | 3 | habitual | 1326 |
| Guayaquil Centro | 4 | pasillo_principal | 1668 |
| Guayaquil Norte | 1 | pasillo_principal | 1331 |
| Guayaquil Norte | 2 | habitual | 1027 |
| Guayaquil Norte | 3 | pasillo_principal | 1377 |
| Guayaquil Norte | 4 | habitual | 1169 |
| Cuenca Centro | 1 | pasillo_principal | 1182 |
| Cuenca Centro | 2 | habitual | 1103 |
| Cuenca Centro | 3 | pasillo_principal | 1330 |
| Cuenca Centro | 4 | habitual | 1186 |
| Cuenca Sur | 1 | habitual | 1211 |
| Cuenca Sur | 2 | pasillo_principal | 1298 |
| Cuenca Sur | 3 | habitual | 1244 |
| Cuenca Sur | 4 | pasillo_principal | 1603 |
| Ambato Centro | 1 | habitual | 1020 |
| Ambato Centro | 2 | pasillo_principal | 1063 |
| Ambato Centro | 3 | habitual | 1123 |
| Ambato Centro | 4 | pasillo_principal | 1158 |
| Manta | 1 | habitual | 966 |
| Manta | 2 | pasillo_principal | 1399 |
| Manta | 3 | habitual | 1095 |
| Manta | 4 | pasillo_principal | 1427 |
| Loja | 1 | habitual | 991 |
| Loja | 2 | pasillo_principal | 1332 |
| Loja | 3 | habitual | 1064 |
| Loja | 4 | pasillo_principal | 1427 |
| Machala | 1 | pasillo_principal | 1194 |
| Machala | 2 | habitual | 1071 |
| Machala | 3 | pasillo_principal | 1424 |
| Machala | 4 | habitual | 1071 |
239.7
102.39471557545231
166.45123307638835
312.94876692361163
IC 95%: [166.45123307638835,312.94876692361163]
Prueba t:  0.0000409166
  
## 6. Respuesta y medición
- Variable respuesta: ventas_producto, medida como el total de unidades vendidas (y su equivalente monetario neto en USD) del producto estrella por tienda en cada semana.
- Período de medición: 4 semanas para capturar ciclos completos de compra semanal y quincenal.
- Quién registra y cómo (¿ciego?): Los datos se extraen automáticamente desde el sistema centralizado por el equipo de Business Intelligence.

## 7. Factores a controlar (mínimo 4)

| Factor a controlar | Cómo se controla o registra |
|---|---|
| 1. Promociones simultáneas | Con un control estricto y registros se prohibirá aplicarle al producto estrella descuentos y ofertas. Si una sucursal aplica una promoción por error se registra como `'si'` en el CSV para filtrar o ajustar el sesgo (+180 unidades) en el análisis.|
| 2. Efecto basal de tienda y ciudad | Bloqueo intra-tienda evaluando las 10 tiendas en ambos niveles (pasillo principal y habitual), en semanas alternas, cada sucursal actúa como su propio control, para neutralizar diferencias estructurales de ventas base entre ciudades|
| 3. Tendencia temporal por semana | Con contrapeso al sortear al azar que tiendas empiezan en `pasillo_principal` y cuáles en `habitual` asi amabs ubicaciones aparecen en semanas impares como en pares equilibrando el efecto del calendario |
| 4. Día y hora exacta de reubicación semanal | Con un protocolo operativo estandarizado debido a que en cada semana se va a alternar la ubicación el cambio físico entre la góndola habitual y el pasillo principal debe realizarse estrictamente el domingo por la noche tras el cierre de caja, evitando que una semana mezcle días de ambas ubicaciones.|

## 8. Limitaciones del diseño

*¿Qué podría invalidar el experimento si no se controla? ¿Qué no se podrá concluir?*
Los factores que podrían invalidar el experimento serian:
- Efecto de  Arrastre: Al cambiar la ubicación del producto semanalmente, los clientes que lo vieron en el pasillo principal podrían biscarlo intencionalmente en el habitual, atenuando la diferencia real.
- Costo Operativo de la Reubicación Semanal: Se requiere un orden estricto del personal de la tienda al retirar el producto y rehubicarlo para no contaminar la medición semanal.
- Promociones Simultaneas no Controladas: Si una tienda activa una promoción simultanea, sesga al alza el promedio de esa condición si no se filtra o modela.

## 9. Comparación en código (Python/R)

*Escribe `scripts/comparacion_experimento.py` (o `.R`): debe cargar `plantillas/registro_experimento.csv` y calcular el promedio de `ventas_producto` por `ubicacion`. Incluye la salida y responde:*
```python
import pandas as pd

df = pd.read_csv("plantillas/registro_experimento.csv")

promedio_ventas = df.groupby("ubicacion")["ventas_producto"].mean()
print("Promedio de ventas por ubicación:")
print(promedio_ventas)
print("-" * 40)

conteo_grupos = df["ubicacion"].value_counts()
print("Número de registros por grupo:")
print(conteo_grupos)
```

-Salidas
| ubicacion | promedio_ventas |
| :--- | :---: |
| habitual | 1040.0 |
| pasillo_principal | 1335.0 |

| ubicacion | count |
| :--- | :---: |
| pasillo_principal | 2 |
| habitual | 2 |

- ¿Qué grupo muestra mayor venta promedio en la plantilla?
  * El grupo pasillo_principal muestra un promedio mayor con 1335.0 unidades/ventas frente a 1040.0 del grupo habitual (una diferencia aparente de +295.0).
- ¿Por qué con 4 filas no se puede concluir nada sobre el efecto de la ubicación?
  * Porque con apenas 4 observaciones (2 tiendas por grupo en una sola semana) la muestra carece de potencia estadística para distinguir un efecto real de la simple variación aleatoria entre tiendas.
- Si el experimento se ejecutara con tu protocolo, ¿qué le faltaría a este análisis para ser justo?
  Con los protocolos del experimento lo que faltaría en el experimento es:  
  * Completar el tamaño muestral del diseño: El scrip básico solo evalúa 4 filas, mientras que el del protocolo requiere las 40 observaciones de las 4 semanas    evaluadas
  * Aplicar un análisis pareado intra-tienda en lugar de un promedio global simple: Como cada tienda prueba ambas ubicaciones en semanas alternas, l análisis debe agrupar tienda y ubicacion (piv = diseno.groupby(["tienda", "ubicacion"])["ventas_producto"].mean().unstack()) para calcular la **diferencia dentro de cada tienda** (pasillo_principal - habitual), bloqueando así el efecto basal de cada sucursal.
  * Filtrar o ajustar las promociones simultáneas:
  Incluir inferencia estadística: Calcular únicamente la media no basta para tomar decisiones gerenciales; falta evaluar la variabilidad entre tiendas mediante una prueba t pareada (scipy.stats.ttest_rel) y calcular su **intervalo de confianza al 95%** para confirmar si la diferencia promedio observada es estadísticamente significativa frente al azar.
