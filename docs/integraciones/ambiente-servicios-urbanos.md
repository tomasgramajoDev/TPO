# Integración con Ambiente, Higiene y Servicios Urbanos — Módulo 6

## Estado general

**Estado de los recorridos probados:** `CONFIRMED` por M3, M6 y Core.

El contrato activo usa `infrastructureRepairRequested`, `containerDamaged` y `treeRiskDetected` desde M6, y `workOrderScheduled`/`workOrderCompleted` desde M3. Los nombres históricos `urbanServiceRepairRequested` y `urbanRiskDetected` quedan como antecedentes del material del PO y no sustituyen el acuerdo directo probado.

## Circuito principal de reparación — 2026-11-05

- M6 publicó `infrastructureRepairRequested` con `eventId=a53fc8ee-5200-4949-b333-480f21be7e5d`.
- Core lo registró `ROUTED` y lo entregó a `q.obras`; M3 confirmó recepción y creó la orden asociada.
- M3 conservó `data.requestId` como `sourceRequestId` y publicó `workOrderScheduled` (`8d109cc9-1802-4b30-89ea-0dd9df8b1843`) y `workOrderCompleted` (`916449bf-9cfb-4449-ae74-65b9825f7693`).
- Los tres eventos conservaron el mismo `correlationId`; Core confirmó el enrutamiento, colas sin pendientes y DLQ vacía.
- M6 confirmó la solicitud cerrada después de procesar los eventos de M3.

El `workOrderId` transportado es UUID técnico y `workOrderNumber` es una referencia humana opcional. `workOrderCompleted` usa `outcome` y `attachments[]`; no se lo presenta como equivalente a la validación interna posterior de la orden.

## Eventos secundarios — 2026-11-14

### `containerDamaged`

- `eventId=748caf0e-6b47-4f35-998c-d1b77b8a1556`.
- M3 lo procesa únicamente cuando `requiresPublicWorks=true`.
- Core confirmó `ROUTED` y entrega `DELIVERED` a `q.obras` en un intento, sin retry ni dead letter; M3 confirmó su procesamiento funcional.
- M6 republicó exactamente el mismo hecho con el mismo `eventId`. Core lo marcó `DUPLICATE` y evitó una segunda entrega. Esta prueba acredita la deduplicación de Core; no acredita por sí sola la deduplicación independiente del Inbox de M3 porque el duplicado no llegó a Obras.

### `treeRiskDetected`

- `eventId=1ca257a6-9cc6-4686-82d6-ee23c194dcde`.
- El caso probado tenía `riskLevel=CRITICAL` y `requiresPublicWorks=true`.
- Core confirmó `ROUTED` y entrega `DELIVERED` a `q.obras` en un intento, sin retry ni dead letter; M3 confirmó su procesamiento funcional.

## Reglas vigentes

- `requestId` identifica la solicitud de reparación y se devuelve como `sourceRequestId` en los eventos de orden.
- `containerId` y `treeId` son referencias del hecho recibido; M3 no los usa como sustituto implícito de `sourceRequestId`.
- `location.neighborhoodId`, cuando está presente, es UUID conforme al contrato vigente; no se sustituye unilateralmente por slug.
- M3 minimiza datos y solo persiste lo necesario para crear y seguir la intervención.

## Antecedentes no vigentes como contrato activo

La matriz del PO incluyó `urbanRiskDetected`, `urbanServiceRepairRequested`, `workOrderCreated`, `workOrderCompleted` y `workOrderValidated` con otros payloads. Esa fuente se conserva como `RECEIVED`, pero los aliases urbanos genéricos fueron reemplazados por los eventos específicos acordados y probados con M6.

## Pendientes no bloqueantes

- Ejecutar una prueba en la que un duplicado llegue efectivamente al Inbox de M3 si se desea acreditar su deduplicación de manera independiente de Core.
- Acordar cualquier cambio futuro de UUID a slug para barrios entre M2, M6 y Core antes de modificar el contrato.
- Mantener trazabilidad de los schemas de `data` registrados en Core; una modificación requiere nueva validación coordinada.
