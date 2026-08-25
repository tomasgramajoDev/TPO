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
- PostgreSQL es el motor de base de datos elegido para el módulo. Esta decisión no define todavía el servicio administrado de Azure, el tamaño, la red, los backups ni la estrategia de migraciones.

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

## Decisiones internas sobre M6

- Obras acepta consumir `infrastructureRepairRequested`.
- `infrastructureRepairRequested.requestId` se conserva y se devuelve en `workOrderCompleted.sourceRequestId` cuando la orden tiene ese origen.
- `containerDamaged` se evalúa únicamente cuando `requiresPublicWorks = true`; no se asume correlación mediante `containerId`.
- Obras consume `treeRiskDetected` cuando requiere intervención de Obras, en lugar de pedir un evento urbano genérico.
- `HIGH` y `CRITICAL` se tratan como riesgos prioritarios.
- `requiresStreetClosure = true` puede originar posteriormente una solicitud a Tránsito.

Los payloads y nombres enviados por M6 siguen `RECEIVED` porque el material los presenta como tentativos y faltan confirmaciones técnicas.
