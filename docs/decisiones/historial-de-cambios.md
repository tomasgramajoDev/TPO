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
- DevOps revisó y autorizó por separado el plan y el `apply` del workflow `Deploy development` 32851888220.
- La ejecución finalizó correctamente y creó `psql-obras-publicas-dev-dfc86d`, la base `obras_publicas` y la regla temporal `allow-azure-services`; el servidor quedó `Ready`.
- La verificación posterior detectó que Azure había asignado la zona 3. Se incorporó esa zona a Terraform para eliminar la deriva sin modificar el recurso desplegado.

## 2026-08-25 — Frontend y backend desplegados en development

- Se fusionó `ignacionogue/DesarrolloDeAplicacionesIIBack#1` en `develop`. El backend incorporó API web, Spring JDBC, configuración PostgreSQL, `/api/health`, pruebas y una imagen Docker no privilegiada.
- Se publicó la imagen backend `662ad1efc318377e93d73399ff94099153941a31` y la imagen frontend `c5161311424f8029c126310ebd54e0038f771624` en Azure Container Registry, ambas identificadas por SHA inmutable.
- El frontend incorporó un proxy Nginx `/api/*` hacia el backend. Una primera prueba detectó un `502` por falta de TLS SNI; se agregó `proxy_ssl_server_name` y la corrección quedó incluida en la imagen vigente.
- Terraform creó `ca-obras-publicas-dev-backend` y `ca-obras-publicas-dev-frontend` con ingress HTTPS, escalado Consumption de 0 a 1 réplica, probes y protección `prevent_destroy`.
- La identidad OIDC no podía asignar la identidad administrada a Container Apps. Se agregó `Managed Identity Operator` limitado a la identidad del proyecto mediante bootstrap Terraform; no se ampliaron permisos a toda la suscripción.
- DevOps autorizó el plan y el `apply` inicial del workflow 32856242288 y luego la actualización del frontend del workflow 32859326234. Este último aplicó 0 altas, 1 cambio y 0 bajas.
- Se verificaron el frontend público con HTTP 200, `/health`, el backend directo `/api/health` y el mismo endpoint mediante el proxy. En ambos accesos al backend se obtuvo `status: ok` y `database: up`, confirmando la consulta real a PostgreSQL.
- El plan Terraform posterior informó `No changes`; la infraestructura real coincide con el código.
- El pull request `NadineLewit/DesarrolloAppsII_Front#1` permanece pendiente porque DevOps tiene permiso de lectura en el repositorio propietario. Hasta su aceptación, la imagen se construye desde la rama `develop` del fork `tomasgramajoDev/DesarrolloAppsII_Front`.
- Este despliegue completa la base técnica de `development`; no implica que ya existan el esquema, las migraciones o los endpoints funcionales del dominio.

## 2026-09-01 — Mensajería Event Grid preparada para development

- Se eligió Azure Event Grid para la distribución de eventos discretos del ambiente académico de desarrollo. La elección evita incorporar la capacidad base de Service Bus Standard mientras no existen requisitos confirmados de orden, transacciones o detección de duplicados.
- Terraform crea el tópico `egt-obras-publicas-dev-events` con esquema CloudEvents 1.0 y protección `prevent_destroy`.
- El endpoint y la clave de publicación se entregan al backend como configuración y secreto de Container Apps; no se publican como output sensible ni se almacenan en Git.
- No se crearon suscripciones ni contratos técnicos por inferencia. Los consumidores, filtros y endpoints se agregarán cuando Core y los módulos involucrados los confirmen.
- Event Grid deberá reevaluarse frente a Service Bus antes de `test` o producción si los contratos futuros exigen semántica transaccional, orden estricto o detección de duplicados.
- Se incorporó una guía DevOps visual y autocontenida en PDF que explica desde cero la infraestructura, los pipelines, GitFlow, la operación y los pendientes, basada en la verificación posterior al despliegue.
- La guía DevOps se reescribió por completo para priorizar explicaciones causales, analogías y ejemplos del trabajo diario. La versión de 19 páginas conecta el cambio de código, CI, Docker, ACR, Terraform, autorizaciones, smoke tests, ambientes y ahorro de crédito sin asumir experiencia previa en infraestructura.

## 2026-09-08 — GitHub y bitácora incorporados a la guía DevOps

- La guía se amplió a 23 páginas con una explicación desde cero de repositorios, commits, ramas, Pull Requests, checks, merge y la diferencia entre GitHub y Azure.
- Se documentó el recorrido real de `feature/config-api-relativa` hacia `develop` y se verificó que Front ya publicó `develop`, mantiene abierto el PR #2 y fusionó el PR #3 de integración.
- Se verificó que Back mantiene abierto el PR #3 de API y migraciones PostgreSQL contra `develop`, con CI exitoso al 2026-09-08.
- Se incorporó una bitácora cronológica desde la elección de Azure hasta la coordinación actual con Front y Back, distinguiendo infraestructura comprobada, avances de desarrollo y pendientes.

## 2026-09-14 — Seguimiento de la bitácora DevOps

- Se volvió a verificar el estado de desarrollo: Front PR #2 y Back PR #3 continúan abiertos; Front PR #3 continúa fusionado.
- No se registró un nuevo despliegue ni una primera release hacia `test`.
- Se ajustó la segunda página de la bitácora del PDF para evitar recortes del encabezado en algunos visores y se actualizó su fecha de verificación.

## 2026-09-14 — Guía DevOps para memorizar

- Se conservó el PDF aportado por el usuario y se generó una versión nueva orientada a una exposición oral de cinco minutos.
- Se redujo el guion, se separó el contenido para memorizar del material de consulta y se eliminaron las indicaciones dirigidas a la diseñadora.
- Se completaron los diagramas para mostrar `Terraform plan`, la autorización de DevOps y la promoción de `develop` a `test` mediante `release/vX.Y.Z`.
- Se verificó el estado de Front PR #2, Front PR #3 y Back PR #3 al 2026-09-14, manteniendo explícitos los pendientes de aplicación, eventos y primera release.

## 2026-09-15 — Primera release desplegada en test

- Se fusionó Back PR `#3` en `develop`; el backend quedó en la imagen inmutable `b70379b077881a4b03ff4a4e5244d2f8195cf9a2`.
- Nadine otorgó permiso sobre Front. Se fusionaron los PR `#4` y `#5` en `develop`; la corrección `#5` agregó el proxy Nginx de `/api/*` hacia Azure. El frontend quedó en la imagen inmutable `9175534aa57e003caaebb7df2479f6e076c8e066`.
- Terraform CI validó formato, bootstrap, `development` y `test`. Los PR de infraestructura `#16` y `#17` fueron fusionados en `main`.
- DevOps revisó y autorizó el plan de actualización de `development`: primero 0 altas, 2 cambios y 0 bajas; luego 0 altas, 1 cambio y 0 bajas para corregir el proxy.
- Se verificaron en `development` frontend, backend, PostgreSQL, proxy `/api`, proyectos, órdenes, cuadrillas, recursos, cortes y tablero. Todos los endpoints consultados respondieron HTTP `200`.
- Se crearon `release/v0.1.0` en frontend y backend. Front PR `#6` y Back PR `#4` fueron fusionados en `main`; ambos repositorios publicaron el tag y la release `v0.1.0`. Back superó 13 pruebas y la construcción del contenedor.
- Se publicó la release de infraestructura `v0.1.0`. DevOps aprobó el plan de `test`, compuesto por 10 altas, 0 cambios y 0 bajas, y autorizó su aplicación.
- Azure `test` quedó con PostgreSQL 16, Event Grid, backend y frontend. El health directo y por proxy informó `database: up`, y los seis endpoints de consulta respondieron HTTP `200`.
- La validación es técnica y usa una base inicialmente vacía. La aceptación funcional del Product Owner y los flujos de escritura continúan pendientes.
- No se crearon suscripciones de Event Grid: faltan consumidores y contratos externos confirmados.
- Al finalizar las verificaciones, se detuvieron `psql-obras-publicas-dev-dfc86d` y `psql-obras-publicas-tst-3d2388`; ambos quedaron en estado `Stopped`. Azure puede reiniciarlos automáticamente después de siete días.

## 2026-09-15 — Criterios de defensa y flujo de órdenes de trabajo

- Se recibió el diagrama “Órdenes de Trabajo” con cinco posibles ingresos: proyecto, eventos de M6, eventos de M7, carga manual y corte de calle.
- Se registraron como criterios académicos recibidos la defensa individual, la demostración de un caso de uso, el uso explícito de un patrón de diseño en Back, la separación arquitectónica y MVC.
- La auditoría de la release `v0.1.0` confirmó capas Controller, Service, Repository, Mapper y Model en Back; esto acredita MVC y separación de responsabilidades, pero no demuestra una arquitectura de microservicios.
- Se verificó que la carga manual y la asociación de cortes con órdenes existen. El vínculo de una orden con un proyecto y los consumidores de eventos M6/M7 todavía no están implementados.
- Los nombres de eventos externos permanecen en estado `RECEIVED`, no `CONFIRMED`; no se generaron consumidores ni contratos ficticios.
- Se agregó un guion de defensa por rol y una demo repetible del ciclo manual de una orden en `development`.
- La demo se ejecutó contra Azure mediante el proxy del frontend: health confirmó PostgreSQL disponible y la orden de evidencia `id=1` llegó correctamente a `VALIDADA`.
