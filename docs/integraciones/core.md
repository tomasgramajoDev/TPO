# Integración con Core Municipal — Módulo 9

## Responsabilidad y contrato común

Core mantiene el hub técnico, el catálogo de eventos, las publicaciones, las suscripciones, el enrutamiento, los reintentos y la DLQ. No se presume consumidor funcional de todos los hechos: cada módulo conserva sus datos y reglas de negocio.

**Estado del contrato común usado por M3:** `CONFIRMED`.

El envelope vigente contiene `eventId`, `eventType`, `eventVersion`, `occurredAt`, `sourceModule`, `correlationId`, `causationId` cuando corresponde y `data`. Los identificadores técnicos son UUID, los nombres usan inglés y `camelCase`, y las fechas incluyen zona horaria. `data` siempre debe existir y ser un objeto.

M3 se conecta por AMQPS al vhost `core`, publica en `muni.inbox` y consume `q.obras`. El token de módulo HTTP no se utiliza para autenticar la conexión RabbitMQ. M3 no crea ni modifica topología desde la aplicación.

## Validación del envelope y alcance de TC-022

Core informó que `POST /api/v1/events` rechaza con HTTP `422` un envelope inválido antes de ingresarlo al hub. La comprobación concreta de omitir `data` por ese endpoint es una prueba contractual de la superficie HTTP de Core.

M3 publica sus eventos directamente por AMQP, no mediante `POST /api/v1/events`. Por eso TC-022 se clasifica `NO_APLICA_AL_CAMINO_AMQP_DE_M3`: no es una prueba pendiente de la integración desplegada de Obras ni corresponde inferir un `422` en un protocolo que no usa HTTP. Si la cátedra requiere demostrar el contrato HTTP de Core, debe ejecutarlo Core o un módulo autorizado para esa superficie y conservar su respuesta; eso no sustituye las validaciones locales del envelope ni las pruebas E2E AMQP de M3.

## Evidencia confirmada por circuito

### M6 → M3 → M6 — 2026-11-05/14

- `infrastructureRepairRequested` (`a53fc8ee-5200-4949-b333-480f21be7e5d`), `workOrderScheduled` (`8d109cc9-1802-4b30-89ea-0dd9df8b1843`) y `workOrderCompleted` (`916449bf-9cfb-4449-ae74-65b9825f7693`) quedaron `ROUTED`, conservaron la correlación y completaron el recorrido funcional. M6 informó el pedido cerrado; Core comprobó colas sin pendientes y DLQ vacía.
- `containerDamaged` (`748caf0e-6b47-4f35-998c-d1b77b8a1556`) y `treeRiskDetected` (`1ca257a6-9cc6-4686-82d6-ee23c194dcde`) fueron entregados a `q.obras` en un intento, sin retry ni dead letter, y M3 confirmó su procesamiento.
- La republicación exacta de `containerDamaged` fue reconocida como duplicada por Core y no generó una segunda entrega. Esto prueba la deduplicación de Core, no constituye por sí solo una prueba independiente del Inbox de M3.

### M3 → M1 → M3 — 2026-11-08/14

- Los escenarios `approved` y `rejected` de `publicWorksProjectApproved` → `caseFileResolved` v1.0 quedaron `ROUTED`/`DELIVERED` en un intento, sin DLQ, con correlación conservada y procesamiento funcional confirmado por M1 y M3.
- `publicWorksProjectCompleted` (`0da5fc0d-b656-4b70-b46d-e76ebb91517a`) quedó `ROUTED` y `DELIVERED` a `q.ciudadanos` en un intento, sin retry ni DLQ. M1 confirmó `OBRA-3` como `COMPLETED`, mantuvo el expediente `RESUELTO/approved` y no emitió otro `caseFileResolved`.

### M2 ↔ M3 — 2026-11-15/16

- M3 procesó `ticketUpdated` (`b99c2981-d7a5-476e-b748-23e31ed75647`) y publicó `STARTED`, dos `PROGRESS` y `RESOLVED` con la correlación original.
- M2 confirmó la aplicación funcional de los cuatro hechos y el ticket `TK-2026-000045` en estado `RESOLVED`.
- Core auditó `RESOLVED` (`c889727e-db9e-4bd6-a064-7ff1ad5b32b6`) como `ROUTED`, entregado a `q.atencion-ciudadana` en un intento, sin error, retry ni dead letter. Core observó los otros tres eventos bajo la misma correlación, pero no realizó la misma auditoría individual sobre cada uno; no se presenta esa observación como evidencia equivalente.

### M7 ↔ M3 — 2026-11-13/16

- El circuito base v1.1, `roadAccidentRegistered` y las variantes A/B/C de cortes quedaron confirmados por M3, M7 y Core.
- Para A/B/C, Core auditó siete eventos `ROUTED` y once entregas `DELIVERED` en el primer intento, sin errores, retry ni dead letters. Las respuestas conservaron la correlación y usaron como `causationId` el `eventId` de la solicitud.
- A terminó `REJECTED`; B terminó `ENDED` mediante cierre automático; C terminó `EXPIRED` sin `streetClosureEnded`, conforme al contrato.
- `roadAccidentRegistered` (`9d7b06ec-dfa3-4ca6-9d28-acc17ed82523`) fue recuperado mediante un único reintento manual de Core. M3 confirmó un único efecto funcional y la ausencia de DNI, patente, vehículos, personas e `inspectorId` en la persistencia minimizada.

## Infraestructura operativa

Azure Test mantiene una réplica mínima cuando la mensajería está habilitada. La evidencia de despliegue confirmó `MESSAGING_ENABLED=true`, health HTTP correcto, PostgreSQL disponible y conexión autenticada de `module_obras` al vhost `core`. Esta disponibilidad no sustituye la confirmación funcional del consumidor en cada prueba, que se documenta por circuito.

## TC-024 — recuperación aislada del publicador — 2026-11-16

Core dio el GO definitivo para ejecutar la simulación sin intervenir RabbitMQ compartido. M3 verificó Azure Test en modo `Single`, una revisión activa, una réplica y Outbox inicial sin pendientes. Con `SIMULATE_MESSAGING_FAILURE=true` creó un `streetClosureRequested` ficticio:

- `eventId`: `3f774fc5-bbd0-409e-a2ef-5af19ef2edb2`.
- `correlationId`: `7f6dd240-2fab-4052-884f-42f36e190c6f`.
- `closureRequestId`: `6e668b66-f886-4c80-b3a0-82622e19cb89`.

La operación funcional persistió la solicitud, la Outbox pasó a un pendiente y la revisión registró dos fallos de publicación para el mismo `eventId`. Antes de cambiar la bandera se detuvo únicamente el Container App de M3; Terraform restauró `SIMULATE_MESSAGING_FAILURE=false` y el despliegue `43935681337` terminó exitosamente. Azure volvió a `Running`, `Single`, una revisión, una réplica `Healthy`; la Outbox pasó a cero y el contador de publicados de `22` a `23`. El log registró `result=published` para el mismo `eventId` a las 16:08:31 ART.

M7 confirmó una única recepción, un único registro procesado y un único corte `REQUESTED`, sin duplicados, rechazos ni descartes, conservando `eventId`, `correlationId` y `closureRequestId`. Antes del restablecimiento había verificado cero registros con esos identificadores. La prueba acredita la recuperación del publicador de M3; no equivale a una caída del broker compartido.

## Pendientes que permanecen abiertos

- Completar la migración coordinada del registro histórico `streetClousureEnded` al nombre vigente `streetClosureEnded` sin cortar consumidores.
- Reconciliar el catálogo final de publicaciones y suscripciones contra el mapa comprometido.
- Obtener el contrato completo de respuesta y errores de `POST /api/v1/auth/module-token` si M3 debe consumir APIs HTTP de Core.
- Mantener como fuente de verdad operativa `GET /api/v1/topology` para TTL y topología efectiva, sin copiar números históricos como configuración vigente.
