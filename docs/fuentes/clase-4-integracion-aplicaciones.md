# Clase 4 — Integración de aplicaciones

## Estado de la fuente

- **Tipo:** material docente recibido.
- **Archivo:** `Clase04_Unidad_IV_Integracion_Aplicaciones.pptx`.
- **Contexto de incorporación:** aportado por el usuario el 2026-08-25.
- **Valor contractual:** contexto académico; no confirma contratos entre módulos ni obliga a elegir una tecnología concreta.
- **Observación:** la presentación contiene referencias internas a “Unidad IV”, “Clase 8” y 21/09/2026. Se conservan como metadatos del archivo, sin tratarlas como fecha efectiva de la clase.

## Criterios de selección explicados

La clase propone evaluar cada integración según el acoplamiento aceptable, la latencia tolerada, el volumen y frecuencia, la naturaleza de los sistemas, la necesidad de transacciones y quién inicia u orquesta la interacción.

| Tipo | Uso característico | Riesgo principal |
| --- | --- | --- |
| Archivos | Intercambio por lotes cuando no se necesita inmediatez. | Datos desactualizados entre corridas y errores de lote. |
| Procedural | Invocación directa y sincrónica para obtener una respuesta inmediata. | Acoplamiento temporal: la indisponibilidad remota bloquea la operación. |
| Datos | Acceso o esquema compartido como fuente única. | Alto acoplamiento al modelo y a sus migraciones. |
| Portales | Vista única sobre información proveniente de sistemas heterogéneos. | Unifica la presentación, pero no resuelve por sí sola la integración subyacente. |
| Procesos | Coordinación de una secuencia distribuida, normalmente asíncrona. | Fallos parciales, duplicados y necesidad de compensaciones y observabilidad. |

## Resolución de los cinco escenarios de MediConecta

| Escenario | Clasificación correcta | Criterio determinante |
| --- | --- | --- |
| Sincronización nocturna de afiliados | Archivos | Latencia tolerada y procesamiento batch. |
| Validación de cobertura al confirmar el turno | Procedural | Respuesta inmediata y sincrónica de un sistema externo. |
| Turnos y facturación comparten pacientes | Datos | Fuente única y acceso directo al mismo esquema. |
| Pantalla unificada para recepción | Portales | Integración en la capa de presentación. |
| Flujo posterior a telemedicina | Procesos | Orquestación asíncrona de varios pasos con posibles fallos parciales. |

La resolución completa con justificación y riesgo se conserva en `output/pdf/Actividad_Integracion_MediConecta_Resuelta.pdf`.
