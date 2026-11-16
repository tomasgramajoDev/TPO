# Decisiones confirmadas

Esta página contiene decisiones internas o acuerdos explícitos. Un evento incluido aquí no queda automáticamente `CONFIRMED` como contrato externo.

## Fase y documentación

- El usuario autorizó el inicio de la fase de desarrollo DevOps el 2026-08-11.
- Se permiten infraestructura, automatización y pipelines; el código de aplicación requiere una solicitud específica.
- El usuario cumple el rol **DevOps** dentro del equipo.
- La documentación se mantiene en español y los identificadores técnicos en inglés.
- No se borra historia: los reemplazos se registran en el historial.
- Las contradicciones no se resuelven silenciosamente.

## Responsabilidad DevOps

- DevOps es responsable del armado y la administración de la infraestructura y los servicios cloud.
- La infraestructura se aprovisionará y administrará como código mediante Terraform.
- DevOps es responsable de preparar y administrar los pipelines.
- El despliegue deberá ser lanzado o autorizado por DevOps.
- Las aplicaciones seguirán un GitFlow simplificado: `feature/*` nace desde `develop`, los pull requests se fusionan en `develop`, la estabilización del sprint usa `release/vX.Y.Z` y las versiones aprobadas se fusionan en `main`.
- Un pull request de aplicación fusionado en `develop` habilita el despliegue al ambiente `development`.
- Una rama `release/vX.Y.Z` creada al cerrar el sprint habilita la promoción de la versión candidata al ambiente `test`.
- El Product Owner realiza la aprobación funcional en `test`; DevOps mantiene una autorización operativa independiente para el despliegue.
- `main` conserva versiones aprobadas y no despliega a producción mientras ese ambiente siga fuera del alcance.
- Los ambientes de GitHub deben exigir revisión de DevOps antes de ejecutar el despliegue.

## Plataforma cloud y CI/CD

- El proveedor elegido para el primer incremento es Microsoft Azure.
- La región predeterminada es `Chile Central`: es la opción habilitada más cercana al equipo y dispone de Azure Container Apps. `Brazil South` fue descartada porque la política de la suscripción Azure for Students impidió desplegar recursos allí.
- La plataforma de ejecución será Azure Container Apps en plan Consumption, con capacidad de escalar a cero.
- El estado remoto de Terraform se almacenará en Azure Blob Storage con autenticación Microsoft Entra ID.
- Los pipelines se implementarán con GitHub Actions y autenticación OIDC; no se usarán secretos de cliente persistentes.
- Se crearán ambientes separados `development` y `test`. Producción queda fuera del primer incremento.
- PostgreSQL es el motor de base de datos elegido para el módulo. En `development` se usa Azure Database for PostgreSQL Flexible Server 16, SKU `B_Standard_B1ms`, 32 GiB, zona 3, backup de 7 días, sin alta disponibilidad ni backup georredundante. La estrategia de migraciones y la red privada para producción continúan pendientes.

## Procedencia de información

- El documento `Integraciones con Módulos` fue enviado por el PO.
- Su procedencia está confirmada; sus contratos se clasifican como `RECEIVED`, no como `AGREED` o `CONFIRMED`.

## Alcance funcional

- El módulo es Obras Públicas, Infraestructura y Mantenimiento Urbano (M3).
- El único frontend previsto es un portal web responsive; no habrá aplicación móvil independiente.
- La UI estará en español.
- El ciudadano común no accede directamente y canaliza problemas mediante Atención Ciudadana.
- Una obra usa los estados Borrador, Pendiente de aprobación, Aprobada, Rechazada, En ejecución, Suspendida y Finalizada, con las transiciones documentadas.
- Una obra finalizada no recibe nuevas órdenes y no puede finalizar con órdenes pendientes.
- `workOrderCompleted`, `workOrderValidated` y `workOrderReopened` representan hechos diferentes.

## Convenciones entre equipos

- Core M9 es responsable de las convenciones comunes de integración.
- Obras debe informar a Core los cambios del catálogo de eventos.
- Core no se presume consumidor funcional de todos los eventos.
- Atributos, funciones y eventos se expresan en inglés y `camelCase`; endpoints, entidades y errores técnicos, en inglés.

## Integraciones verificadas

- M2 confirmó el 2026-11-15 la aplicación de `STARTED`, dos `PROGRESS` y `RESOLVED` para `TK-2026-000045`. El evento final `c889727e-db9e-4bd6-a064-7ff1ad5b32b6` quedó `PROCESSED/APPLIED`, sin error, y el ticket pasó de `IN_PROGRESS` a `RESOLVED`. Core lo auditó el 2026-11-16 como `ROUTED` y `DELIVERED` a M2 en un intento, sin retry ni dead letter; el recorrido probado queda `CONFIRMED`.
- Las variantes A/B/C de cortes v1.1 están `CONFIRMED`: Core auditó siete eventos `ROUTED`, once entregas `DELIVERED` en un intento y cero dead letters; M3/M7 confirmaron `REJECTED`, `ENDED` automático y `EXPIRED` sin `streetClosureEnded`, respectivamente.
- El escenario `approved` del circuito M3 → Core → M1 → Core → M3 quedó confirmado el 2026-11-08 mediante `publicWorksProjectApproved` y `caseFileResolved` v1.0, con correlación conservada, entrega en un intento, sin DLQ y procesamiento funcional confirmado por ambos módulos.
- El escenario `rejected` del mismo circuito quedó confirmado el 2026-11-14. Core registró `caseFileResolved` con `eventId=44fd8a17-fc0b-4638-8fdf-046117b8a00e`, `correlationId=f38eeb5c-7430-49d3-ac05-a639d1b59487`, estado `ROUTED`, entrega `DELIVERED` a `q.obras` en un intento y sin registros en DLQ. M3 confirmó `PROCESSED` y la asociación de la resolución con `OBRA-16`.
- El circuito base M3 ↔ M7 v1.1 quedó confirmado: Core verificó solicitud y respuestas `ROUTED`/`DELIVERED`, M7 confirmó el procesamiento de la solicitud y M3 procesó `streetClosureApproved` y `streetClosureEnded` hasta el estado final `ENDED`.
- `roadAccidentRegistered` quedó confirmado después de un único reintento manual de la dead letter original: M3 registró un solo efecto funcional y no persistió DNI, patente, vehículos, personas ni `inspectorId`.
- M6, M3 y Core confirmaron el circuito `infrastructureRepairRequested` → `workOrderScheduled` → `workOrderCompleted`, además de las entregas y el procesamiento de `containerDamaged` y `treeRiskDetected`.
- M1, M3 y Core confirmaron también `publicWorksProjectCompleted` para `OBRA-3`: entrega en un intento, sin retry/DLQ y procesamiento funcional por M1 sin emitir una nueva resolución administrativa.

## Decisiones vigentes sobre M6

- Obras acepta consumir `infrastructureRepairRequested`.
- `infrastructureRepairRequested.requestId` se conserva y se devuelve en `workOrderCompleted.sourceRequestId` cuando la orden tiene ese origen.
- `containerDamaged` se evalúa únicamente cuando `requiresPublicWorks = true`; no se asume correlación mediante `containerId`.
- Obras consume `treeRiskDetected` cuando requiere intervención de Obras, en lugar de pedir un evento urbano genérico.
- `HIGH` y `CRITICAL` se tratan como riesgos prioritarios.
- `requiresStreetClosure = true` puede originar posteriormente una solicitud a Tránsito.

Los recorridos y payloads efectivamente probados están `CONFIRMED`. Las variantes históricas de la matriz del PO y cualquier campo no ejercitado conservan estado `RECEIVED`; no se extrapola la evidencia a contratos distintos.
