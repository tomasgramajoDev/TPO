# Decisiones pendientes

**Corte de estado:** 15/11/2026. Este archivo enumera solo decisiones o pruebas realmente abiertas. Los acuerdos y pruebas cerrados se conservan en `decisiones-confirmadas.md` y en el historial de Git.

## Entrega académica y QA

1. Testing debe cerrar las evidencias manuales y los entregables requeridos: plan, matriz de trazabilidad, informe de ejecución, registro de defectos, informe de seguridad y declaración nominal de uso de IA.
2. Ejecutar la prueba guiada por el manual, la exploratoria y las comprobaciones pendientes de API, JWT, responsive y Lighthouse.
3. Reconciliar todos los defectos: cero Bloqueantes/Críticos abiertos y, como máximo, tres Mayores con workaround documentado.
4. Confirmar con la matriz de trazabilidad que todas las historias comprometidas el 03/11 están implementadas o registrar explícitamente la brecha y el plan de corrección.
5. Actualizar Jira con el cierre real de Gemini, las integraciones confirmadas y los bloqueos externos restantes.
6. Subir PDF, presentación y documentos QA a Teams antes del inicio de la clase; luego ensayar la demo y defensa individual.
7. Resuelto el 15/11 mediante PR #77: `compose.yaml` fija Back `a33873a56e25fb3406c1fcc11dfae5be71c8b0eb` y Front `918ce5d9a3b35f8fec091fe1fbbd0ccfa9af5dc0`, las revisiones desplegadas en Azure Test. El gate del PR `43779877210` quedó verde.
8. Los tags históricos `v1.0-testing` no se reescribieron. Los commits finales están identificados adicionalmente con `v1.0-testing-final` en Frontend, Backend e Infraestructura.

## DevOps y cloud

1. Aprobar costo y ventana antes de diseñar una salida IP estática con VNet/NAT Gateway. Azure Test funciona con allowlist de la salida observada, pero el Container Apps Environment actual no está integrado a una VNet.
2. Definir si existirá Producción y, en ese caso, su promoción, dimensionamiento, red privada, backups, recuperación, presupuesto y alertas.
3. Definir rollback de migraciones. Las imágenes ya son inmutables y la función de IA puede apagarse con feature flag o volver al proveedor `mock`.
4. Definir una política permanente de rotación de secretos técnicos y credenciales de módulos.

## Core Municipal

1. Ejecutar TC-022: publicar por HTTP un envelope sin `data`; el resultado esperado es HTTP 422 sin ingreso al hub ni a la DLQ.
2. Ejecutar TC-024: coordinar una caída real de RabbitMQ y verificar persistencia en Outbox, recuperación sin pérdida y deduplicación por `eventId`.
3. Mantener `maxAttempts=4` mientras no exista un acuerdo global diferente. La topología efectiva consultable en Core prevalece sobre documentos históricos.
4. Completar la migración del nombre histórico `streetClousureEnded` al nombre acordado `streetClosureEnded` sin cortar consumidores existentes.
5. Confirmar el catálogo final de publicaciones/suscripciones de M3 contra el mapa de Miro y adjuntar evidencia del ambiente compartido.

## Atención Ciudadana - M2

1. Core debe confirmar `ROUTED/DELIVERED`, cola, intentos y DLQ/retry para `STARTED` `e9d0e937-95c1-4999-83b3-ef1258c20b7b`, los dos `PROGRESS` y `RESOLVED` `c889727e-db9e-4bd6-a064-7ff1ad5b32b6`.
2. La prueba negativa de transición fuera de orden continúa como cobertura adicional, no como requisito para desconocer el circuito funcional ya confirmado por M2.
3. Conservar la autoridad de M2 sobre estado, prioridad y categoría. M3 solo informa hechos mediante `updateTicketStatus`.

## Ambiente - M6

No quedan pendientes contractuales para el circuito principal probado. La integración `infrastructureRepairRequested` -> `workOrderScheduled` -> `workOrderCompleted` está `CONFIRMED` por M3, M6 y Core, con correlación preservada, colas vacías y DLQ vacía.

Queda obtener la confirmación de M3/Core para `containerDamaged` (`eventId=748caf0e-6b47-4f35-998c-d1b77b8a1556`) y `treeRiskDetected` (`eventId=1ca257a6-9cc6-4686-82d6-ee23c194dcde`). M6 reenvió `containerDamaged` con el mismo `eventId`; falta evidencia de que Inbox lo deduplicó sin producir un segundo efecto.

## Tránsito - M7

1. El circuito funcional de corte ya llegó a M3: la solicitud `2d6893aa-9482-4dfd-98c3-85607f36bdab`, la aprobación `6f521edf-177f-43c4-b3ec-0a3eb1245fd5` y el cierre `c8479b39-4741-49f3-a3ea-f255d16416c2` conservaron `correlationId=afca371d-ddfd-497c-a437-f9152bef52bf`; Azure Test registró las dos respuestas como `PROCESSED`.
2. Core debe aportar la verificación de `ROUTED`/`DELIVERED`, intentos y DLQ para la aprobación y el cierre antes de elevar el circuito completo a `CONFIRMED`.
3. Ejecutar TC-017 de forma específica: un corte `ACTIVE` debe finalizar al vencer y emitir `streetClosureEnded`; uno `APPROVED` que nunca se activó debe pasar a `EXPIRED`. La prueba recibida no demuestra por sí sola cuál de esos disparadores produjo el cierre.
4. `roadAccidentRegistered` llegó con `eventId=9d7b06ec-dfa3-4ca6-9d28-acc17ed82523` y `correlationId=dca92b7c-b533-438e-99de-cebc6446d4ef`, pero M3 lo rechazó antes de Inbox en las cuatro entregas (5 s, 30 s y 2 min entre intentos). M7 y M3 deben cruzar el payload exacto con el contrato, corregir la incompatibilidad y repetir la prueba; Core debe confirmar el estado final y la DLQ.

## Ciudadanos y Expedientes - M1

1. Las variantes `approved` y `rejected` están `CONFIRMED`: Core verificó `ROUTED`/`DELIVERED`, M1 creó y resolvió los expedientes, y M3 registró ambas resoluciones.
2. Falta la prueba adicional de `publicWorksProjectCompleted` sobre el expediente existente de `OBRA-3` si ese evento continúa comprometido en el mapa del 03/11.
3. La migración futura al login central de M1, el mapeo de roles y la estrategia de firma/verificación de tokens quedan fuera del cierre funcional actual y requieren un acuerdo de arquitectura posterior.

## IA aplicada

1. La implementación ya no está pendiente: Gemini está activo en Azure Test detrás de `IncidentTriageGateway`, con salida estructurada, sanitización, revisión humana, timeout, circuit breaker, rate limit, feature flag y fallback manual.
2. Falta únicamente incorporar al paquete final y a los entregables de QA la evidencia del despliegue `v2.0-entrega4.3-gemini` y la declaración nominal de uso de Codex, Claude y Gemini.
3. Antes de promover la función a Producción se debe aprobar presupuesto, privacidad, límites de cuota y repetir el eval set contra la versión efectiva del modelo.

## Seguridad requerida en vivo

1. Ejecutar BOLA/IDOR sobre un recurso asociado a identidades diferentes o conseguir confirmación explícita de la cátedra de que no aplica al dominio. La justificación interna de “sin ownership” no reemplaza la prueba exigida por el profesor.
2. Ejecutar BFLA con un rol sin permiso y conservar el HTTP 403 y la ausencia de cambio de estado.
3. Ejecutar los cuatro JWT inválidos: vencido, firma alterada, `alg=none` y emisor incorrecto; todos deben devolver 401.
4. Preparar evidencia en vivo de mass assignment, inyección/XSS y rate limiting 429 sin bloquear las cuentas de demo.
5. Adjuntar el ZAP sin alertas High y el análisis de dependencias sin CVE críticas sin mitigar a la versión evaluada.

## Integración completa de la comisión

La entrega exige integración con Core y con los demás módulos del mapa de Miro, no solo que existan handlers locales.

1. M6: el flujo principal está confirmado, pero deben quedar trazados también los eventos secundarios comprometidos (`containerDamaged` y `treeRiskDetected`) mediante contrato y pruebas de consumidor.
2. M1: `approved` y `rejected` están confirmados; falta `publicWorksProjectCompleted` si figura en la matriz comprometida del 03/11.
3. M2: la transición válida está confirmada funcionalmente; falta únicamente la evidencia de transporte de Core y queda como cobertura adicional el rechazo fuera de orden.
4. M7: falta el circuito bilateral completo de cortes, rechazo, vencimiento y `streetClosureEnded`; también debe quedar verificado `roadAccidentRegistered` si continúa en el mapa.
5. Core: faltan las pruebas de envelope inválido y caída/recuperación del broker, además de reconciliar catálogo y nombre histórico del evento de cierre.
6. Dependencias del tercer checkpoint: confirmar JWT firmado/validado con M1. El login propio de M3 no demuestra esta dependencia; ambiente de Test y catálogo de Core deben quedar evidenciados.

## Testing y documentación exigidos

1. El código cumple actualmente 3 patrones con ADR (Strategy, State e Inbox/Outbox), 409 para transición inválida, Idempotency-Key, ETag y Problem Details; falta incorporar la evidencia final al paquete que se subirá.
2. Backend tiene más de 85% de líneas y más de 70% de ramas; Front alcanzó 85,66% de líneas. Deben adjuntarse los reportes de la versión evaluada.
3. Mutation score alcanzó 60%, Sonar Quality Gate está aprobado, Testcontainers ejecutó PostgreSQL en CI y la suite se repitió para detectar inestabilidad. Debe conservarse esa evidencia junto al tag evaluado.
4. BRD, documentación funcional, Gherkin, ADR, OpenAPI, justificación de SOAP no aplicable y manual existen; falta ejecutar una tarea al azar usando solamente el manual.
5. Regenerar el paquete final para incorporar Gemini, la evidencia del despliegue, los reportes actuales y esta auditoría; el ZIP del 11/11 quedó anterior a esos cambios.

## Dominio interno no bloqueante para esta entrega

1. Completar la matriz exhaustiva de transiciones menos frecuentes de `WorkOrder`, especialmente demoras y reprogramaciones.
2. Definir el tratamiento futuro de ampliaciones de obra y sus consumidores externos.
3. Aclarar con la cátedra si la exigencia de no monolito requiere microservicios desplegables o acepta el monolito modular actual con separación MVC y por capas.

## Cierres que no deben reabrirse sin evidencia nueva

- M6-M3-Core E2E: `CONFIRMED`.
- M1-M3-Core escenario `approved`: `CONFIRMED`.
- Envelope de Core, UUID, ISO 8601 con offset, correlación/causalidad y RabbitMQ compartido: implementados según los contratos vigentes.
- PostgreSQL, Flyway, CI/CD, Terraform, Azure Test, HSTS, CORS, análisis de secretos y SonarCloud: verificados.
- IA con Gemini: implementada y verificada en Azure Test; la clave no se versiona.
