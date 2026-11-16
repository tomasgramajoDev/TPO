# Evidencia final de seguridad y resiliencia — Entrega 4

**Corte:** 16 de noviembre de 2026

**Candidata operativa TC-024:** tag `v2.0-entrega4.10-tc024-ready`

**Backend:** `b07d38079c2feb7c1b1ca18b1974e28bc335a9af`

**Frontend:** `ab2970fec6fd1001468049e152262d42d3109f33`

Este documento consolida controles comprobados y limita expresamente lo que todavía requiere una demostración humana. No contiene usuarios, contraseñas, tokens ni claves.

## Resultado ejecutivo

- **Seguridad automatizada:** PASS. JWT, BFLA, rate limiting, validaciones, mass assignment, ETag, idempotencia y Problem Details tienen regresiones aprobadas.
- **Seguridad de la candidata:** PASS con observaciones menores. Gitleaks no detectó secretos y ZAP informó `0` alertas High/Critical; permanecen una alerta Medium y una Low documentadas.
- **Resiliencia de aplicación:** PASS. Timeout/fallback, rollback, Inbox/Outbox, deduplicación, orden por clave, confirmaciones AMQP y reintento con el mismo `eventId` tienen pruebas aprobadas.
- **Resiliencia operativa:** PASS. TC-024 inyectó una indisponibilidad aislada antes de `RabbitTemplate.send` solo en Azure Test, sin intervenir el broker compartido. La operación funcional se conservó, la Outbox quedó pendiente, registró dos fallos y publicó el mismo `eventId` después del restablecimiento. M7 confirmó una única recepción y un único efecto funcional.

## Ejecución reproducida el 16/11

Se ejecutaron en limpio las suites críticas del Backend:

```text
AuthApprovalReviewTests                         14 PASS
DeliveryFourCriteriaTests                       5 PASS
EventIntegrationFoundationTests                12 PASS
IdempotencyKeyFilterTransactionTests            1 PASS
RabbitEventTransportTests                       3 PASS
ResilientIncidentTriageGatewayTest              2 PASS
TOTAL                                           37 PASS
Fallos / errores / omitidas                     0 / 0 / 0
```

El CI completo del Backend `43929457968` aprobó `145` pruebas, JaCoCo, SonarCloud Quality Gate, mutation testing, Gitleaks, Trivy y la construcción del contenedor. El Frontend `43928900864` aprobó `65` pruebas, lint, cobertura, E2E, accesibilidad, build y contenedor.

## Matriz de seguridad

| Control | Resultado | Evidencia | Riesgo / acción |
| --- | --- | --- | --- |
| Autenticación obligatoria | PASS | Sin token y token manipulado devuelven `401` uniforme en `AuthApprovalReviewTests`. | Ninguno abierto. |
| JWT vencido, firma alterada, `alg=none` e issuer incorrecto | PASS | Cuatro regresiones de `AuthApprovalReviewTests`; issuer también fue verificado en Azure Test el 15/11. | No almacenar los tokens de prueba. |
| BFLA / autorización por función | PASS | Un rol no aprobador recibe `403`; `SecurityConfig` limita cada transición por rol. | Repetir un caso al azar en la defensa. |
| BOLA / IDOR por propietario | NO APLICA | El modelo municipal no asigna propiedad individual de proyectos u órdenes. La autorización vigente es por rol, no por `ownerId`. | Explicarlo así; no presentar un PASS inventado. |
| Mass assignment | PASS | La edición general con `approvedBudget` o `approvedDeadlineDays` devuelve `422`; los términos aprobados permanecen intactos. La prueba histórica de Azure con `status`, `role` y `owner` dejó el proyecto en `BORRADOR`. | Conservar captura sanitizada de Azure en el paquete QA. |
| SQL injection / XSS | PASS | La prueba histórica de Azure trató el payload como texto literal, sin ejecutar script ni SQL. El smoke `demo-security-live.ps1` rechaza exposición de errores internos. | Repetir solo con datos ficticios. |
| Fuerza bruta | PASS | `LoginRateLimitFilter`; regresión con `429`, `RATE_LIMITED` y `Retry-After`. | No bloquear una cuenta de demo durante la exposición; usar cuenta descartable. |
| Validaciones y Problem Details | PASS | Requests inválidos producen `400/401/403/409/412/422` coherentes, sin stack trace. | Ninguno abierto. |
| Concurrencia e idempotencia REST | PASS | `Idempotency-Key` devuelve replay, impide reutilizar la clave con otro cuerpo y crea un solo recurso bajo concurrencia. | Ninguno abierto. |
| ETag / actualización perdida | PASS | ETag vigente avanza la versión y uno obsoleto devuelve `412 PRECONDITION_FAILED`. | Ninguno abierto. |
| CORS y headers | PASS con observaciones | Evidencia live en Azure; ZAP del tag final no registró High/Critical. | Documentadas CSP `unsafe-inline` Medium y versión de servidor Low. |
| Secretos | PASS | Gitleaks sobre historial completo en el workflow del tag final. `.env.example` no contiene valores reales. | Mantener secretos únicamente en GitHub/Azure. |
| Dependencias e imagen | PASS | Trivy Backend sin vulnerabilidades bloqueantes; Front sin High/Critical productivas. | Revisar periódicamente tooling de desarrollo. |
| AMQPS | PASS | TLS y hostname verification obligatorios; sin contraseña o con TLS deshabilitado el arranque falla. La topología pertenece a Core. | No crear colas/exchanges desde M3. |

## Matriz de resiliencia

| Escenario | Resultado | Evidencia | Límite honesto |
| --- | --- | --- | --- |
| Proveedor IA lento o caído | PASS | Timeout por defecto de `5 s`, fallback y circuit breaker en `ResilientIncidentTriageGatewayTest`. | El fallback no ejecuta cambios de negocio. |
| Publicación AMQP recibe nack/return | PASS | `RabbitEventTransportTests`: no se marca publicado y no se filtra el mensaje privado del broker. | Prueba con doble del cliente. |
| Publicador sin transporte hacia el broker | PASS live controlado | TC-024: `streetClosureRequested` `3f774fc5-bbd0-409e-a2ef-5af19ef2edb2`; Outbox `0 → 1 → 0`, dos fallos registrados, luego `published` con el mismo `eventId`. M7 comprobó una recepción, un corte `REQUESTED` y cero duplicados. Workflow de restauración `43935681337` exitoso. | La prueba valida la recuperación del publicador de M3; no simula una caída real del RabbitMQ compartido. |
| Transacción funcional falla | PASS | Rollback conjunto del efecto de negocio, reserva idempotente y Outbox. | Ninguno abierto. |
| Consumidor interrumpido | PASS | El Inbox persistido retoma el evento pendiente. | Ninguno abierto. |
| Mensaje duplicado/concurrente | PASS | Dos consumidores producen un único efecto; el segundo resultado es `duplicated`. | La deduplicación adicional de `containerDamaged` ocurrió en Core antes de llegar a M3. |
| Error técnico del handler | PASS | Efectos revertidos, Inbox queda `TECHNICAL_ERROR` y el envelope persistido puede reintentarse. | Ninguno abierto. |
| Rechazo de negocio | PASS | Efectos revertidos y resultado terminal, sin bucle de reintentos. | Ninguno abierto. |
| Mensaje inválido en listener | PASS | `nack(requeue=false)` y sin `ack`. Core gestiona DLQ/reintentos. | No existe DLQ propia de M3. |
| Disponibilidad del consumidor | PASS live | Azure Test conserva `minReplicas=1` con mensajería activa; conexión `module_obras` comprobada. | La allowlist de IP sigue siendo una dependencia operativa de Core. |
| Recuperación real de entrega | PASS externo | Core reintentó una única dead letter de `roadAccidentRegistered` conservando `eventId`; M3 confirmó un único procesamiento y una única proyección, sin datos personales persistidos. | Fue recuperación administrativa, no outage deliberado. |

## Gate obligatorio del tag

El workflow `Testing release gates`, disparado por `v2.0-entrega4`, verifica:

- Arranque limpio: `138 s` (límite: 15 minutos).
- Gitleaks: aprobado.
- ZAP: `0` High/Critical; 1 Medium, 1 Low y 2 informativas documentadas.
- k6: `50` VUs durante `301,3 s`, `44.695` requests, p95 `8,03 ms`, tasa de fallos `0` y checks `100%`.

La ejecución concreta se consulta en GitHub Actions filtrando por la rama/tag `v2.0-entrega4`: <https://github.com/tomasgramajoDev/TPO/actions/workflows/testing-release.yml>

## Riesgos abiertos y aceptados

| ID | Clasificación | Estado | Tratamiento |
| --- | --- | --- | --- |
| SR-01 | Operativo | MITIGADO | Core es compartido y no se detuvo. TC-024 demostró de forma aislada la conservación y recuperación de la Outbox de M3, con coordinación de Core y confirmación funcional de M7. |
| SR-02 | ZAP Medium | ACEPTADO | `style-src 'unsafe-inline'`; no habilita scripts inline. Migrar estilos a nonce/hash fuera de esta entrega. |
| SR-03 | ZAP Low | ACEPTADO | Header de servidor expone versión. Ocultarlo en una mejora posterior de proxy. |
| SR-04 | Dependencia externa | MITIGADO | La IP de salida AMQPS puede cambiar; `minReplicas=1`, monitoreo y procedimiento de allowlist reducen el riesgo. |

## Actividades pendientes para la exposición

No son faltantes de código:

1. Ejecutar un caso BFLA y un JWT inválido elegido por el profesor.
2. Explicar por qué BOLA/IDOR por propietario es `NO APLICA` en este dominio.
3. Mostrar la recuperación de Outbox con la evidencia de TC-024 y aclarar que se simuló la falla del publicador de M3, no una caída del broker compartido.
4. Mantener credenciales, tokens y headers `Authorization` fuera de pantalla y de las capturas.

## Veredicto

**SEGURIDAD Y RESILIENCIA: LISTAS PARA ENTREGA, CON OBSERVACIONES DOCUMENTADAS.** No hay un bloqueo técnico conocido en estos dos ejes. Permanece únicamente la ejecución presencial elegida por la cátedra; no se debe interrumpir RabbitMQ compartido.
