# Integración con Ciudadanos y Expedientes Digitales — Módulo 1

## Evidencia E2E del escenario aprobado — 2026-11-08

**Estado contractual y funcional del escenario `approved`:** `CONFIRMED`.

**Fuente:** confirmación publicada por Core (M9) en Discord el 2026-11-08 a las 16:10, complementada por las confirmaciones funcionales de M1 y M3.

- M3 publicó `publicWorksProjectApproved` con `eventId=ce10dbfb-fa87-45a8-921f-adf8689ac1dc` y `sourceModule=obras`.
- Core lo validó, registró como `ROUTED` y entregó a `q.ciudadanos` en un intento, sin rechazos ni ingreso a DLQ.
- M1 creó el expediente institucional y publicó `caseFileResolved` v1.0 con `eventId=ad03a26a-12d8-414f-808a-63527e6417b6`, `sourceModule=ciudadanos`, `state=resolved` y `resolution=approved`.
- Core validó el evento, lo registró como `ROUTED` y lo entregó a `q.obras` en un intento, sin rechazos ni ingreso a DLQ.
- Ambos eventos conservaron `correlationId=223653b4-4d6b-4d59-9e75-a8ecc66d27ef`.
- El circuito relacionó `publicWorksProjectId=42807c4d-ff24-438f-aaa2-d025e8c27980` con `caseFileId=2567331e-d718-4e24-9870-2366f1c43059`.
- M3 confirmó el procesamiento funcional y la asociación del expediente con el proyecto en su base de datos.

La variante `rejected` no queda cubierta por esta evidencia y continúa pendiente como prueba independiente.

## Evento recibido comunicado por el PO

### `caseFileResolved`

- **Nombre funcional:** expediente resuelto.
- **Estado histórico de esta sección:** `RECEIVED`. El contrato v1.0 y el escenario `approved` quedaron confirmados posteriormente por la evidencia E2E precedente.
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
