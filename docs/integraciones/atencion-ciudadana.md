# Integración con Atención Ciudadana — Módulo 2

## Objetivo

Recibir reclamos de infraestructura derivados o escalados y publicar los estados que Atención Ciudadana confirme necesitar para el seguimiento del ciudadano.

## Eventos recibidos comunicados por el PO

### `complaintRouted`

- **Estado:** `RECEIVED` (fuente: matriz enviada por el PO; pendiente de confirmación con M2).
- **Nombre funcional original:** Reclamo derivado.
- **Emisor:** Atención Ciudadana.
- **Disparador:** un reclamo se clasifica como problema de infraestructura.
- **Payload funcional comunicado por el PO:** `ticketId`, `category`, `subcategory`, `description`, `location`, `priority`, `createdAt`, `evidence`, `affectedPeople` cuando corresponda.
- **Acción de Obras:** registrar para evaluación; aceptar, pedir información, vincular a una orden o crear una nueva.
- **Evento derivado posible:** `workOrderCreated`.
- **Correlación:** identificador de ticket pendiente de acuerdo.

### `complaintEscalated`

- **Estado:** `RECEIVED` (fuente: matriz enviada por el PO; pendiente de confirmación con M2).
- **Nombre funcional original:** Reclamo escalado.
- **Emisor:** Atención Ciudadana.
- **Disparador:** aumenta la prioridad de un reclamo previamente derivado.
- **Payload funcional comunicado por el PO:** `ticketId`, `previousPriority`, `newPriority`, `reason`, `escalatedAt`.
- **Acción de Obras:** actualizar prioridad y alertar; si cambia la programación, publicar `workOrderRescheduled`.

La obligatoriedad de estos campos no está acordada.

## Eventos que la matriz del PO asigna a M2

`workOrderCreated`, `workOrderScheduled`, `workOrderAssigned`, `workOrderStarted`, `workOrderPaused`, `workOrderDelayed`, `workOrderRescheduled`, `workOrderCompleted`, `workOrderValidated` y `workOrderReopened`.

Todos quedan `RECEIVED` como información del PO y pendientes de confirmación bilateral con M2. La matriz describe `workOrderValidated` como resolución definitiva del reclamo vecinal; esa definición no se eleva a `AGREED` hasta que M2 la confirme.

## Pendientes externos

- Nombres definitivos y casing.
- Payloads y campos obligatorios/opcionales.
- Uso de `ticketId` u otro identificador.
- Estados que M2 desea consumir.
- Cierre del reclamo con `workOrderCompleted` o `workOrderValidated`.
- Confirmar si M2 consume también `workOrderPaused`, incorporado por la matriz del PO pero ausente en la lista anterior.
- Manejo de duplicados, reaperturas y conformidad del ciudadano.
- Convenciones de Core.
