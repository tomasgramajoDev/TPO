# Integración con Ambiente, Higiene y Servicios Urbanos — Módulo 6

## Estado general

M6 comunicó eventos y payloads tentativos. Obras aceptó funcionalmente consumir las derivaciones relevantes, pero no existe evidencia suficiente para marcar los contratos como `CONFIRMED`; se mantienen `RECEIVED` hasta cerrar payloads, correlación y convenciones de Core.

## Eventos recibidos

### `infrastructureRepairRequested`

- **Nombre funcional:** solicitud de reparación de infraestructura.
- **Estado:** `RECEIVED`.
- **Emisor:** M6.
- **Consumidor:** M3 Obras Públicas.
- **Disparador:** M6 detecta en vía pública un daño de infraestructura ajeno a su competencia.
- **Payload recibido:** `requestId`, `damageType`, `severity`, `location`, `detectedIn`, `complaintId?`, `publicSafetyRisk`, `requestedAt`.
- **Obligatorios:** todos salvo `complaintId`, según la notación recibida; confirmar formalmente.
- **Correlación:** si genera una orden, debe conservarse `requestId`. Al responder, `workOrderCompleted.sourceRequestId = infrastructureRepairRequested.requestId`.
- **Acción de Obras:** evaluar y, si corresponde, crear una `WorkOrder` trazable.
- **Respuesta esperada por M6:** `workOrderCompleted`.
- **Prioridad de integración:** bloqueante/alta.
- **Dudas:** enums, estructura de `location`, definición de `detectedIn`, envelope y cierre definitivo.

### `containerDamaged`

- **Nombre funcional:** contenedor dañado con posible componente de obra civil.
- **Estado:** `RECEIVED`.
- **Emisor:** M6.
- **Consumidor:** M3, solo cuando `requiresPublicWorks = true`.
- **Payload recibido:** `containerId`, `containerCode`, `zoneId`, `location`, `damageType`, `severity`, `requiresPublicWorks`, `detectedAt`, `complaintId?`.
- **Obligatorios:** todos salvo `complaintId`, según la notación recibida; confirmar formalmente.
- **Acción de Obras:** evaluar si corresponde crear una orden.
- **Prioridad de integración:** baja.
- **Correlación:** pendiente. No asumir que `containerId` se mapea automáticamente a `sourceRequestId`.

### `treeRiskDetected`

- **Nombre funcional:** riesgo de arbolado detectado.
- **Estado:** `RECEIVED`.
- **Emisor:** M6.
- **Consumidor:** M3 cuando `requiresPublicWorks = true`.
- **Payload recibido:** `treeId`, `surveyCode`, `species`, `zoneId`, `location`, `riskLevel`, `riskType`, `healthStatus`, `suggestedIntervention`, `requiresStreetClosure`, `requiresPublicWorks`, `surveyedAt`.
- **Prioridad funcional:** `HIGH` y `CRITICAL` son situaciones prioritarias. El material de M6 también las menciona como condición de disparo; se debe confirmar si se emiten otros niveles.
- **Acción de Obras:** evaluar intervención; si `requiresStreetClosure = true`, coordinar luego con Tránsito.
- **Correlación:** pendiente; no se acordó si usar `treeId`, `surveyCode` u otro identificador.
- **Decisión interna:** consumir este evento en lugar del genérico `urbanRiskDetected`.

## Evento solicitado por M6

### `workOrderCompleted`

- **Estado para esta integración:** `RECEIVED`.
- **Emisor:** M3.
- **Consumidor solicitado:** M6.
- **Disparador:** la cuadrilla termina físicamente la ejecución y carga evidencia.
- **Payload mínimo solicitado por M6:** `workOrderId`, `sourceRequestId`, `completedAt`, `outcome`, `attachments[]`.
- **Correlación acordada para reparaciones:** `sourceRequestId = requestId` de `infrastructureRepairRequested`.
- **Duda crítica:** M6 pidió usarlo para cerrar automáticamente la solicitud, pero debe confirmarse si el cierre definitivo debe esperar `workOrderValidated`.
- **Diferencia de vocabulario:** el alcance anterior propone `result`/`evidence`; M6 solicita `outcome`/`attachments[]`. No se elige un mapeo hasta acordarlo.

## Variante genérica recibida del PO

La matriz enviada por el PO vuelve a presentar los siguientes contratos con estado documental `RECEIVED`:

- `urbanRiskDetected`: `riskId`, `riskType`, `description`, `location`, `severity`, `detectedAt`, `evidence`, `sourceArea`.
- `urbanServiceRepairRequested`: `requestId`, `repairType`, `description`, `location`, `priority`, `requestedAt`, `evidence`, `notes`.
- `workOrderCreated`, `workOrderCompleted` y `workOrderValidated` como eventos enviados a M6.

Esta variante contradice la comunicación directa de M6, que ofrece `infrastructureRepairRequested`, `containerDamaged` y `treeRiskDetected`, y también difiere del payload mínimo solicitado por M6 para `workOrderCompleted`. La matriz del PO no se usa para sobrescribir esa comunicación: ambas versiones quedan abiertas hasta que PO, M6 y Obras definan cuál rige.

## Propuestas genéricas en tensión

- `urbanServiceRepairRequested` había quedado reemplazado en el catálogo activo por `infrastructureRepairRequested`, pero reaparece en la matriz enviada por el PO.
- `urbanRiskDetected` había quedado reemplazado por `treeRiskDetected` para M6, pero reaparece en la matriz enviada por el PO.

La decisión interna vigente de Obras continúa siendo consumir los eventos específicos comunicados directamente por M6. La contradicción externa se conserva en [decisiones pendientes](../decisiones/decisiones-pendientes.md) y ningún contrato se eleva a `AGREED` o `CONFIRMED`.
