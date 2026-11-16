# Matriz de trazabilidad — Entrega 4

| Requisito | Implementación/evidencia | Prueba | Estado al 15/11 |
| --- | --- | --- | --- |
| State y transiciones 409 | `WorkOrderState`, `WorkOrderStates`, ADR-002 Back | `DeliveryFourCriteriaTests`, flujo de órdenes | PASS CI |
| Tres patrones con ADR | State, Strategy de creación, Inbox/Outbox | ADR-001/002/003 Back | DOCUMENTADO |
| Idempotency-Key | filtro persistente + Flyway V11 | repetición y conflicto de cuerpo | PASS local |
| ETag/If-Match | `@Version`, controladores + Flyway V12 | ETag vigente/obsoleto/malformado | PASS local |
| Problem Details | manejador global y 401/403 | aserciones de Content-Type/código | PASS local |
| Fuerza bruta 429 | `LoginRateLimitFilter` | tercer intento bloqueado y Retry-After | PASS local |
| Timeout/fallback IA | gateway HTTP de 5 s | proveedor ausente, error y respuesta vacía | PASS local |
| Prompt injection/fuera de dominio/fuga | servicio de asistente | cuatro casos de seguridad | PASS local |
| Tests Back | Maven/JaCoCo/PIT | 140 tests; JaCoCo y mutation 60% | PASS CI final `43857225056` |
| Testcontainers PostgreSQL | `PostgresContainerSmokeTests` | Flyway y health real | PASS CI |
| Tests Front | SHA `4d1a885f...` | 64 tests; cobertura global >85%; 7 E2E; build | PASS CI final `43901973413` |
| M6 E2E | Core/M6/M3 | reparación → programada → completada | CONFIRMADO externo |
| M1 approved E2E | Core/M1/M3 | proyecto aprobado → expediente resuelto | CONFIRMADO externo |
| M1 rejected | `caseFileResolved` rechazado para OBRA-16 | Core `44fd8a17-fc0b-4638-8fdf-046117b8a00e`; M1 y M3 | CONFIRMADO externo |
| M2 E2E | `ticketUpdated` → `STARTED/PROGRESS/RESOLVED` | M2/M3/Core; cierre `c889727e-db9e-4bd6-a064-7ff1ad5b32b6` | CONFIRMADO externo |
| M7 E2E | solicitud, aprobación/rechazo, cierre manual/automático, expiración y accidente | M3/M7/Core, variantes A/B/C auditadas el 16/11 | CONFIRMADO externo |
| Build único | `docker compose up --build --wait` | tag `v2.0-entrega4`, run `43890063632` | PASS, 140 s |
| Carga 50 usuarios | k6 en tag `v2.0-entrega4` | 301,2 s; 44.746 requests; p95 7,84 ms; fallos 0; checks 100% | PASS |
| ZAP/secretos | workflow release | 0 High/Critical + Gitleaks historial completo | PASS |
| Azure Test | Terraform + imágenes por SHA y digests ACR | revisiones finales con 100% del tráfico; HTTP 200 en Front y Back | PASS live 15/11 |
| RabbitMQ Core | listener AMQPS y `minReplicas=1` | allowlist `57.156.67.226/32`; conexión `module_obras` creada | PASS conectividad |
| OpenAPI y Swagger | contrato REST + `api-openapi-soap-entrega4.md` presentes en el tag | `/v3/api-docs` 200 y `/swagger-ui/index.html` 200 en Azure Test | PASS; WSDL no aplica porque M3 no usa SOAP |
| Manual de usuario | `manual-usuario-entrega4.md` presente en el tag | tareas por rol y recuperación básica | DOCUMENTADO; recorrido al azar pendiente de clase |
| Jira al día | KAN-1 a KAN-136 informados por QA | revisión humana final antes de Teams | CARGADO; verificar estados finales |
| Teams | PDF y presentación | carga antes de clase | PENDIENTE humana |
| Demo en vivo | ambiente accesible | recorrido docente | PENDIENTE de clase |
| IA real | `IncidentTriageGateway` + Gemini en Azure Test | salida estructurada, revisión humana y fallback | PASS despliegue; evidencia adversarial final a consolidar |
