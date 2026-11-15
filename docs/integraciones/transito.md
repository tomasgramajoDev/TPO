# Integración con Tránsito — Módulo 7

## Objetivo

Solicitar cortes de calle y recibir su autorización o rechazo; evaluar incidentes viales que puedan requerir Obras.

## Evidencia parcial E2E — 2026-11-13/14

- M3 publicó `streetClosureRequested` con `eventId=2d6893aa-9482-4dfd-98c3-85607f36bdab` y `correlationId=afca371d-ddfd-497c-a437-f9152bef52bf`.
- Core confirmó aceptación, estado `ROUTED`, entrega `DELIVERED` a `q.transito` en el primer intento, sin reintentos y sin DLQ.
- M7 confirmó recepción, persistencia del corte y sus tramos, y procesamiento sin errores.
- El circuito completo permanece abierto porque M7 perdió conectividad AMQPS después de un redeploy. Debe publicar `streetClosureApproved` o `streetClosureRejected`, y luego ejecutar `streetClosureEnded`.

**Estado:** `CONFIRMED` únicamente para la solicitud M3 → Core → M7; respuesta y cierre todavía `PENDING`.

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
