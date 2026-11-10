# Matriz de trazabilidad — Entrega 4

| Requisito | Implementación/evidencia | Prueba | Estado al 10/11 |
| --- | --- | --- | --- |
| State y transiciones 409 | `WorkOrderState`, `WorkOrderStates`, ADR-002 Back | `DeliveryFourCriteriaTests`, flujo de órdenes | PASS CI |
| Tres patrones con ADR | State, Strategy de creación, Inbox/Outbox | ADR-001/002/003 Back | DOCUMENTADO |
| Idempotency-Key | filtro persistente + Flyway V11 | repetición y conflicto de cuerpo | PASS local |
| ETag/If-Match | `@Version`, controladores + Flyway V12 | ETag vigente/obsoleto/malformado | PASS local |
| Problem Details | manejador global y 401/403 | aserciones de Content-Type/código | PASS local |
| Fuerza bruta 429 | `LoginRateLimitFilter` | tercer intento bloqueado y Retry-After | PASS local |
| Timeout/fallback IA | gateway HTTP de 5 s | proveedor ausente, error y respuesta vacía | PASS local |
| Prompt injection/fuera de dominio/fuga | servicio de asistente | cuatro casos de seguridad | PASS local |
| Tests Back | Maven/JaCoCo/PIT | 117 tests; 90,43% líneas; 71,10% ramas; mutation 60% | PASS CI |
| Testcontainers PostgreSQL | `PostgresContainerSmokeTests` | Flyway y health real | PASS CI |
| Tests Front | workflow del Front | 61 tests; 85,66% líneas; lint, build y contenedor | PASS CI |
| M6 E2E | Core/M6/M3 | reparación → programada → completada | CONFIRMADO externo |
| M1 approved E2E | Core/M1/M3 | proyecto aprobado → expediente resuelto | CONFIRMADO externo |
| M1 rejected | mismo circuito con rechazo | prueba coordinada | PENDIENTE externo |
| M2 y M7 E2E | contratos vigentes | prueba bilateral | PENDIENTE externo |
| Build único | `docker compose up --build` | clon limpio en 138 s | PASS tag `v2.0-entrega4` |
| Carga 50 usuarios | k6 en tag `v2.0-entrega4` | 5 min; p95 6,35 ms; errores 0%; checks 100% | PASS |
| ZAP/secretos | workflow release | 0 High/Critical + Gitleaks historial completo | PASS |
| Azure Test | Terraform + imágenes por SHA | 2 cambios in-place; 0 destrucciones; 6 logins | PASS HTTP/DB |
| RabbitMQ Core | listener AMQPS y `minReplicas=1` | allowlist `57.156.67.226/32`; conexión `module_obras` creada | PASS conectividad |
| Jira al día | tablero externo | revisión humana | NO VERIFICADO |
| Teams | PDF y presentación | carga antes de clase | PENDIENTE humana |
| Demo en vivo | ambiente accesible | recorrido docente | PENDIENTE de clase |
| IA real | `AI_GATEWAY_URL`/`AI_GATEWAY_API_KEY` | llamada a proveedor | BLOQUEADO por endpoint/secretos |
