# Eventos recibidos por Obras

## Resumen activo

| Evento | Emisor | Estado | Acción principal | Correlación |
| --- | --- | --- | --- | --- |
| `complaintRouted` | M2 | `RECEIVED` (fuente PO) | Evaluar reclamo y crear/vincular orden. | Identificador de ticket pendiente. |
| `complaintEscalated` | M2 | `RECEIVED` (fuente PO) | Actualizar prioridad y reprogramar si aplica. | Identificador de ticket pendiente. |
| `infrastructureRepairRequested` | M6 | `RECEIVED` | Evaluar y crear orden si corresponde. | `requestId` → `sourceRequestId` al responder. |
| `containerDamaged` | M6 | `RECEIVED` | Procesar solo con `requiresPublicWorks = true`. | Pendiente. |
| `treeRiskDetected` | M6 | `RECEIVED` | Procesar si requiere Obras; coordinar corte si aplica. | Pendiente. |
| `trafficIncidentRegistered` | M7 | `RECEIVED` (fuente PO) | Evaluar daño e intervención. | `incidentId` propuesto. |
| `streetClosureAuthorized` | M7 | `RECEIVED` (fuente PO) | Habilitar programación dentro del período. | `closureRequestId` propuesto. |
| `streetClosureRejected` | M7 | `RECEIVED` (fuente PO) | Bloquear, ajustar o reprogramar. | `closureRequestId` propuesto. |
| `caseFileResolved` | M1 | `RECEIVED` (fuente PO) | Registrar resolución y aplicar el bloqueo funcional acordado. | `caseFileId` y `publicWorksProjectId` propuestos. |

## Variante genérica de M6 recibida del PO

- `urbanRiskDetected`: `riskId`, `riskType`, `description`, `location`, `severity`, `detectedAt`, `evidence`, `sourceArea`.
- `urbanServiceRepairRequested`: `requestId`, `repairType`, `description`, `location`, `priority`, `requestedAt`, `evidence`, `notes`.

Esta variante no reemplaza la comunicación directa de M6; ambas quedan documentadas hasta resolver la contradicción.

## Payloads recibidos de M6

- `infrastructureRepairRequested`: `requestId`, `damageType`, `severity`, `location`, `detectedIn`, `complaintId?`, `publicSafetyRisk`, `requestedAt`.
- `containerDamaged`: `containerId`, `containerCode`, `zoneId`, `location`, `damageType`, `severity`, `requiresPublicWorks`, `detectedAt`, `complaintId?`.
- `treeRiskDetected`: `treeId`, `surveyCode`, `species`, `zoneId`, `location`, `riskLevel`, `riskType`, `healthStatus`, `suggestedIntervention`, `requiresStreetClosure`, `requiresPublicWorks`, `surveyedAt`.

`?` indica opcional según el material recibido. El payload fue presentado por M6 como diseño tentativo, por lo que permanece `RECEIVED`.

## Payloads comunicados por la matriz del PO

- `complaintRouted`: `ticketId`, `category`, `subcategory`, `description`, `location`, `priority`, `createdAt`, `evidence`, `affectedPeople` cuando corresponda.
- `complaintEscalated`: `ticketId`, `previousPriority`, `newPriority`, `reason`, `escalatedAt`.
- `trafficIncidentRegistered`: `incidentId`, `occurredAt`, `location`, `description`, `reportedDamage`, `severity`, `evidence`.
- `streetClosureAuthorized`: `closureRequestId`, `publicWorksProjectId` o `workOrderId`, `authorizedSections`, `authorizedFrom`, `authorizedTo`, `conditions`, `notes`, `authorizedBy`.
- `streetClosureRejected`: `closureRequestId`, `publicWorksProjectId` o `workOrderId`, `reason`, `rejectedAt`, `notes`.
- `caseFileResolved`: `caseFileId`, `publicWorksProjectId`, `resolutionType`, `result`, `resolvedAt`, `notes`, `documentation`.

La obligatoriedad de estos payloads no está acordada bilateralmente. Las fichas completas están en la carpeta [integraciones](../integraciones/README.md).
