# Integración con Tránsito — Módulo 7

## Objetivo

Solicitar cortes de calle y recibir su autorización o rechazo; evaluar incidentes viales que puedan requerir Obras.

## Evidencia E2E de cortes — 2026-11-13/15

- M3 publicó `streetClosureRequested` con `eventId=2d6893aa-9482-4dfd-98c3-85607f36bdab` y `correlationId=afca371d-ddfd-497c-a437-f9152bef52bf`.
- Core confirmó aceptación, estado `ROUTED`, entrega `DELIVERED` a `q.transito` en el primer intento, sin reintentos ni DLQ. M7 confirmó recepción, persistencia del corte y sus tramos, y procesamiento funcional.
- El 2026-11-15 M3 recibió y procesó `streetClosureApproved` con `eventId=6f521edf-177f-43c4-b3ec-0a3eb1245fd5` y el mismo `correlationId`.
- M3 recibió y procesó luego `streetClosureEnded` con `eventId=c8479b39-4741-49f3-a3ea-f255d16416c2` y el mismo `correlationId`.
- La evidencia del consumidor M3 prueba el recorrido funcional M7 → Core → M3. Falta la verificación de Core sobre `ROUTED`/`DELIVERED`, intentos y DLQ de las dos respuestas para elevar el circuito completo a `CONFIRMED` según el criterio documental del equipo.

**Estado:** solicitud M3 → Core → M7 `CONFIRMED`; aprobación y cierre M7 → M3 comprobados funcionalmente y pendientes únicamente de la constancia operativa de Core.

## Incidente vial de prueba — 2026-11-15

- M7 publicó `roadAccidentRegistered`; Core lo entregó a M3 con `eventId=9d7b06ec-dfa3-4ca6-9d28-acc17ed82523` y `correlationId=dca92b7c-b533-438e-99de-cebc6446d4ef`.
- Azure Test registró cuatro pares `received`/`error` a las 17:10:45, 17:10:50, 17:11:21 y 17:13:21 UTC, coherentes con la entrega original y los tres reintentos configurados para `maxAttempts=4`.
- El evento falló durante la validación anterior a `event_inbox`; por eso no figura como procesado y no produjo una proyección funcional.
- El sobre exacto debe cruzarse con el contrato M3–M7 antes de atribuir la falla a un campo concreto. M7 y Core deben confirmar el payload y el estado final/DLQ; después se repite la prueba con un nuevo hecho o el mismo `eventId` si se trata de reentregar exactamente el mismo hecho corregido según las reglas de Core.

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

## Pendientes externos

- Nombres y payloads definitivos.
- Modelo de calles, tramos y ubicación.
- Identificadores y correlación.
- Períodos autorizados, condiciones, desvíos y extensiones.
- Representación de los desvíos en el payload de `streetClosureRequested`.
- Semántica de bloqueo de una orden durante rechazo o vencimiento.
- Convenciones de Core.
