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

## 2026-09-19 — Formularios, aprobación y JWT desplegados en development

- Se revisaron y fusionaron Front PR `#7` y Back PR `#5` contra `develop` como una única entrega compatible.
- Front superó lint, 8 pruebas y build; Back superó tests, Flyway V1/V2 y empaquetado.
- El pipeline de imágenes pasó a consumir el repositorio oficial de Front y publicó los SHA inmutables `4c6ff95ca9a14609c2b595cc4bb86f77c58dcc6c` y `574a147ad81b2663462b05011ce56f65fab29104`.
- Terraform incorporó una contraseña aleatoria de aplicación y un secreto JWT. Ambos permanecen fuera de Git y se inyectan como secretos de Container Apps.
- DevOps revisó y autorizó el plan de `development`: 2 altas, 2 cambios y 0 bajas.
- El workflow `35475940801` aplicó correctamente el plan. PostgreSQL quedó `Ready`, y Front y Back quedaron `Running` con las imágenes nuevas.
- La prueba posterior confirmó frontend y `/health` HTTP `200`, `/api/health` con `database: up`, acceso anónimo protegido HTTP `401`, login JWT correcto y seis endpoints autenticados HTTP `200`.
- `test` no fue modificado: conserva la release `v0.1.0` hasta la siguiente promoción formal.

## 2026-09-20 — Release de aplicación v0.2.0 desplegada en Test

- Se fusionaron Front PR `#8` y Back PR `#6` en `develop`. Front superó lint, 10 pruebas y build; Back informó 60 pruebas H2, 60 PostgreSQL y 164 controles HTTP, y sus workflows de release volvieron a superar tests, empaquetado y construcción del contenedor.
- Se publicaron las imágenes inmutables de Front `5b4892b5668626aebbdef0c91900c69b7f78bdf5` y Back `91f30e4c7b5e03d0fd33fb831a30c63fae09ada3`. Desarrollo respondió HTTP 200 por Front, proxy `/api/health` y Back directo, con `database: up`.
- Se crearon `release/v0.2.0`, PR `#9` de Front y PR `#7` de Back; ambos se fusionaron a `main` y publicaron la release de aplicación `v0.2.0`.
- Terraform incorporó `AUTH_BOOTSTRAP_USERS` como secreto y cinco cuentas de prueba por rol. La contraseña se generó fuera de Git, se guardó como secreto protegido `TEST_DEMO_PASSWORD` del ambiente GitHub Test y se copió al portapapeles local para compartirla por un canal privado.
- Los intentos de infraestructura `v0.2.0` y `v0.2.1` se detuvieron antes del plan porque PostgreSQL estaba apagado y luego porque el output nuevo aún no existía en el estado anterior. No aplicaron cambios. El pipeline se corrigió para iniciar PostgreSQL antes del plan y derivar el nombre desde el FQDN persistido.
- La release operativa de infraestructura `v0.2.2` promovió las mismas aplicaciones `v0.2.0`. DevOps revisó un plan de 3 altas, 2 cambios y 0 bajas y autorizó el apply del workflow `35516745301`.
- Azure Test quedó disponible en `https://ca-obras-publicas-tst-frontend.purpleisland-1134bab8.chilecentral.azurecontainerapps.io`; Front y `/api/health` respondieron HTTP 200 y PostgreSQL informó `up`.
- Se probaron las cinco cuentas y sus roles mediante login y `/api/auth/me`. La prueba integrada creó proyecto `1`, comprobó denegación HTTP 403 con rol incorrecto, aprobó el proyecto, creó cuadrilla `1`, rechazó una orden PROYECTO sin `projectId` con HTTP 400 y recorrió la orden `1` por `ASIGNADA`, `EN_EJECUCION`, `PAUSADA`, `EN_EJECUCION`, `COMPLETADA` y `VALIDADA`.
- Se agregó un plan de Testing basado en el TPO y un guion separado de un minuto para la demostración. Las integraciones externas M2/M6/M7 y las brechas funcionales declaradas continúan pendientes; no se presentaron como implementadas.
## 2026-09-21 — Sexta cuenta de demostración en Test

- Se recibió un array JSON privado con seis cuentas, una más que las cinco previamente aprovisionadas.
- Se preparó Terraform para consumir `AUTH_BOOTSTRAP_USERS` desde el secreto `TEST_BOOTSTRAP_USERS` del environment GitHub `test`, sin almacenar credenciales en Git.
- El bootstrap del backend crea únicamente cuentas ausentes y no rota credenciales existentes. El workflow reinicia la revisión activa al actualizar el secreto para que tome efecto.
- La verificación de las seis credenciales desde el frontend queda sujeta al despliegue y a la evidencia de login; no se declara aprobada por el mero cambio de configuración.
- La release operativa `v0.2.6` finalizó con éxito en el workflow `35615302917`: Terraform aplicó 0 altas, 2 cambios y 0 bajas; `/api/health` informó `database: up`; los cinco logins anteriores pasaron con `TEST_DEMO_PASSWORD` y la sexta cuenta pasó con la clave privada de `users.json`. El reinicio manual de la revisión devolvió un error interno de Azure, pero la revisión activa ya había tomado el secreto y el smoke test fue exitoso.

## 2026-09-21 — Prueba exploratoria desde el navegador

- Se ejecutó el acceso real al Front de Test, registrado en `docs/entrega/ejecucion-testing-manual-2026-09-21.md`. La validación local de campos obligatorios pasó, pero el login con una cuenta válida devolvió HTTP 403 desde el navegador.
- La misma petición fue HTTP 200 sin `Origin` y HTTP 403 con el origen público del Front. Se registró una incidencia CORS bloqueante; los casos funcionales posteriores quedan pendientes hasta su corrección y nueva verificación desde la interfaz. Los smoke tests previos de API no se reinterpretan como pruebas de UI exitosas.

## 2026-09-21 — Corrección CORS y reprueba visual en Test

- PR `#35` agregó `CORS_ALLOWED_ORIGINS` en Terraform para el Front público de Test y reforzó los seis logins del pipeline con el encabezado `Origin`; las validaciones de Terraform pasaron.
- Release de infraestructura `v0.2.7`, workflow `35640984823`: plan 0 altas, 2 cambios in-place, 0 bajas; aplicación y smoke test finalizados correctamente.
- Desde navegador, `ingeniero.arquitecto` ingresó, navegó, consultó proyecto y orden existentes, filtró órdenes, recargó sesión y cerró sesión. Se registraron una carga inicial que requiere reintento, menú móvil solapado y etiqueta `development` en Test. El recorrido de los cinco roles operativos continúa pendiente; detalles en el informe de ejecución.

## 2026-09-21 — Segunda ejecución funcional por interfaz en Test

- Se comprobó el ingreso de los cinco perfiles operativos restantes y se continuó el caso de uso desde el Front público. Para recuperar la contraseña compartida sin publicarla se usó un workflow temporal que entregó solo texto cifrado; se retiró después (PR `#37` y `#38`). No se guardó la clave en documentación ni Git.
- Personal de Obras creó y presentó proyecto ficticio #2; Responsable Autorizado lo aprobó. Personal creó la OT #2 con origen Proyecto y vínculo #2. La falta de proyecto fue rechazada por el formulario. Jefe de Cuadrilla inició, pausó y reanudó la orden; Inspector pudo leerla, pero no validarla aún por su estado. Se creó un corte de prueba para la OT #2, que persistió en estado Pendiente.
- El navegador integrado no implementa `window.prompt()`, usado por el Front para Programar, Completar y Validar; esos pasos no se declararon aprobados. Se registraron además el detalle de proyecto desactualizado después de la mutación, la carga inicial intermitente del token, el menú móvil solapado y la etiqueta de ambiente confusa. La aceptación del flujo completo sigue pendiente. Evidencia y resultados por caso en `docs/entrega/ejecucion-testing-manual-2026-09-21.md`.
- Se actualizó el instructivo de Testing para incluir la sexta cuenta de ingeniería sin revelar contraseñas.

## 2026-09-21 — Corrección del Front y ciclo completo por interfaz

- Front PR `#10` corrigió los diálogos nativos de OT por formularios internos, la carga inicial del token, el detalle desactualizado, el menú móvil, la etiqueta de Test y la leyenda del indicador externo. Se añadió CI de Front; lint, pruebas, build y contenedor aprobaron.
- Infraestructura PR `#40` publicó la imagen corregida en Desarrollo. PR `#41` y release `v0.2.8` la promovieron a Test. El workflow `35646785528` terminó correctamente y comprobó los seis logins por el proxy público.
- En Test se creó la OT ficticia #3 asociada al proyecto #2. Jefe la programó, inició, pausó y reanudó; Operario la completó; Inspector la reabrió con motivo; Jefe y Operario repitieron el trabajo; Inspector la validó. Se comprobaron mensajes de campos obligatorios. La medición a 390 px mostró navegación sin solapamiento. Resultados y límites en `docs/entrega/ejecucion-testing-manual-2026-09-21.md`.
- La rama `release/v0.2.1` de Front integró `main`, pasó CI, se fusionó mediante PR `#11` y publicó la release `v0.2.1`. Su árbol de archivos coincide con la imagen inmutable ya probada en Test, aunque el commit de merge de Git es posterior. Las integraciones externas y demás brechas del TPO no se declaran implementadas por esta prueba.
- La reprueba agregó controles HTTP negativos en Test: 401 sin token, 403 para escritura de Operario, 400 para presupuesto negativo y 404 para proyecto inexistente; los recuentos no cambiaron. Tras recarga persistieron la OT #3 validada y el corte QA pendiente. El detalle queda en el informe de testing.
- Back PR `#8` sincronizó la rama por defecto `master` con `main`/release `v0.2.0` después de que CI superó pruebas, paquete Maven y construcción del contenedor (`35648259561`). Ambas ramas tienen el mismo árbol de archivos. Esta sincronización de Git no cambió la imagen de Back activa en Azure, que sigue siendo `91f30e4c7b5e03d0fd33fb831a30c63fae09ada3`.
- Se cerró la matriz QA-01 a QA-14 del alcance implementado. Siete rutas principales devolvieron 401 sin sesión; se comprobaron 403, 400 y 404 sin mutación. En móvil a 390 px se recorrieron las seis pantallas y el tráfico observado usó el proxy `/api` del Front. La aceptación de esta demo no implica que estén implementadas las integraciones externas ni las brechas funcionales pendientes del TPO.
