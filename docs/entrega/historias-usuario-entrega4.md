# Historias de usuario y requisitos trazables - Entrega 4

**Modulo:** M3 Obras Publicas
**Version documental:** 1.0
**Fecha de corte:** 2026-11-13
**Estado:** catalogo consolidado para QA y defensa. Las estimaciones son una propuesta de planificacion y requieren aceptacion del equipo.

Este documento reemplaza, para la entrega, las numeraciones parciales usadas en borradores anteriores. No elimina esos antecedentes. Cada historia se vincula con criterios de aceptacion, pruebas y evidencia en la matriz de trazabilidad.

## HU-01 - Iniciar sesion con permisos por rol

**Como** integrante del area de Obras, **quiero** iniciar sesion con mi cuenta, **para** acceder solamente a las funciones permitidas para mi rol.
**Prioridad:** P0. **Estimacion propuesta:** 3 puntos. **Estado QA:** PASS.

### Criterios de aceptacion

- **CA-01.1:** Dado un usuario activo y una clave valida, cuando inicia sesion, entonces recibe una sesion valida y ve el menu correspondiente a su rol.
- **CA-01.2:** Dada una clave incorrecta, cuando intenta ingresar, entonces recibe 401 y no se crea una sesion.
- **CA-01.3:** Dado un token expirado, manipulado o con algoritmo no permitido, cuando accede a un endpoint protegido, entonces recibe 401 sin revelar detalles sensibles.
- **CA-01.4:** Dado un usuario sin el rol necesario, cuando intenta una accion restringida, entonces recibe 403 y el recurso no cambia.

## HU-02 - Crear y presentar un proyecto de obra

**Como** personal de Obras, **quiero** registrar y presentar un proyecto, **para** iniciar su evaluacion administrativa.
**Prioridad:** P0. **Estimacion propuesta:** 5 puntos. **Estado QA:** PASS.

### Criterios de aceptacion

- **CA-02.1:** Dado un proyecto con datos validos, cuando se crea, entonces queda en borrador y persiste en PostgreSQL.
- **CA-02.2:** Dado un borrador completo, cuando se presenta, entonces queda pendiente de aprobacion.
- **CA-02.3:** Dado un presupuesto negativo o datos invalidos, cuando se intenta guardar, entonces la API responde 400 y no crea el proyecto.
- **CA-02.4:** Dado un identificador inexistente, cuando se consulta o modifica, entonces la API responde 404.

## HU-03 - Aprobar o rechazar un proyecto

**Como** responsable autorizado, **quiero** aprobar o rechazar proyectos presentados, **para** controlar que solo se ejecuten obras autorizadas.
**Prioridad:** P0. **Estimacion propuesta:** 5 puntos. **Estado QA:** PASS.

### Criterios de aceptacion

- **CA-03.1:** Dado un proyecto pendiente y una sesion RESPONSABLE_AUTORIZADO, cuando se aprueba con presupuesto y plazo validos, entonces queda aprobado y el cambio persiste.
- **CA-03.2:** Dado un proyecto pendiente, cuando se rechaza con motivo, entonces queda rechazado y conserva la auditoria.
- **CA-03.3:** Dado un usuario sin autorizacion, cuando intenta aprobar o rechazar, entonces recibe 403 y el proyecto no cambia.
- **CA-03.4:** Dada una repeticion del mismo comando con la misma Idempotency-Key y cuerpo, entonces se devuelve la respuesta original sin crear una segunda operacion.

## HU-04 - Ejecutar el ciclo de una orden de trabajo

**Como** equipo operativo, **quiero** crear, programar, iniciar, pausar, completar, reabrir y validar una orden, **para** registrar el trabajo de campo con un historial consistente.
**Prioridad:** P0. **Estimacion propuesta:** 8 puntos. **Estado QA:** PASS funcional; quedan controles manuales puntuales documentados.

### Criterios de aceptacion

- **CA-04.1:** Dado un proyecto aprobado, cuando se crea una orden, entonces queda vinculada una sola vez al proyecto.
- **CA-04.2:** Dada una orden y los roles habilitados, cuando se ejecutan transiciones validas, entonces el estado y la auditoria se actualizan.
- **CA-04.3:** Dada una orden en un estado incompatible, cuando se intenta una transicion invalida, entonces la API responde 409 y no muta la orden.
- **CA-04.4:** Dada una orden completada con observaciones, cuando el inspector la reabre, entonces vuelve al flujo operativo y conserva el historial.
- **CA-04.5:** Dada una orden corregida, cuando el inspector la valida, entonces queda VALIDADA.

## HU-05 - Asignar recursos a una orden

**Como** responsable operativo, **quiero** asignar cuadrillas, maquinaria y materiales a una orden, **para** planificar su ejecucion.
**Prioridad:** P1. **Estimacion propuesta:** 5 puntos. **Estado QA:** PASS para asignacion y carga. El control de stock se clasifica NO APLICA porque el modulo no administra inventario.

### Criterios de aceptacion

- **CA-05.1:** Dada una orden programable y una cuadrilla disponible, cuando se asigna, entonces se crea el vinculo y se actualiza su carga.
- **CA-05.2:** Dado un recurso ocupado o no permitido, cuando se intenta asignar, entonces se rechaza sin crear una asociacion invalida.
- **CA-05.3:** Dada una asignacion existente, cuando se consulta la orden, entonces los recursos permanecen vinculados despues de recargar.

## HU-06 - Coordinar cortes de calle con M7 Transito

**Como** responsable de una orden que afecta la via publica, **quiero** solicitar y seguir un corte de calle, **para** ejecutar la obra con autorizacion de Transito.
**Prioridad:** P0. **Estimacion propuesta:** 8 puntos. **Estado QA:** contrato y pruebas locales PASS; prueba bilateral real pendiente.

### Criterios de aceptacion

- **CA-06.1:** Dada una orden valida, cuando se solicita un corte, entonces se publica streetClosureRequested v1.0 con tramos estructurados.
- **CA-06.2:** Dada una aprobacion o rechazo de M7, cuando M3 consume el evento, entonces actualiza el estado y conserva correlationId y referencias.
- **CA-06.3:** Dado un corte ACTIVE cuyo endDate vencio, entonces M7 publica streetClosureEnded y M3 registra la finalizacion.
- **CA-06.4:** Dado un corte APPROVED nunca activado cuyo endDate vencio, entonces queda EXPIRED sin habilitar la orden.

## HU-07 - Atender tickets derivados por M2

**Como** personal de Obras, **quiero** recibir tickets de Atencion Ciudadana e informar su avance, **para** mantener al ciudadano actualizado sin perder la autoridad de estado de M2.
**Prioridad:** P0. **Estimacion propuesta:** 8 puntos. **Estado QA:** implementacion y pruebas locales PASS; bilateral M2 pendiente.

### Criterios de aceptacion

- **CA-07.1:** Dado ticketUpdated con responsibleAreaId distinto de M3, cuando se consume, entonces se confirma e ignora sin mutacion.
- **CA-07.2:** Dado un ticket ROUTED a M3, cuando comienza el trabajo, entonces se publica STARTED antes de PROGRESS.
- **CA-07.3:** Dado un PROGRESS fuera de secuencia, cuando M2 lo procesa, entonces lo rechaza sin dejar estados inconsistentes.
- **CA-07.4:** Dada una resolucion operativa, cuando M3 publica RESOLVED, entonces M2 valida y aplica la transicion correspondiente.

## HU-08 - Crear y cerrar ordenes originadas por M6 Ambiente

**Como** personal de Obras, **quiero** convertir solicitudes ambientales en ordenes y devolver su avance, **para** resolver reparaciones de infraestructura detectadas por M6.
**Prioridad:** P0. **Estimacion propuesta:** 8 puntos. **Estado QA:** PASS E2E M6-M3-Core.

### Criterios de aceptacion

- **CA-08.1:** Dado infrastructureRepairRequested, cuando M3 lo consume, entonces crea una sola orden y conserva requestId como sourceRequestId.
- **CA-08.2:** Cuando la orden se programa, entonces M3 publica workOrderScheduled con el mismo correlationId.
- **CA-08.3:** Cuando la orden se completa, entonces M3 publica workOrderCompleted con el mismo sourceRequestId.
- **CA-08.4:** Dado el mismo eventId repetido, cuando se recibe nuevamente, entonces Inbox evita una segunda mutacion.

## HU-09 - Vincular proyectos con expedientes de M1

**Como** responsable de Obras, **quiero** vincular un proyecto con su expediente administrativo, **para** registrar la resolucion institucional antes de continuar el flujo correspondiente.
**Prioridad:** P0. **Estimacion propuesta:** 8 puntos. **Estado QA:** escenario approved PASS E2E; variante rejected pendiente.

### Criterios de aceptacion

- **CA-09.1:** Dado un proyecto aprobado, cuando se publica publicWorksProjectApproved, entonces M1 crea el expediente usando publicWorksProjectId como referencia UUID.
- **CA-09.2:** Dado un dictamen approved, cuando M3 consume caseFileResolved, entonces registra caseFileId, numero y aprobacion sin duplicar el proyecto.
- **CA-09.3:** Dado un dictamen rejected, cuando M3 lo consume, entonces registra el rechazo como resultado valido y no lo interpreta como error tecnico.
- **CA-09.4:** Los eventos del mismo circuito conservan correlationId y usan referencias humanas solo en campos separados.

## HU-10 - Evitar operaciones REST duplicadas

**Como** cliente de la API, **quiero** reintentar comandos sin crear duplicados, **para** recuperarme de cortes de red de forma segura.
**Prioridad:** P0. **Estimacion propuesta:** 5 puntos. **Estado QA:** PASS.

### Criterios de aceptacion

- **CA-10.1:** Dado un POST con Idempotency-Key, cuando se repite con el mismo cuerpo, entonces devuelve la respuesta original y no crea otro recurso.
- **CA-10.2:** Dada una clave ya usada, cuando se reutiliza con otro cuerpo, entonces responde 409.
- **CA-10.3:** Si falla la transaccion de negocio, no queda una respuesta idempotente parcial ni una Outbox incoherente.

## HU-11 - Controlar ediciones concurrentes con ETag

**Como** usuario que modifica un recurso, **quiero** detectar si otra persona lo cambio antes, **para** no sobrescribir informacion mas reciente.
**Prioridad:** P1. **Estimacion propuesta:** 5 puntos. **Estado QA:** PASS.

### Criterios de aceptacion

- **CA-11.1:** Dado el ETag vigente, cuando se modifica con If-Match correcto, entonces se acepta y devuelve una nueva version.
- **CA-11.2:** Dado un ETag obsoleto, cuando se intenta modificar, entonces responde 412 con Problem Details y no aplica el cambio.

## HU-12 - Mantener eventos ante fallas del broker

**Como** operador del sistema, **quiero** que los eventos sobrevivan a fallas temporales, **para** no perder integraciones ni repetir efectos de negocio.
**Prioridad:** P0. **Estimacion propuesta:** 8 puntos. **Estado QA:** Inbox/Outbox y reintentos automatizados PASS; caida real coordinada con Core pendiente.

### Criterios de aceptacion

- **CA-12.1:** Dado un hecho persistido con broker caido, entonces el evento queda pendiente en Outbox con el mismo eventId.
- **CA-12.2:** Cuando el broker vuelve, entonces Outbox publica sin perdida y sin duplicado funcional.
- **CA-12.3:** Dado un evento duplicado, Inbox confirma sin repetir la mutacion.
- **CA-12.4:** Dado un payload invalido, entonces se aplica la politica de rechazo y DLQ definida por Core sin requeue infinito.

## HU-13 - Recibir asistencia de IA de forma segura

**Como** personal de Obras, **quiero** recibir una sugerencia de clasificacion y prioridad, **para** preparar una decision humana con mayor rapidez.
**Prioridad:** P1. **Estimacion propuesta:** 8 puntos. **Estado QA:** implementacion supervisada; requiere evidencia final del proveedor configurado y declaracion nominal de uso de IA.

### Criterios de aceptacion

- **CA-13.1:** Dada una consulta valida del dominio, cuando el proveedor responde dentro del timeout, entonces devuelve una sugerencia estructurada y revisable.
- **CA-13.2:** Dado un fallo o timeout del proveedor, entonces se usa un fallback seguro y la operacion principal no queda bloqueada.
- **CA-13.3:** Dado un pedido de secretos, datos personales, prompt injection o contenido fuera de Obras, entonces se rechaza o sanitiza sin revelar informacion.
- **CA-13.4:** La IA no crea, aprueba, asigna ni ejecuta obras u ordenes; una persona acepta o corrige la sugerencia.

## Requisitos no funcionales

- **RNF-01 Reproducibilidad:** una persona nueva puede configurar secretos fuera de Git y levantar el sistema desde cero con el procedimiento documentado.
- **RNF-02 Calidad continua:** CI, pruebas, cobertura, mutacion, SonarCloud, Gitleaks, Trivy y construccion Docker deben pasar sobre el commit entregado.
- **RNF-03 Seguridad:** no hay secretos en Git ni logs; se prueban autenticacion, autorizacion, CORS, headers, inyeccion, mass assignment y dependencias.
- **RNF-04 Rendimiento:** la prueba de carga cumple los umbrales definidos para p95 y errores.
- **RNF-05 Accesibilidad y responsive:** la interfaz se verifica en 360, 768 y 1280 px, sin desborde critico y sin hallazgos serios o criticos de accesibilidad.
- **RNF-06 Observabilidad:** health, logs, metricas y trazabilidad por eventId/correlationId permiten diagnosticar el circuito sin exponer secretos.

## Definition of Done usada para la entrega

Una historia se considera terminada cuando sus criterios estan trazados a casos ejecutados, la evidencia es accesible, los defectos estan registrados, CI esta verde, no hay secretos y el PO/QA acepta el resultado. Una integracion externa solo se marca E2E PASS con confirmacion del emisor, Core y receptor.
