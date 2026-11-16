# Integración con Tránsito — Módulo 7

## Objetivo

Solicitar cortes de calle y recibir su autorización o rechazo; evaluar incidentes viales que puedan requerir Obras.

## Evidencia E2E de cortes v1.1 — 2026-11-15

- M3 publicó `streetClosureRequested` con `eventId=7f371af0-f38a-412f-adc3-09981a10de90`, `correlationId=3f2e4d0b-a6fa-4b08-ba40-8fb5101b240a` y `closureRequestId=01f1246b-8ac1-49de-8103-025e85d4ebcc`.
- Core confirmó aceptación, estado `ROUTED` y entrega `DELIVERED` a `q.transito` en el primer intento, sin reintentos ni DLQ. M7 confirmó recepción y procesamiento funcional.
- M7 publicó `streetClosureApproved` con `eventId=614222ce-715d-44e7-8e63-89250488ea7b` y `streetClosureEnded` con `eventId=7f098173-82c6-4831-849f-47a3b5ec0cb4`.
- Las dos respuestas conservaron el `correlationId` original y usaron el `eventId` de la solicitud como `causationId`, conforme al contrato documental v1.1; el envelope mantuvo `eventVersion="1.0"`.
- Core las registró `ROUTED` y `DELIVERED` a `q.obras` en un intento, sin errores ni dead letters. M3 confirmó ambas como `PROCESSED`, `streetClosureId=baf2c468-c354-4478-8588-cdb9486ba98e` y estado final `ENDED`.

**Estado:** circuito base y variantes adicionales del contrato documental v1.1 `CONFIRMED` por M3, M7 y Core.

## Variantes adicionales A/B/C — 2026-11-16

Core auditó siete eventos y once entregas. Todas quedaron `ROUTED`/`DELIVERED`, en un intento, sin error, retry ni dead letter. M3 confirmó las cuatro respuestas como `PROCESSED` y M7 confirmó los estados finales:

- A, rechazo: solicitud `d5f328ec-5b71-4bdb-8edb-653a6de2fd22`, respuesta `04edb9b6-9a45-4a68-b81f-4bd1c20979aa`, estado `REJECTED`.
- B, cierre automático: solicitud `458a93ea-19b9-49a8-bd09-c1a01f87c781`, aprobación `43597886-72a5-4028-9c75-822847197a3d`, cierre `a6fe83e5-5339-4686-b399-6c1239571e34`, estado `ENDED`.
- C, aprobado sin activar: solicitud `1d6ae7a0-eae8-485c-9469-fbd964beb965`, aprobación `1d426b5a-ac1b-428b-81dc-7f3890a6a35f`, estado interno `EXPIRED`; correctamente no se publicó `streetClosureEnded`.

Todas las respuestas conservaron correlación y usaron como `causationId` el `eventId` de su solicitud. El envelope continúa con `eventVersion="1.0"`; v1.1 es la versión documental.

## Incidente vial de prueba — 2026-11-15

- M7 publicó `roadAccidentRegistered`; Core lo entregó a M3 con `eventId=9d7b06ec-dfa3-4ca6-9d28-acc17ed82523` y `correlationId=dca92b7c-b533-438e-99de-cebc6446d4ef`.
- La primera entrega agotó cuatro intentos y quedó como dead letter `DELIVERY_FAILED`. Tras corregir el consumidor, Core realizó un único reintento manual conservando el `eventId` y registró auditoría `MANUAL/SUCCESS`.
- M3 confirmó Inbox `PROCESSED`, un intento local y una única proyección funcional para `accidentId=c4c66355-093c-46f4-a175-96bf6c0d5252`.
- M3 verificó que no persistió DNI, patente, vehículos, personas ni `inspectorId` en el Inbox minimizado ni en la proyección funcional.

**Estado:** `CONFIRMED`. La falla inicial y su recuperación se conservan como evidencia de resiliencia; no quedan como un pendiente del circuito.

## Eventos recibidos comunicados por el PO

### `trafficIncidentRegistered`

- **Estado:** `RECEIVED` (fuente: matriz enviada por el PO; pendiente de confirmación con M7).
- **Emisor:** Tránsito.
- **Disparador:** incidente vial con posibles daños en calles, señalización o infraestructura.
- **Payload comunicado por el PO:** `incidentId`, `occurredAt`, `location`, `description`, `reportedDamage`, `severity`, `evidence`.
- **Acción:** registrar y evaluar una intervención; correlacionar una orden con `incidentId` si corresponde.

### `streetClosureAuthorized`

- **Estado:** `RECEIVED` (fuente: matriz enviada por el PO; pendiente de confirmación con M7).
- **Emisor:** Tránsito.
- **Payload comunicado por el PO:** `closureRequestId`, `publicWorksProjectId` o `workOrderId`, `authorizedSections`, `authorizedFrom`, `authorizedTo`, `conditions`, `notes`, `authorizedBy`.
- **Acción:** marcar la solicitud como autorizada y programar dentro del período permitido.

### `streetClosureRejected`

- **Estado:** `RECEIVED` (fuente: matriz enviada por el PO; pendiente de confirmación con M7).
- **Emisor:** Tránsito.
- **Payload comunicado por el PO:** `closureRequestId`, `publicWorksProjectId` o `workOrderId`, `reason`, `rejectedAt`, `notes`.
- **Acción:** rechazar la solicitud y reprogramar, ajustar o bloquear la orden; publicar `workOrderRescheduled` si cambia la fecha.

## Eventos publicados comunicados por el PO

### `streetClosureRequested`

- **Estado:** `RECEIVED` (fuente: matriz enviada por el PO; pendiente de confirmación con M7).
- **Emisor:** Obras.
- **Consumidor:** Tránsito.
- **Disparador:** una obra u orden requiere interrupción total o parcial del tránsito.
- **Payload comunicado por el PO:** `closureRequestId`, `publicWorksProjectId` o `workOrderId`, `reason`, `affectedSections`, `requestedFrom`, `requestedTo`, `closureType`, `estimatedDuration`, `requestedBy`, `notes`.

La descripción de la matriz indica que la solicitud informa tramos, desvíos y horarios, pero el payload listado no contiene un campo explícito de desvíos. Debe aclararse si esa información forma parte de `affectedSections`, `notes` o de un campo aún no documentado.

### `workOrderCreated`

- **Estado:** `RECEIVED` (fuente: matriz enviada por el PO; pendiente de confirmación con M7).
- **Emisor:** Obras.
- **Consumidor:** Tránsito cuando la orden nace de un incidente vial.
- **Payload comunicado:** `workOrderId`, `publicWorksProjectId`, `sourceRequestId`, `interventionType`, `description`, `location`, `priority`, `status`, `createdAt`.
- **Pendiente:** confirmar si `publicWorksProjectId` es obligatorio para este origen y si `sourceRequestId` corresponde a `incidentId`.

## Pendientes externos fuera de los recorridos probados

- Completar la limpieza coordinada del registro histórico `streetClousureEnded`; el contrato y el código vigente usan `streetClosureEnded`.
- Probar prórrogas solo si continúan dentro del alcance comprometido; no son necesarias para reabrir los recorridos ya confirmados.
- Cualquier extensión futura de desvíos o tramos requiere versionar el contrato; no se infiere de la matriz histórica del PO.
