# Decisiones pendientes

## DevOps y cloud

1. Definir la estrategia de migraciones, la red privada y el dimensionamiento de PostgreSQL para `test`/producción.
2. Event Grid queda elegido para distribuir eventos discretos en `development`. Reevaluar Service Bus para `test`/producción si los contratos confirmados requieren orden estricto, transacciones o detección de duplicados.
3. Definir IAM de usuarios de aplicación, certificados, copias de seguridad y recuperación. Los secretos técnicos de `development` ya se entregan mediante Container Apps y Terraform.
4. Confirmar si existirá ambiente de producción y, en ese caso, su flujo de promoción y aprobación.
5. Definir estrategia de rollback funcional y tratamiento de migraciones. El versionado actual de imágenes por SHA ya es inmutable.
6. Establecer el presupuesto mensual y los umbrales de alertas.
7. Adoptar formalmente una Definition of Done del equipo y decidir qué controles serán bloqueantes en CI/CD.
8. Decidir si el futuro ambiente de producción utilizará feature flags y si una historia puede considerarse terminada estando desplegada pero desactivada.
9. Definir cómo se generan, revisan y publican las release notes.
10. Confirmar la herramienta y dinámica de coordinación entre equipos; Nexus, SAFe y el modelo Spotify aparecen como material docente, no como elección del proyecto.
11. Mantener sincronizados Front, Back e infraestructura después de la incorporación de los PR de la primera release; ya no se depende del fork para publicar Front.
12. Completar los casos funcionales aún ausentes del backend: vínculo proyecto–orden, creación por eventos externos confirmados y cobertura integral de reglas del backlog.

## Core Municipal

1. Confirmar nombres, tipos y obligatoriedad del envelope común.
2. Definir zona horaria, formato de fechas, versiones, correlación y causalidad.
3. Precisar el rol de Core como hub técnico sin convertirlo en consumidor funcional de todos los eventos.
4. Acordar idempotencia, reintentos, auditoría y DLQ.
5. Confirmar casing de entidades, endpoints y errores técnicos.
6. Confirmar con M9 las referencias a UUID, ISO 8601, versión y JSON Schema incluidas en la matriz del PO.

## Atención Ciudadana

1. Confirmar `complaintRouted` y `complaintEscalated` o sus nombres definitivos.
2. Acordar payloads y campos obligatorios/opcionales.
3. Definir si la correlación usa `ticketId` u otro identificador.
4. Elegir qué estados de `WorkOrder` consume M2.
5. Definir si el reclamo se cierra con `workOrderCompleted` o `workOrderValidated` y cómo se trata una reapertura.
6. Confirmar si M2 consume `workOrderPaused`, agregado por la matriz del PO.

## Ambiente, Higiene y Servicios Urbanos

1. Confirmar nombres definitivos y casing de `infrastructureRepairRequested`, `containerDamaged` y `treeRiskDetected`.
2. Confirmar payloads tentativos, tipos, enums y estructura de `location`.
3. Definir correlación de órdenes originadas por `containerDamaged`.
4. Definir correlación de órdenes originadas por `treeRiskDetected` (`treeId`, `surveyCode` u otro ID).
5. Aclarar si `treeRiskDetected` solo se emite para `HIGH`/`CRITICAL` o si esos niveles son únicamente prioridad de consumo.
6. Confirmar si M6 cierra con `workOrderCompleted` o espera `workOrderValidated`.
7. Resolver `outcome` vs `result` y `attachments[]` vs `evidence` en el payload de respuesta.
8. Confirmar respuesta esperada para `containerDamaged` y `treeRiskDetected`.
9. Resolver con el PO y M6 la reaparición de `urbanRiskDetected` y `urbanServiceRepairRequested` frente a los eventos específicos comunicados directamente por M6.

## Tránsito

1. Confirmar nombres y payloads de `trafficIncidentRegistered`, `streetClosureRequested`, `streetClosureAuthorized` y `streetClosureRejected`.
2. Acordar modelo de calles, tramos y ubicación.
3. Definir identificadores, períodos, condiciones, desvíos, extensiones y vencimientos.
4. Precisar qué ocurre con una orden ante rechazo, vencimiento o cambio de autorización.
5. Definir cómo se representan los desvíos mencionados en la descripción de `streetClosureRequested` pero ausentes de su payload explícito.
6. Confirmar si `workOrderCreated.publicWorksProjectId` es obligatorio para órdenes originadas por incidentes viales.

## Ciudadanos y Expedientes Digitales

1. Confirmar `caseFileResolved`, su payload y resultados que habilitan o bloquean una obra.
2. Definir qué eventos del ciclo de la obra necesita realmente M1.
3. Acordar correlación y manejo de documentación administrativa.
4. Confirmar si M1 consume `publicWorksExtensionRequested`, `publicWorksExtensionApproved` y `publicWorksExtensionRejected`, agregados por la matriz del PO.
5. Definir si `publicWorksProgressRegistered` usa `stageId`, `milestoneId` o ambos.

## Dominio interno aún no cerrado

1. Completar la matriz exhaustiva de transiciones de `WorkOrder`, especialmente `PAUSED`, `DELAYED`, `REOPENED` y reprogramaciones.
2. Definir si `sourceRequestId` es un campo universal o si se requieren identificadores de origen tipados por integración.
3. Confirmar consumidores de `publicWorksExtensionRequested`, `publicWorksExtensionApproved` y `publicWorksExtensionRejected`.
4. Aclarar con la cátedra si “no aplicación monolítica” exige microservicios desplegables de manera independiente o si se acepta un monolito modular con separación MVC. El backend actual cumple separación por capas, pero se despliega como un único servicio Spring Boot.
5. Definir y acordar el vínculo entre `WorkOrder` y `PublicWorksProject`: cardinalidad, obligatoriedad de `projectId`, comportamiento de órdenes independientes y migración de datos.

## Contradicciones y diferencias detectadas

| Tema | Versiones en tensión | Tratamiento actual |
| --- | --- | --- |
| Eventos de M6 | El alcance anterior usa `urbanRiskDetected` y `urbanServiceRepairRequested`; M6 comunica `treeRiskDetected`, `infrastructureRepairRequested` y además `containerDamaged`. | Se actualiza el catálogo activo con lo recibido y se conserva el reemplazo en el historial. |
| Matriz del PO vs comunicación de M6 | La nueva matriz del PO vuelve a listar `urbanRiskDetected` y `urbanServiceRepairRequested`, y omite los tres eventos específicos de la comunicación directa de M6. | Conservar ambas fuentes como `RECEIVED`; la línea interna sigue usando los eventos específicos, pero la definición externa queda pendiente. |
| Naming de M6 | El PDF de M6 muestra nombres en PascalCase; el acuerdo general exige eventos en `camelCase`. | Se documentan en `camelCase` como convención vigente, pero el contrato sigue `RECEIVED`. |
| Cierre para M6 | El alcance asigna cierre definitivo a `workOrderValidated`; M6 pide `workOrderCompleted` para cerrar automáticamente. | No se elige; decisión externa pendiente. |
| Payload de finalización | Alcance: `result`/`evidence`; M6: `outcome`/`attachments[]`. | Mantener ambas propuestas hasta acordar el contrato. |
| Rol de Core | El TPO lo llama hub que recibe eventos; el acuerdo vigente dice que no es consumidor funcional por defecto. | Distinguir enrutamiento técnico de consumo funcional y confirmar con M9. |
| Riesgo de arbolado | M6 indica disparo `HIGH`/`CRITICAL`; la instrucción vigente agrega procesamiento solo si `requiresPublicWorks = true`. | Documentar ambas condiciones y pedir precisión sobre emisión vs consumo. |
| Eventos originales | El TPO usa nombres funcionales en español y PascalCase; el catálogo actual usa inglés y `camelCase`. | Tratar los nombres originales como antecedente, no como contrato técnico vigente. |
| Cierre de reclamo M2 | La matriz del PO afirma que `workOrderValidated` concluye definitivamente el reclamo; antes se mantenía abierto entre `workOrderCompleted` y `workOrderValidated`. | Registrar la definición como `RECEIVED` y pedir confirmación a M2. |
| Eventos de ampliación hacia M1 | La matriz del PO incluye los tres `publicWorksExtension*`; la lista anterior para Expedientes no los incluía. | Mantenerlos `RECEIVED` para esa ruta y confirmar con M1. |
| Payload de progreso | La documentación anterior expresaba `stageId` o `milestoneId`; la matriz del PO lista ambos. | Confirmar cardinalidad y obligatoriedad con M1/Core. |
| Convenciones Core | La matriz del PO menciona UUID, ISO 8601, versión y JSON Schema; las convenciones exactas seguían pendientes de Core. | Registrar como `RECEIVED`, sin fijarlas como definitivas hasta confirmación de M9. |
| Evento al crear borrador | El backlog recibido indica que no se publica un evento al crear el borrador; la matriz del PO y el catálogo `RECEIVED` incluyen `publicWorksProjectCreated`. | No publicar ni retirar el evento por inferencia; confirmar con PO, M1 y Core. |
| Ingreso desde M2 | Un ciclo usa `ticketCreated`; el catálogo vigente usa `complaintRouted`. | Mantener `complaintRouted` como nombre documentado y pedir a M2 el contrato definitivo. |
| Respuesta de corte de calle | Un ciclo usa `streetClosureApproved`; el catálogo vigente usa `streetClosureAuthorized`. | Mantener ambas variantes registradas y confirmar con M7/Core. |
| Actualización de reclamo | El ciclo de órdenes invoca `updateTicketStatus`, pero ese identificador no figura en el catálogo vigente. | Tratarlo como operación ilustrativa, no como contrato implementable, hasta definir API o evento con M2. |
| Finalización e inspección de orden | El backlog ubica el `workOrderCompleted` definitivo después de la inspección; el ciclo y catálogo separan finalización operativa, `workOrderValidated` y `workOrderReopened`. | No unificar los hechos. Confirmar quién emite cada evento y cuál cierra el proceso externo. |
| Aplicación móvil | El backlog menciona “App Móvil”; el alcance confirmado excluye una aplicación móvil independiente y define portal web responsive. | Mantener portal responsive como alcance vigente; pedir autorización explícita si se requiere una app independiente. |
