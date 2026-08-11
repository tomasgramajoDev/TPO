# Integraciones

Cada integración se documenta por separado y no debe darse por confirmada sin evidencia bilateral.

## Estados contractuales

| Estado | Uso |
| --- | --- |
| `PROPOSED` | Propuesta del equipo de Obras no acordada externamente. |
| `RECEIVED` | Comunicación de otro equipo pendiente de revisión o confirmación bilateral. |
| `AGREED` | Lógica y contrato acordados entre ambos grupos, aún sin confirmación técnica completa. |
| `CORE_PENDING` | Lógica funcional acordada; falta adaptar el contrato a las convenciones definitivas de Core. |
| `CONFIRMED` | Contrato funcional y técnico confirmado con evidencia. |

No hay contratos `CONFIRMED` en la información disponible.

## Fuente transversal recibida

El PO envió la matriz `Integraciones con Módulos`. Su contenido se registra como `RECEIVED`: acredita una definición comunicada por el PO, pero no reemplaza por sí solo la confirmación bilateral con M1, M2, M6, M7 o M9. Cuando difiere de una comunicación directa de un módulo, se conservan ambas versiones y se abre una decisión pendiente.

## Índice

- [Core Municipal](core.md)
- [Atención Ciudadana](atencion-ciudadana.md)
- [Ambiente, Higiene y Servicios Urbanos](ambiente-servicios-urbanos.md)
- [Tránsito](transito.md)
- [Ciudadanos y Expedientes Digitales](expedientes.md)

## Ficha mínima por evento

Cada contrato debe conservar: nombre funcional, nombre técnico, estado, emisor, consumidores, descripción, disparador, payload, obligatoriedad, correlación, acción del consumidor, respuestas derivadas, dudas y contexto del acuerdo.

Los campos de envelope (`eventId`, `eventType`, `occurredAt`, `source`, `version`, `correlationId`, `data`) pueden usarse únicamente como propuesta hasta que Core confirme sus nombres y semántica.
