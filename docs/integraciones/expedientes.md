# Integración con Ciudadanos y Expedientes Digitales — Módulo 1

## Evento recibido comunicado por el PO

### `caseFileResolved`

- **Nombre funcional:** expediente resuelto.
- **Estado:** `RECEIVED` (fuente: matriz enviada por el PO; pendiente de confirmación con M1).
- **Emisor:** M1.
- **Disparador:** se emite una resolución administrativa relacionada con una obra.
- **Payload comunicado por el PO:** `caseFileId`, `publicWorksProjectId`, `resolutionType`, `result`, `resolvedAt`, `notes`, `documentation`.
- **Acción de Obras:** registrar la resolución en el historial administrativo y bloquear el avance cuando la resolución sea necesaria y no habilite continuar.
- **Obligatoriedad y enums:** pendientes de acuerdo.

## Eventos que la matriz del PO asigna a M1

`publicWorksProjectCreated`, `publicWorksProjectSubmittedForApproval`, `publicWorksProjectApproved`, `publicWorksProjectRejected`, `publicWorksProjectStarted`, `publicWorksProgressRegistered`, `publicWorksExtensionRequested`, `publicWorksExtensionApproved`, `publicWorksExtensionRejected`, `publicWorksProjectSuspended`, `publicWorksProjectResumed` y `publicWorksProjectCompleted`.

La matriz recibida los deja en estado `RECEIVED`, no `AGREED`. M1 todavía debe confirmar cuáles consume. La inclusión de los tres eventos de ampliación es nueva respecto de la lista anterior y queda expresamente pendiente.

## Pendientes externos

- Qué eventos necesita realmente M1.
- Si M1 consume los eventos `publicWorksExtension*` incluidos por el PO.
- Si `publicWorksProgressRegistered` utiliza `stageId`, `milestoneId` o exactamente uno de ambos.
- Nombres, payloads y obligatoriedad.
- Qué tipos/resultados de resolución habilitan o bloquean el ciclo de la obra.
- Correlación entre `caseFileId` y `publicWorksProjectId`.
- Documentación adjunta, versionado y convenciones de Core.
