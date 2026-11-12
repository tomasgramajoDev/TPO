# Decisiones pendientes

**Corte de estado:** 12/11/2026. Este archivo enumera solo decisiones o pruebas realmente abiertas. Los acuerdos y pruebas cerrados se conservan en `decisiones-confirmadas.md` y en el historial de Git.

## Entrega académica y QA

1. El tag exigido por la cátedra es `v2.0-entrega4` en `main`. Actualmente existe, pero antecede a Gemini y a correcciones posteriores. Como los commits posteriores no serán considerados, se debe publicar una referencia final antes de la clase sin perder el commit histórico original.
2. Testing debe cerrar las evidencias manuales y los entregables requeridos: plan, matriz de trazabilidad, informe de ejecución, registro de defectos, informe de seguridad y declaración nominal de uso de IA.
3. Ejecutar la prueba guiada por el manual, la exploratoria y las comprobaciones pendientes de API, JWT, responsive y Lighthouse.
4. Reconciliar todos los defectos: cero Bloqueantes/Críticos abiertos y, como máximo, tres Mayores con workaround documentado.
5. Confirmar con la matriz de trazabilidad que todas las historias comprometidas el 03/11 están implementadas o registrar explícitamente la brecha y el plan de corrección.
6. Actualizar Jira con el cierre real de Gemini, las integraciones confirmadas y los bloqueos externos restantes.
7. Subir PDF, presentación y documentos QA a Teams antes del inicio de la clase; luego ensayar la demo y defensa individual.
8. Mantener los tags históricos `v1.0-testing` sin reescribirlos. Los commits finales están identificados adicionalmente con `v1.0-testing-final` en Frontend, Backend e Infraestructura.

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

1. Ejecutar TC-019: `ticketUpdated` provoca `updateTicketStatus/STARTED` y luego `PROGRESS`; M2 debe confirmar ambas transiciones.
2. Ejecutar TC-020: enviar `PROGRESS` mientras el ticket continúa `ROUTED`; M2/Core deben confirmar rechazo, reintentos y resultado final.
3. Conservar la autoridad de M2 sobre estado, prioridad y categoría. M3 solo informa hechos mediante `updateTicketStatus`.

## Ambiente - M6

No quedan pendientes contractuales para el circuito probado. La integración `infrastructureRepairRequested` -> `workOrderScheduled` -> `workOrderCompleted` está `CONFIRMED` por M3, M6 y Core, con correlación preservada, colas vacías y DLQ vacía.

## Tránsito - M7

1. Ejecutar la prueba bilateral del circuito `streetClosureRequested` -> `streetClosureApproved`/`streetClosureRejected` -> `streetClosureEnded`.
2. Ejecutar TC-017: un corte `ACTIVE` debe finalizar al vencer y emitir `streetClosureEnded`; uno `APPROVED` que nunca se activó debe pasar a `EXPIRED`.
3. Registrar evidencia de `eventId`, `correlationId`, estados, entrega y DLQ. El contrato v1.0 y el nombre correcto `streetClosureEnded` ya están acordados.

## Ciudadanos y Expedientes - M1

1. Ejecutar la variante `rejected` del circuito `publicWorksProjectApproved` -> `caseFileResolved`.
2. La variante `approved` está `CONFIRMED`: Core verificó `ROUTED`/`DELIVERED`, M1 creó y resolvió el expediente, y M3 registró su asociación con el proyecto.
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
2. M1: `approved` está confirmado; faltan `rejected` y la evidencia de los demás eventos comprometidos, incluido `publicWorksProjectCompleted` si figura en la matriz del 03/11.
3. M2: faltan pruebas bilaterales de `ticketUpdated` y `updateTicketStatus`, incluida transición válida y rechazo fuera de orden.
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
