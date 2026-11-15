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
| Tests Back | Maven/JaCoCo/PIT | 132 tests; 90,56% líneas; 72,24% ramas; mutation 60% | PASS local; Testcontainers requiere CI |
| Testcontainers PostgreSQL | `PostgresContainerSmokeTests` | Flyway y health real | PASS CI |
| Tests Front | SHA `d472da55...` | 63 tests; 85,55% líneas; 75,84% ramas; build | PASS local |
| M6 E2E | Core/M6/M3 | reparación → programada → completada | CONFIRMADO externo |
| M1 approved E2E | Core/M1/M3 | proyecto aprobado → expediente resuelto | CONFIRMADO externo |
| M1 rejected | `caseFileResolved` rechazado para OBRA-16 | Core `44fd8a17-fc0b-4638-8fdf-046117b8a00e`; M1 y M3 | CONFIRMADO externo |
| M2 E2E | `ticketUpdated` → `updateTicketStatus` | prueba bilateral | PENDIENTE externo |
| M7 E2E | solicitud entregada y procesada; falta respuesta/cierre | Core/M7 `2d6893aa-9482-4dfd-98c3-85607f36bdab` | PARCIAL externo |
| Build único | `docker compose up --build` | candidata corregida con SHAs finales | GATE REMOTO A REPETIR |
| Carga 50 usuarios | k6 en tag `v2.0-entrega4` | 5 min; p95 6,35 ms; errores 0%; checks 100% | PASS |
| ZAP/secretos | workflow release | 0 High/Critical + Gitleaks historial completo | PASS |
| Azure Test | Terraform + imágenes por SHA y digests ACR | revisiones finales con 100% del tráfico; HTTP 200 en Front y Back | PASS live 15/11 |
| RabbitMQ Core | listener AMQPS y `minReplicas=1` | allowlist `57.156.67.226/32`; conexión `module_obras` creada | PASS conectividad |
| OpenAPI y Swagger | contrato REST + `api-openapi-soap-entrega4.md` presentes en el tag | `/v3/api-docs` 200 y `/swagger-ui/index.html` 200 en Azure Test | PASS; WSDL no aplica porque M3 no usa SOAP |
| Manual de usuario | `manual-usuario-entrega4.md` presente en el tag | tareas por rol y recuperación básica | DOCUMENTADO; recorrido al azar pendiente de clase |
| Jira al día | tablero externo | revisión humana | NO VERIFICADO |
| Teams | PDF y presentación | carga antes de clase | PENDIENTE humana |
| Demo en vivo | ambiente accesible | recorrido docente | PENDIENTE de clase |
| IA real | `IncidentTriageGateway` + Gemini en Azure Test | salida estructurada, revisión humana y fallback | PASS despliegue; evidencia adversarial final a consolidar |
