# Historial de cambios

## 2026-08-13 — Adopción de GitFlow simplificado para aplicaciones

- El usuario confirmó que frontend y backend seguirán el esquema docente `feature/*` → `develop` → `release/vX.Y.Z` → `main`.
- `develop` quedó asociado al ambiente Azure `development` y `release/*` al ambiente `test`.
- El cierre del sprint crea una rama de release; el Product Owner valida la versión candidata en `test` y DevOps autoriza operativamente cada despliegue.
- `main` pasa a representar versiones aprobadas, sin despliegue productivo mientras producción continúe fuera del alcance.
- Los workflows Terraform actuales no se modificaron: administran la plataforma y no son todavía los pipelines de frontend/backend.
- Esta decisión reemplaza para las aplicaciones el flujo inicial `main` → `development` y release publicada → `test`, conservado en este historial.

## 2026-08-11 — Inicialización documental

- Se creó la estructura solicitada y el índice navegable.
- Se organizó el alcance funcional, los ciclos de vida, roles y reglas de negocio.
- Se registraron por separado las integraciones con M1, M2, M6, M7 y M9.
- Se creó el catálogo de eventos y se distinguió el conjunto inicial de los eventos agregados por el equipo.
- Se clasificaron contratos como `PROPOSED`, `RECEIVED` o `CORE_PENDING`; no se marcó ninguno `CONFIRMED`.

## 2026-08-11 — Actualización de la integración con M6

- `urbanServiceRepairRequested` deja de ser la propuesta activa y queda reemplazado por `infrastructureRepairRequested` según la comunicación de M6.
- `urbanRiskDetected` deja de ser la propuesta activa para M6 y queda reemplazado por `treeRiskDetected` por decisión del equipo de Obras.
- Se incorpora `containerDamaged` con consumo condicionado por `requiresPublicWorks = true`.
- Se registra la correlación `infrastructureRepairRequested.requestId` → `workOrderCompleted.sourceRequestId`.
- Se registra como pendiente la correlación de `containerDamaged` y `treeRiskDetected`.
- Se registra la diferencia entre el payload general `result`/`evidence` y el solicitado por M6 `outcome`/`attachments[]`.
- Se registra como pendiente si M6 cierra con `workOrderCompleted` o espera `workOrderValidated`.
- Se actualizó el documento de alcance compartido: las secciones recibidas de M6 ahora describen `infrastructureRepairRequested`, `containerDamaged` y `treeRiskDetected`; las secciones siguientes fueron renumeradas y `workOrderCompleted` conserva explícitamente el pedido y las dudas de M6.

No se eliminó el antecedente de los eventos genéricos; permanece documentado como propuesta histórica reemplazada.

## 2026-08-11 — Rol del usuario

- Se registró que el usuario cumple el rol **DevOps** dentro del equipo.
- La fase continúa siendo exclusivamente documental; el rol no habilita aún cambios de infraestructura, despliegue o automatización.

## 2026-08-11 — Responsabilidades DevOps y flujo de despliegue

- Se amplió el alcance del rol DevOps: selección del proveedor cloud, armado y administración de la parte cloud, infraestructura como código con Terraform y administración de pipelines.
- Se registró que el despliegue debe ser lanzado o autorizado por DevOps.
- Se documentó el flujo previsto de promoción: pull request completado hacia desarrollo y release aprobado hacia prueba.
- Se dejaron pendientes el proveedor, los servicios, los eventos exactos de los pipelines, la modalidad de autorización y el eventual ambiente de producción.
- No se implementó infraestructura, automatización ni despliegues; el repositorio continúa en fase documental.

## 2026-08-11 — Matriz de integraciones enviada por el PO

- Se incorporó como fuente `RECEIVED` el documento `Integraciones con Módulos`, enviado por el PO.
- Se actualizaron a `RECEIVED` las rutas de eventos que la matriz asigna a M1, M2 y M7, sin elevarlas a acuerdo bilateral.
- Se registró que M2 recibiría también `workOrderPaused` y que la matriz describe `workOrderValidated` como cierre definitivo del reclamo.
- Se registró que la matriz asigna a M1 los tres eventos `publicWorksExtension*`.
- Se incorporó `workOrderCreated` como evento informado a Tránsito cuando nace de un incidente vial.
- Se registraron como definiciones técnicas recibidas del PO UUID, `camelCase`, ISO 8601, versionado y JSON Schema, pendientes de confirmación con Core.
- Se reabrió la contradicción de M6: la matriz del PO lista `urbanRiskDetected` y `urbanServiceRepairRequested`, mientras la comunicación directa de M6 define `infrastructureRepairRequested`, `containerDamaged` y `treeRiskDetected`.

## 2026-08-11 — Inicio de la fase de desarrollo DevOps

- El usuario autorizó expresamente comenzar las tareas DevOps.
- Se cerró la fase exclusivamente documental y se habilitaron infraestructura, Terraform, automatización y pipelines.
- Se eligió Microsoft Azure con región predeterminada `Brazil South` para el primer incremento.
- Se eligieron Azure Container Apps Consumption, Azure Blob Storage para el estado de Terraform y GitHub Actions con OIDC.
- Se fijó el flujo inicial: merge de pull request a `main` hacia `development` y release publicado hacia `test`, ambos con autorización de DevOps mediante ambientes protegidos.
- El desarrollo del frontend y backend, la base de datos, la mensajería, autenticación y producción siguen fuera de este primer incremento.

## 2026-08-11 — Incorporación de la Clase 2

- Se incorporó la Clase 2 como fuente docente sobre sistemas orientados a eventos, metodologías ágiles, Definition of Done, Git y escalado ágil.
- Se registraron como propuesta DevOps la revisión por pares, las pruebas, la documentación, los requisitos no funcionales y las release notes antes de promover una historia.
- La referencia a producción con feature toggle desactivado quedó pendiente y no habilitó la creación de un ambiente productivo.
- Nexus, SAFe y el modelo Spotify se conservaron como alternativas explicadas en clase, no como metodología elegida por el proyecto.

## 2026-08-11 — Ajuste de región Azure

- La política `Allowed resource deployment regions` de Azure for Students rechazó los recursos en `Brazil South`.
- Se eligió `Chile Central`, la región permitida más cercana a Argentina que soporta Storage, Managed Identity, Container Registry, Log Analytics y Container Apps.
- Los resource groups vacíos creados durante el intento inicial conservan su ubicación de metadatos en `Brazil South`; los recursos de servicio se despliegan en `Chile Central`.

## 2026-08-11 — Bootstrap Azure y GitHub

- Se desplegaron el estado remoto, el Container Registry Basic, la identidad administrada, las credenciales federadas y los permisos de `development` y `test`.
- El estado del bootstrap se migró a Azure Blob Storage y un plan posterior confirmó que no existen cambios pendientes.
- Se crearon los environments `development` y `test` con el usuario DevOps como revisor obligatorio.
- Se cargaron las variables OIDC y del backend en ambos environments, sin `client secret`.
- Se habilitaron los disparos automáticos: un cambio en `main` prepara `development` y una release publicada prepara `test`; los `apply` continúan sujetos a aprobación DevOps.

## 2026-08-13 — Primer despliegue de development

- Se fusionó el PR de infraestructura en `main`; el archivo Java anterior dejó de formar parte del repositorio vigente.
- El merge inició el workflow `Deploy development` mediante el disparador automático configurado.
- DevOps autorizó por separado la generación del plan y la aplicación del artefacto aprobado.
- El plan revisado creó `cae-obras-publicas-dev` y `log-obras-publicas-dev` en `Chile Central`: 2 altas, 0 cambios y 0 eliminaciones.
- La ejecución de GitHub Actions finalizó correctamente y guardó el estado en `development.terraform.tfstate`.
- El ambiente aún no contiene frontend, backend, base de datos ni mensajería; esos componentes continúan pendientes de definición e implementación.

## 2026-08-25 — PostgreSQL, actividad de integración y diagramas

- El usuario confirmó PostgreSQL como motor de base de datos del módulo.
- La elección no se amplió por inferencia a un servicio administrado, tamaño, red, backups, credenciales ni estrategia de migraciones de Azure.
- Se incorporó la Clase 4 / Unidad IV como material docente y se verificó que las cinco clasificaciones de MediConecta son correctas.
- Se completó la actividad con criterio de selección, justificación y riesgo para cada escenario.
- Se incorporaron el backlog, los dos ciclos y los prototipos como fuentes `RECEIVED`.
- Se verificó que los ciclos aportados ya son diagramas de secuencia y se creó el diagrama de casos de uso faltante.
- Se creó una secuencia propuesta de aprobación de proyecto con PostgreSQL y publicación asíncrona, sin fijar Service Bus frente a Event Grid.
- Se registraron sin resolver las diferencias `ticketCreated`/`complaintRouted`, `streetClosureApproved`/`streetClosureAuthorized`, `updateTicketStatus`, la semántica de finalización de órdenes, el evento del borrador y la referencia a aplicación móvil.

## 2026-08-25 — Repositorios de aplicación verificados

- Se recibieron y clonaron para auditoría los repositorios públicos `NadineLewit/DesarrolloAppsII_Front` e `ignacionogue/DesarrolloDeAplicacionesIIBack`.
- El frontend confirmó React 19, TypeScript 6, Vite 8, Node 24, Nginx 1.29, Dockerfile y health check `/health`; lint, cuatro pruebas y build finalizaron correctamente.
- El backend confirmó Spring Boot 4.1.0, Java 17 y Maven Wrapper; su única prueba y el build finalizaron correctamente.
- El backend recibido aún no implementa API web, PostgreSQL, health check ni Dockerfile, por lo que no puede considerarse desplegable como servicio HTTP.
- Se verificó permiso GitHub `WRITE` para el backend y `READ` para el frontend con la cuenta autenticada.
- Se abrieron los pull requests `ignacionogue/DesarrolloDeAplicacionesIIBack#1` y `NadineLewit/DesarrolloAppsII_Front#1` con los workflows CI.
- El CI del backend detectó inicialmente que `mvnw` no tenía permiso de ejecución en Linux; se corrigió el workflow y la segunda corrida validó pruebas, empaquetado e imagen Docker correctamente.
- El CI del frontend se ejecutó en el fork y validó correctamente instalación, lint, cuatro pruebas, build Vite e imagen Docker. La incorporación al repositorio original sigue pendiente de revisión del propietario.
- Los workflows aún no publican imágenes ni despliegan recursos Azure.

## 2026-08-25 — PostgreSQL preparado en Terraform

- Se registró `Microsoft.DBforPostgreSQL` en la suscripción Azure for Students; el registro no creó recursos facturables.
- Azure confirmó en `Chile Central` el SKU burstable `Standard_B1ms`, 32 GiB mínimos y PostgreSQL 16.
- Se preparó Azure Database for PostgreSQL Flexible Server únicamente para `development`, con backup de 7 días, sin alta disponibilidad ni backup georredundante.
- Terraform genera el nombre y una contraseña robusta; la contraseña permanece sensible en el estado remoto y no se publica como output ni se guarda en Git.
- Se agregó protección `prevent_destroy` al servidor y a la base `obras_publicas`.
- Se documentó el riesgo temporal de permitir direcciones Azure mediante la regla `0.0.0.0`; deberá reemplazarse por red privada antes de producción.
- `terraform fmt` y `terraform validate` finalizaron correctamente para `development` y `test`.
- El plan real contra el estado remoto quedó en 5 altas, 0 cambios y 0 bajas. Se corrigió antes una deriva del perfil Container Apps para evitar modificar el entorno existente.
- El plan todavía no fue aplicado; continúa sujeto a revisión y autorización DevOps.
