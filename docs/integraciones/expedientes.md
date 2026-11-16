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

Con esta evidencia quedan confirmadas ambas variantes de resolución.

## Evidencia de finalización del proyecto — 2026-11-14

**Estado de `publicWorksProjectCompleted` v1.0:** `CONFIRMED`.

- M3 publicó `publicWorksProjectCompleted` para `OBRA-3` con `eventId=0da5fc0d-b656-4b70-b46d-e76ebb91517a` y `correlationId=223653b4-4d57-a292-d4fb7daff878`.
- Core lo registró `ROUTED` y lo entregó a `q.ciudadanos` en un intento, sin error, retry ni dead letter.
- M1 confirmó el procesamiento funcional: la obra quedó `COMPLETED`, mientras el expediente asociado permaneció `RESUELTO` con resultado `approved`.
- M1 no emitió otro `caseFileResolved`, porque la finalización operativa de la obra no constituye una nueva resolución administrativa.

## Evento recibido comunicado por el PO

### `caseFileResolved`

- **Nombre funcional:** expediente resuelto.
- **Estado histórico de esta sección:** `RECEIVED`. El contrato v1.0 y los escenarios `approved` y `rejected` quedaron confirmados posteriormente por la evidencia E2E precedente.
- **Emisor:** M1.
- **Disparador:** se emite una resolución administrativa relacionada con una obra.
- **Payload comunicado por el PO:** `caseFileId`, `publicWorksProjectId`, `resolutionType`, `result`, `resolvedAt`, `notes`, `documentation`.
- **Acción de Obras:** registrar la resolución en el historial administrativo y bloquear el avance cuando la resolución sea necesaria y no habilite continuar.
- **Obligatoriedad y enums:** pendientes de acuerdo.

## Eventos que la matriz del PO asigna a M1

`publicWorksProjectCreated`, `publicWorksProjectSubmittedForApproval`, `publicWorksProjectApproved`, `publicWorksProjectRejected`, `publicWorksProjectStarted`, `publicWorksProgressRegistered`, `publicWorksExtensionRequested`, `publicWorksExtensionApproved`, `publicWorksExtensionRejected`, `publicWorksProjectSuspended`, `publicWorksProjectResumed` y `publicWorksProjectCompleted`.

La matriz recibida conserva estado `RECEIVED` para los eventos no probados. M1 confirmó y procesó `publicWorksProjectApproved` y `publicWorksProjectCompleted`; no se extrapola ese acuerdo al resto de la lista. Los tres eventos de ampliación continúan fuera del contrato activo M1–M3 hasta que exista un acuerdo nuevo.

## Pendientes externos

- Confirmar cualquier evento adicional de la matriz que no haya sido parte de los recorridos probados.
- Los eventos `publicWorksExtension*` permanecen fuera del contrato activo; solo se reabren mediante acuerdo expreso de M1.
- Si `publicWorksProgressRegistered` utiliza `stageId`, `milestoneId` o exactamente uno de ambos.
- Nombres, payloads y obligatoriedad de los eventos todavía no acordados.
- Documentación adjunta y versionado de los eventos todavía no acordados; las convenciones comunes de Core ya están confirmadas para los recorridos probados.
