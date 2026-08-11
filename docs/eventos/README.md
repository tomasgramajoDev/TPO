# Catálogo de eventos

Los nombres son identificadores técnicos vigentes o propuestos en inglés y `camelCase`. Ninguno posee contrato técnico `CONFIRMED` con la evidencia disponible.

| Evento | Dirección para Obras | Módulo relacionado | Estado | Documento donde está definido |
| --- | --- | --- | --- | --- |
| `complaintRouted` | Recibido | M2 Atención Ciudadana | `RECEIVED` (fuente PO) | [Atención Ciudadana](../integraciones/atencion-ciudadana.md) |
| `complaintEscalated` | Recibido | M2 Atención Ciudadana | `RECEIVED` (fuente PO) | [Atención Ciudadana](../integraciones/atencion-ciudadana.md) |
| `infrastructureRepairRequested` | Recibido | M6 Ambiente y Servicios Urbanos | `RECEIVED` | [Ambiente](../integraciones/ambiente-servicios-urbanos.md) |
| `containerDamaged` | Recibido | M6 Ambiente y Servicios Urbanos | `RECEIVED` | [Ambiente](../integraciones/ambiente-servicios-urbanos.md) |
| `treeRiskDetected` | Recibido | M6 Ambiente y Servicios Urbanos | `RECEIVED` | [Ambiente](../integraciones/ambiente-servicios-urbanos.md) |
| `urbanRiskDetected` | Recibido, variante en tensión | M6 según matriz PO | `RECEIVED` (fuente PO) | [Ambiente](../integraciones/ambiente-servicios-urbanos.md) |
| `urbanServiceRepairRequested` | Recibido, variante en tensión | M6 según matriz PO | `RECEIVED` (fuente PO) | [Ambiente](../integraciones/ambiente-servicios-urbanos.md) |
| `trafficIncidentRegistered` | Recibido | M7 Tránsito | `RECEIVED` (fuente PO) | [Tránsito](../integraciones/transito.md) |
| `streetClosureAuthorized` | Recibido | M7 Tránsito | `RECEIVED` (fuente PO) | [Tránsito](../integraciones/transito.md) |
| `streetClosureRejected` | Recibido | M7 Tránsito | `RECEIVED` (fuente PO) | [Tránsito](../integraciones/transito.md) |
| `caseFileResolved` | Recibido | M1 Expedientes | `RECEIVED` (fuente PO) | [Expedientes](../integraciones/expedientes.md) |
| `publicWorksProjectCreated` | Publicado | M1 según matriz PO | `RECEIVED` | [Eventos publicados](eventos-publicados.md) |
| `publicWorksProjectSubmittedForApproval` | Publicado | M1 según matriz PO | `RECEIVED` | [Eventos publicados](eventos-publicados.md) |
| `publicWorksProjectApproved` | Publicado | M1 según matriz PO | `RECEIVED` | [Eventos publicados](eventos-publicados.md) |
| `publicWorksProjectRejected` | Publicado | M1 según matriz PO | `RECEIVED` | [Eventos publicados](eventos-publicados.md) |
| `publicWorksProjectStarted` | Publicado | M1 según matriz PO | `RECEIVED` | [Eventos publicados](eventos-publicados.md) |
| `publicWorksProgressRegistered` | Publicado | M1 según matriz PO | `RECEIVED` | [Eventos publicados](eventos-publicados.md) |
| `publicWorksExtensionRequested` | Publicado | M1 según matriz PO | `RECEIVED` | [Eventos publicados](eventos-publicados.md) |
| `publicWorksExtensionApproved` | Publicado | M1 según matriz PO | `RECEIVED` | [Eventos publicados](eventos-publicados.md) |
| `publicWorksExtensionRejected` | Publicado | M1 según matriz PO | `RECEIVED` | [Eventos publicados](eventos-publicados.md) |
| `publicWorksProjectSuspended` | Publicado | M1 según matriz PO | `RECEIVED` | [Eventos publicados](eventos-publicados.md) |
| `publicWorksProjectResumed` | Publicado | M1 según matriz PO | `RECEIVED` | [Eventos publicados](eventos-publicados.md) |
| `publicWorksProjectCompleted` | Publicado | M1 según matriz PO | `RECEIVED` | [Eventos publicados](eventos-publicados.md) |
| `workOrderCreated` | Publicado | M2/M6/M7 según matriz PO | `RECEIVED` | [Eventos publicados](eventos-publicados.md) |
| `workOrderScheduled` | Publicado | M2 según matriz PO | `RECEIVED` | [Eventos publicados](eventos-publicados.md) |
| `workOrderAssigned` | Publicado | M2 según matriz PO | `RECEIVED` | [Eventos publicados](eventos-publicados.md) |
| `workOrderStarted` | Publicado | M2 según matriz PO | `RECEIVED` | [Eventos publicados](eventos-publicados.md) |
| `workOrderPaused` | Publicado | M2 según matriz PO | `RECEIVED` | [Eventos publicados](eventos-publicados.md) |
| `workOrderDelayed` | Publicado | M2 según matriz PO | `RECEIVED` | [Eventos publicados](eventos-publicados.md) |
| `workOrderRescheduled` | Publicado | M2 según matriz PO | `RECEIVED` | [Eventos publicados](eventos-publicados.md) |
| `workOrderCompleted` | Publicado | M2/M6 según fuentes recibidas | `RECEIVED` (PO y pedido M6) | [Ambiente](../integraciones/ambiente-servicios-urbanos.md) |
| `workOrderValidated` | Publicado | M2/M6 según matriz PO | `RECEIVED` | [Eventos publicados](eventos-publicados.md) |
| `workOrderReopened` | Publicado | M2 según matriz PO | `RECEIVED` | [Eventos publicados](eventos-publicados.md) |
| `streetClosureRequested` | Publicado | M7 Tránsito | `RECEIVED` (fuente PO) | [Tránsito](../integraciones/transito.md) |

## Variantes de M6 en tensión

La comunicación directa de M6 define `infrastructureRepairRequested`, `containerDamaged` y `treeRiskDetected`. La matriz enviada por el PO vuelve a definir `urbanRiskDetected` y `urbanServiceRepairRequested`. Se conservan ambas variantes como `RECEIVED`; los eventos específicos de M6 continúan como línea de trabajo interna, pero la selección externa definitiva queda pendiente.

Ver también [eventos recibidos](eventos-recibidos.md), [eventos publicados](eventos-publicados.md) y [contratos pendientes](contratos-pendientes.md).
