# Contratos de eventos pendientes

| Evento o familia | Pendiente | Equipo externo |
| --- | --- | --- |
| Todos | Envelope, versión, fechas, correlación, idempotencia y naming final. | Core M9 |
| `complaintRouted`, `complaintEscalated` | Nombres, payload, obligatoriedad e identificador del reclamo. | Atención Ciudadana M2 |
| Estados de `WorkOrder` hacia M2 | Confirmar el subconjunto comunicado por el PO, incluida la incorporación de `workOrderPaused`, y si `workOrderValidated` cierra definitivamente el reclamo. | Atención Ciudadana M2 |
| `infrastructureRepairRequested` | Confirmación bilateral del payload, enums, `location` y casing. | Ambiente M6 |
| `containerDamaged` | Identificador de correlación y respuesta esperada. | Ambiente M6 |
| `treeRiskDetected` | Identificador de correlación y condición exacta de emisión por nivel de riesgo. | Ambiente M6 |
| Variantes de eventos M6 | Resolver eventos específicos comunicados directamente por M6 frente a `urbanRiskDetected` y `urbanServiceRepairRequested` reintroducidos por la matriz del PO. | PO / Ambiente M6 |
| `workOrderCompleted` hacia M6 | `outcome` vs `result`, `attachments[]` vs `evidence` y cierre con `Completed` vs `Validated`. | Ambiente M6 |
| `trafficIncidentRegistered` | Nombre, payload y criterio de creación de orden. | Tránsito M7 |
| Eventos de corte | Tramos, ubicación, identificadores, períodos, condiciones, expiración y campo que representa desvíos. | Tránsito M7 |
| `caseFileResolved` | Payload, resultados habilitantes/bloqueantes y obligatoriedad. | Expedientes M1 |
| Ciclo de obra hacia M1 | Confirmar los doce eventos comunicados por el PO y si `stageId`/`milestoneId` son alternativos. | Expedientes M1 |
| `publicWorksExtension*` | Confirmar si M1 consume los tres eventos de ampliación incorporados por la matriz del PO. | Expedientes M1 |
| `workOrderPaused`, `workOrderDelayed`, `workOrderRescheduled` | Semántica y estados que cada consumidor requiere. | M2/M6/M7 |
| Convenciones comunes | Confirmar con M9 UUID, ISO 8601, versión y JSON Schema mencionados por el PO, incluidos nombres exactos y zona horaria. | Core M9 |

La lista de decisiones con contexto y contradicciones está en [decisiones pendientes](../decisiones/decisiones-pendientes.md).
