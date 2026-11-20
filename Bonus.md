# Plantilla Bonus — Adaptación del diseño a un ensayo clínico (Vacuna)

**Equipo:** 1 · **Integrantes:** Jordan Sangucho · **Fecha:** 27/10/2026

1. **Pregunta e hipótesis:**
   - **Pregunta:** ¿La administración de la vacuna experimental reduce la incidencia de infección sintomática en comparación con un placebo durante
     un seguimiento de 6 meses?
   - **Hipótesis nula (H_0):** La proporción de participantes que desarrollan infección sintomática en el grupo vacunado es igual o
     mayor que en el grupo placebo {vacuna}{placebo}.
   - **Hipótesis alternativa (H_1):** La proporción de infección sintomática en el grupo vacunado es significativamente menor que en el
     grupo placebo {vacuna} < {placebo}.

2. **Unidad Experimental:**
   - **Unidad:** Cada **participante voluntario sano** inscrito en el estudio. *(Nota: A diferencia del diseño cruzado en tiendas, aquí no se puede
     alternar el tratamiento en un mismo sujeto porque la inmunización es irreversible; por ello se emplea un diseño de grupos paralelos).*
   - **Tamaño muestral (N):** N = 200$ voluntarios ($100$ asignados al grupo de vacuna y $100$ al grupo de control) distribuidos en las mismas ciudades
     del estudio comercial (Quito, Guayaquil, Cuenca, etc.) para garantizar potencia estadística y representatividad poblacional.

3. **Factor, niveles y tratamiento:**
   - **Factor (variable manipulada):** Intervención inmunológica administrada (`intervencion`).
   - **Niveles:** `vacuna_experimental` y `placebo` (solución salina estéril de apariencia idéntica).
   - **Tratamiento:** Aplicación intramuscular de la dosis activa de la **`vacuna_experimental`** según el esquema establecido.

4. **Grupo de control:**
   - **Definición y rol:** Los $100$ participantes que reciben el **`placebo`**. Cumplen el rol de línea base contemporánea para medir la tasa natural
     de contagio en la población durante los 6 meses y neutralizar el efecto psicológico de recibir una inyección (efecto placebo) o cambios
     en el comportamiento preventivo de los voluntarios.

5. **Aleatorización (con código y semilla):**
   - **Método y justificación:** Se utiliza asignación aleatoria balanceada mediante código con la misma semilla fija (`np.random.default_rng(1234597)`) para
     repartir factores desconocidos (inmunidad previa no detectada, genética o exposición diaria al virus) equitativamente entre ambos grupos, evitando el sesgo
     de selección médica.
   ```python
   import numpy as np
   import pandas as pd

   rng = np.random.default_rng(1234597)
   participantes = [f"P{i:03d}" for i in range(1, 201)]
   vacunados = rng.choice(participantes, size=100, replace=False)

   ensayo = pd.DataFrame({
       "participante": participantes,
       "grupo": ["vacuna_experimental" if p in vacunados else "placebo" for p in participantes]
   })
   print(ensayo["grupo"].value_counts())
   ```

6. **Respuesta y Medición **
   - Variable respuesta: infeccion_confirmada (variable binaria si/no).
   - Período de medición: 6 meses (24 semanas) posteriores a la última dosis.
   - Registro y ciego: aquí se aplica doble ciego: ni el participante ni el personal médico que administra la dosis o evalúa los síntomas saben si el código
   - asignado corresponde a vacuna_experimental o placebo, evitando sesgos en el reporte de síntomas.
  
7. **Factores a Controlar **

| Factor a controlar | Cómo se controla o registra |
| :--- | :--- |
| **1. Edad y comorbilidades** | Se estratifica o restringe el ingreso a adultos de 18 a 65 años sin inmunosupresión, registrando edad e historial clínico. |
| **2. Exposición geográfica** | Se bloquea por ciudad de residencia (Quito, Guayaquil, Cuenca) para evitar que un brote local afecte desproporcionadamente a un solo grupo. |
| **3. Cumplimiento del esquema** | Registro estricto de fechas de vacunación; quienes no completan las dosis en el plazo estipulado se documentan en notas. |
| **4. Almacenamiento y cadena de frío** | Control continuo de temperatura de los viales para evitar pérdida de eficacia por manipulación. |

8. **Limitaciones del Diseño**
- Perdida de seguimiento: El abandono voluntario de los pacientes durante los 6 meses, puede reducir las estadísticas entre grupos.
- Variabilidad en la Exposicision Real: No se puede obligar a todos los participantes a mantener exactamente el mismo nivel de contacto social.
- Validez Externa: Los resultados aplican al rango de edad evaluado y a las variantes circulantes durante esos 6 meses, sin garantizar la misma eficacia en
  niños, adultos mayores o futuras mutaciones.
       

