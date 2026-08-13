# Eventos publicados por Obras

Los payloads de esta página fueron incluidos en la matriz enviada por el PO y quedan `RECEIVED` para las rutas allí indicadas. La obligatoriedad, el envelope, la versión técnica y la confirmación bilateral todavía deben acordarse con consumidores y Core.

## Ciclo de obra

| Evento | Disparador | Payload funcional propuesto | Origen histórico |
| --- | --- | --- | --- |
| `publicWorksProjectCreated` | Proyecto creado en Borrador. | `publicWorksProjectId`, `name`, `description`, `scope`, `location`, `estimatedBudget`, `estimatedDuration`, `technicalManager`, `status`, `createdAt` | Conjunto inicial (`ProyectoObraCreado`). |
| `publicWorksProjectSubmittedForApproval` | Pasa a Pendiente de aprobación. | `publicWorksProjectId`, `submittedAt`, `submittedBudget`, `submittedDeadline`, `technicalManager`, `submittedBy`, `documentation`, `notes` | Agregado por el equipo. |
| `publicWorksProjectApproved` | Pasa a Aprobada. | `publicWorksProjectId`, `approvedBudget`, `approvedDeadline`, `approvedAt`, `approvedBy`, `notes` | Conjunto inicial (`ObraAprobada`). |
| `publicWorksProjectRejected` | Pasa a Rechazada. | `publicWorksProjectId`, `rejectedAt`, `reason`, `notes`, `rejectedBy`, `observedDocumentation` | Agregado por el equipo. |
| `publicWorksProjectStarted` | Comienza formalmente la ejecución. | `publicWorksProjectId`, `actualStartDate`, `startedBy`, `currentPlan`, `notes` | Conjunto inicial (`ObraIniciada`). |
| `publicWorksProgressRegistered` | Se registra avance físico o presupuestario. | `publicWorksProjectId`, `stageId` o `milestoneId`, `physicalProgressPercentage`, `executedAmount`, `registeredAt`, `registeredBy`, `notes`, `documentation` | Conjunto inicial (`AvanceObraRegistrado`). |
| `publicWorksExtensionRequested` | Se solicita ampliar plazo/presupuesto. | `extensionId`, `publicWorksProjectId`, `extensionType`, `currentValue`, `requestedValue`, `reason`, `justification`, `documentation`, `requestedAt`, `requestedBy` | Agregado por el equipo. |
| `publicWorksExtensionApproved` | Se aprueba la ampliación. | `extensionId`, `publicWorksProjectId`, `extensionType`, `previousValue`, `approvedValue`, `approvedAt`, `approvedBy`, `notes` | Agregado por el equipo. |
| `publicWorksExtensionRejected` | Se rechaza la ampliación. | `extensionId`, `publicWorksProjectId`, `extensionType`, `requestedValue`, `reason`, `rejectedAt`, `rejectedBy`, `notes` | Agregado por el equipo. |
| `publicWorksProjectSuspended` | Se suspende la ejecución. | `publicWorksProjectId`, `suspendedAt`, `reason`, `estimatedImpact`, `affectedWorkOrders`, `suspendedBy`, `notes` | Conjunto inicial (`ObraSuspendida`). |
| `publicWorksProjectResumed` | Vuelve a En ejecución. | `publicWorksProjectId`, `resumedAt`, `reason`, `resumedBy`, `updatedPlan`, `enabledWorkOrders`, `notes` | Agregado por el equipo. |
| `publicWorksProjectCompleted` | Pasa a Finalizada. | `publicWorksProjectId`, `actualCompletionDate`, `finalCost`, `result`, `completionPercentage`, `certifications`, `finalDocumentation`, `completedBy` | Conjunto inicial (`ObraFinalizada`). |

M1 aparece como consumidor tentativo de varios eventos, pero debe confirmar cuáles necesita.

## Ciclo de órdenes

| Evento | Disparador | Payload funcional propuesto | Origen histórico |
| --- | --- | --- | --- |
| `workOrderCreated` | Se registra una orden. | `workOrderId`, `publicWorksProjectId?`, `sourceRequestId`, `interventionType`, `description`, `location`, `priority`, `status`, `createdAt` | Conjunto inicial (`OrdenTrabajoCreada`). |
| `workOrderScheduled` | Se fija fecha/horario. | `workOrderId`, `sourceRequestId`, `scheduledFrom`, `scheduledTo`, `estimatedDuration`, `location`, `plannedResources`, `status`, `scheduledBy` | Agregado por el equipo. |
| `workOrderAssigned` | Se asigna cuadrilla. | `workOrderId`, `sourceRequestId`, `crewId`, `scheduledDate`, `assignedMachinery`, `plannedMaterials`, `status`, `assignedBy` | Conjunto inicial (`OrdenTrabajoAsignada`). |
| `workOrderStarted` | La cuadrilla inicia. | `workOrderId`, `sourceRequestId`, `startedAt`, `crewId`, `startedBy`, `status`, `notes` | Conjunto inicial (`OrdenTrabajoIniciada`). |
| `workOrderPaused` | Se detiene temporalmente. | `workOrderId`, `sourceRequestId`, `pausedAt`, `reason`, `pausedBy`, `currentProgress`, `notes` | Agregado por el equipo. |
| `workOrderDelayed` | No se cumple la fecha prevista. | `workOrderId`, `sourceRequestId`, `reason`, `originalScheduledDate`, `estimatedNewDate`, `reportedBy`, `notes` | Conjunto inicial (`OrdenTrabajoDemorada`). |
| `workOrderRescheduled` | Cambia la programación. | `workOrderId`, `sourceRequestId`, `previousScheduledDate`, `newScheduledDate`, `reason`, `rescheduledBy`, `notes` | Agregado por el equipo. |
| `workOrderCompleted` | La cuadrilla termina físicamente y carga evidencia. | Alcance general: `workOrderId`, `sourceRequestId`, `publicWorksProjectId?`, `result`, `completedAt`, `consumedMaterials`, `notes`, `evidence`, `crewId`. M6 solicita como mínimo `workOrderId`, `sourceRequestId`, `completedAt`, `outcome`, `attachments[]`. | Conjunto inicial (`OrdenTrabajoFinalizada`); payload M6 recibido. |
| `workOrderValidated` | Inspector confirma el resultado. | `workOrderId`, `sourceRequestId`, `validatedAt`, `validationResult`, `inspectorId`, `notes`, `evidence` | Agregado por el equipo. |
| `workOrderReopened` | La inspección exige correcciones. | `workOrderId`, `sourceRequestId`, `reopenedAt`, `reason`, `inspectorId`, `requiredCorrections`, `priority`, `notes` | Agregado por el equipo. |

El consumidor principal de los eventos de orden será el módulo que originó la solicitud, pero cada módulo debe confirmar qué estados consume. Para M6, `workOrderCompleted.sourceRequestId` debe conservar el `requestId` de `infrastructureRepairRequested`; los demás orígenes no tienen correlación cerrada.

## Cortes de calle

| Evento | Disparador | Payload funcional propuesto | Origen histórico |
| --- | --- | --- | --- |
| `streetClosureRequested` | Una obra u orden requiere cortar total o parcialmente el tránsito. | `closureRequestId`, `publicWorksProjectId` o `workOrderId`, `reason`, `affectedSections`, `requestedFrom`, `requestedTo`, `closureType`, `estimatedDuration`, `requestedBy`, `notes` | Conjunto inicial (`CorteCalleSolicitado`). |

## Estado

- Los eventos de ciclo de obra quedan `RECEIVED` para la ruta hacia M1 indicada por el PO, incluidos los tres eventos de ampliación.
- Los eventos de orden quedan `RECEIVED` para las rutas M2/M6/M7 que aparecen en la matriz; cada contraparte debe confirmar el subconjunto que consume.
- `workOrderCompleted` mantiene además el payload mínimo diferente comunicado directamente por M6.
- Ningún evento queda `AGREED` o `CONFIRMED` únicamente por aparecer en la matriz.
