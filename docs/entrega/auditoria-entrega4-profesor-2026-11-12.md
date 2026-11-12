# Auditoría contra la 4.ª Entrega Obligatoria

**Fecha de control:** 12/11/2026  
**Clase:** martes 17/11/2026  
**Criterio:** se distingue `CUMPLE`, `PARCIAL`, `PENDIENTE` y `BLOQUEANTE`. Ningún “CUMPLE” se basa solamente en una afirmación generada por IA.

## Resumen honesto

La aplicación, infraestructura, base de datos, CI, patrones, controles REST, cobertura, seguridad automatizada e IA están implementados. La entrega completa todavía no está cerrada: faltan integración bilateral con M2 y M7, variante M1 `rejected`, pruebas de resiliencia coordinadas con Core, JWT central de M1, pruebas de seguridad manuales y el cierre formal de QA/Teams. El tag obligatorio `v2.0-entrega4` quedó anterior a cambios que se pretenden presentar.

## Condiciones de admisión

| Condición | Estado | Evidencia o acción faltante |
| --- | --- | --- |
| Arranque con un comando y README, menos de 15 minutos | CUMPLE | Gate de clean start aprobado; tiempo registrado muy por debajo de 15 minutos. |
| Tag `v2.0-entrega4` en `main` | BLOQUEANTE | Existe desde el 10/11, pero no contiene Gemini ni cambios posteriores. Los commits posteriores no cuentan según la cátedra. |
| CI verde sobre la versión evaluada | PARCIAL | Los CI actuales están verdes; debe reconciliarse la referencia final con el tag obligatorio. |
| Jira al día | PARCIAL | Actualizado al 11/11; falta incorporar Gemini, auditoría final e integraciones pendientes. |
| Sin secretos en el historial | CUMPLE | Gitleaks y scans aprobados; claves entregadas como secretos de GitHub/Azure. |
| Demo en vivo E2E | PENDIENTE | Aplicación accesible; falta ensayo y seleccionar el circuito definitivo. |
| Declaración de IA | PARCIAL | Documento preparado; faltan revisión/firma nominal y subida a Teams. |
| Informe honesto de defectos | PENDIENTE | Testing debe cerrar clasificación y límites de severidad. |
| Documentación/presentación en horario | PENDIENTE | Falta carga final en Teams. |

## Eje A - Historias y documentación

| Requisito | Estado | Observación |
| --- | --- | --- |
| Historias comprometidas el 03/11 | NO VERIFICABLE | Requiere matriz HU -> criterio -> caso -> resultado -> evidencia sin huecos. |
| BRD y documentación funcional | CUMPLE | Versionados en `docs/entrega`. |
| Historias en Gherkin | CUMPLE | Incluyen dominio, REST, resiliencia e IA. |
| Tres ADR y State | CUMPLE | Strategy, State, Inbox/Outbox y ADR de IA. |
| Manual de usuario | PARCIAL | Existe; falta prueba humana de tarea aleatoria usando solo el manual. |
| OpenAPI | CUMPLE | `/v3/api-docs` y Swagger verificados. |
| WSDL | NO APLICA | M3 no expone ni consume SOAP; la justificación está documentada. |
| QA: plan, matriz, ejecución y defectos | PENDIENTE | Delegado a Testing; debe cerrarse y subirse. |

## Eje B - Código y pruebas

| Requisito | Estado | Evidencia |
| --- | --- | --- |
| Backend >=85% líneas | CUMPLE | 90,04% de líneas en el control vigente. |
| Backend >=70% ramas | CUMPLE | 71,64% de ramas. |
| Front >=85% | CUMPLE | 85,66% de líneas; 85,41% statements. |
| Mutation score >=60% | CUMPLE | 32/53 mutaciones, 60%; test strength 82%. |
| Sonar Quality Gate | CUMPLE | Pipeline actual aprobado. |
| Testcontainers | CUMPLE | PostgreSQL 17 ejecutó 2 pruebas sin skips en el paso principal de CI. |
| API y contratos | CUMPLE | Suites REST, schemas y handlers ejecutadas. |
| Sin flaky tests | CUMPLE CON EVIDENCIA | La suite de 127 tests se repitió dos veces en CI, sin fallos ni skips. |

## Eje C - Integración y resiliencia

| Requisito | Estado | Faltante |
| --- | --- | --- |
| Timeout 5 s y fallback | CUMPLE | Gateway de IA y fallback manual. |
| Broker caído sin pérdida | PENDIENTE | TC-024 real con Core; Outbox está implementada pero falta evidencia coordinada. |
| Consumidor idempotente | CUMPLE EN CÓDIGO | Inbox por `eventId`; falta ampliar evidencia externa a todos los flujos. |
| DLQ | PARCIAL | Core y M6 mostraron DLQ vacía; falta prueba deliberada de rechazo/reintento. |
| Outbox/rollback | CUMPLE EN CÓDIGO | Falta TC-024 para cierre operativo. |
| Idempotency-Key y ETag | CUMPLE | Casos automatizados y 409/412. |
| Problem Details | CUMPLE | Errores REST normalizados. |
| Carga 50 usuarios, p95 <500 ms | CUMPLE | k6: p95 6,35 ms y 0% errores en la evidencia vigente. |
| M6-M3-Core | CUMPLE PARCIAL DEL MAPA | Flujo principal confirmado; revisar eventos secundarios comprometidos. |
| M1-M3-Core | PARCIAL | `approved` confirmado; faltan `rejected` y eventos restantes del mapa. |
| M2-M3-Core | PENDIENTE | No existe prueba bilateral cerrada. |
| M7-M3-Core | PENDIENTE | No existe prueba bilateral cerrada. |
| Envelope sin `data` | PENDIENTE | TC-022 con Core. |

## Eje D - Seguridad

| Requisito | Estado | Observación |
| --- | --- | --- |
| BOLA/IDOR en vivo | BLOQUEANTE HASTA ACLARAR | El sistema no modela ownership; el profesor exige prueba. Probar un recurso entre identidades o consultar públicamente la excepción. |
| BFLA | CUMPLE/PREPARADO | Acciones de otro rol devuelven 403 sin cambio de estado. Debe mostrarse en vivo. |
| JWT inválidos | PENDIENTE MANUAL | Vencido, firma alterada, `alg=none` y emisor incorrecto deben devolver 401. |
| Mass assignment | CUMPLE | Campos internos inyectados no se aplicaron. |
| Inyecciones/XSS | CUMPLE | Texto tratado como dato; sin ejecución. |
| Fuerza bruta | CUMPLE AUTOMATIZADO | 429 y `Retry-After`; preparar demostración sin bloquear usuarios de demo. |
| ZAP sin High | CUMPLE | Evidencia disponible. |
| Dependencias sin CVE crítica | CUMPLE | Scan de CI aprobado. |

## Eje E - IA

| Requisito | Estado | Observación |
| --- | --- | --- |
| IA detrás de gateway | CUMPLE | Gemini en Test y `mock-v1` determinista en CI. |
| Prompt injection | CUMPLE | Prueba adversarial live aprobada. |
| Fuera de dominio | CUMPLE EN EVALS | Incorporar el reporte al paquete final. |
| Fuga de datos | CUMPLE | Entrada con PII no la devolvió en la salida. |
| Caída del proveedor | CUMPLE EN TEST | Timeout, circuit breaker y fallback; preparar evidencia/demo. |
| Declaración de herramientas | PARCIAL | Codex, Claude y Gemini documentados; faltan autores y firma/revisión del equipo. |
| Incluida en `v2.0-entrega4` | NO | Fue incorporada después del tag obligatorio actual. |

## Requisitos propios de la comisión

| Requisito | Estado | Acción |
| --- | --- | --- |
| Integración con Core y módulos del Miro | PENDIENTE | Cerrar M2, M7, M1 `rejected`, eventos secundarios y resiliencia Core. |
| Despliegue accesible | CUMPLE | Azure Test y seis logins QA responden 200. |
| 85% Front y Back | CUMPLE | Front 85,66%; Back 90,04% líneas. |
| JWT firmado en M1 | PENDIENTE | M3 continúa con autenticación propia; falta integración central o acuerdo verificable. |
| Ambiente Testing | CUMPLE | Azure Test accesible y PostgreSQL operativo. |
| Catálogo de eventos Core | PARCIAL | Publicaciones principales registradas; faltan reconciliaciones y pruebas del mapa completo. |

## Orden de cierre recomendado

1. Resolver la referencia `v2.0-entrega4` antes de seguir agregando commits.
2. Cerrar matriz de historias y defectos con Testing.
3. Coordinar M2, M7, M1 `rejected`, TC-022 y TC-024.
4. Resolver BOLA/IDOR y JWT M1.
5. Regenerar paquete final, actualizar Jira y subir PDF/presentación/documentos a Teams.
6. Ensayar demo y defensa individual.
