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

## Evidencia E2E del escenario rechazado — 2026-11-14

**Estado contractual y funcional del escenario `rejected`:** `CONFIRMED`.

- M1 recibió `publicWorksProjectApproved` con `eventId=57f75122-d874-489a-9745-5de4bc694ff3` y creó el expediente institucional de `OBRA-16`.
- M1 publicó `caseFileResolved` v1.0 con `eventId=44fd8a17-fc0b-4638-8fdf-046117b8a00e`, `correlationId=f38eeb5c-7430-49d3-ac05-a639d1b59487`, `caseFileId=d0d81527-b2df-45a5-be06-387743a9209d` y `resolution=rejected`.
- Core verificó estado `ROUTED`, entrega `DELIVERED` a `q.obras` en un intento, sin error y sin registro asociado en `dead_letters`.
- M3 confirmó procesamiento `PROCESSED` y asociación de la resolución administrativa con `OBRA-16`.

Con esta evidencia quedan confirmadas ambas variantes de resolución. Continúa pendiente únicamente la prueba adicional de `publicWorksProjectCompleted` si forma parte del alcance comprometido.

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
