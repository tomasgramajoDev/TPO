# BRD — M3 Obras Públicas — Entrega 4

**Versión:** candidata `v2.0-entrega4`  
**Fecha de corte:** 10 de noviembre de 2026  
**Estado:** candidato; el tag y la aceptación docente siguen pendientes.

## Objetivo de negocio

Centralizar la planificación, aprobación, ejecución, control y cierre de obras públicas y órdenes de trabajo municipales, con trazabilidad por rol e integración asincrónica mediante el Core.

## Actores

- Personal de Obras: crea proyectos, órdenes y solicitudes operativas.
- Responsable Autorizado: aprueba o rechaza proyectos.
- Jefe de Cuadrilla: programa, inicia, pausa y reanuda órdenes.
- Operario Contratista: informa la finalización operativa.
- Inspector de Obra: valida o reabre el trabajo.
- Ingeniero/Arquitecto: consulta información técnica habilitada.
- Módulos externos: M1 Ciudadanos/Expedientes, M2 Atención Ciudadana, M6 Ambiente, M7 Tránsito y M9 Core.

## Capacidades comprometidas

1. Autenticación JWT y autorización por roles.
2. Gestión de proyectos y aprobación.
3. Gestión de órdenes con patrón State y rechazo HTTP 409 ante transiciones inválidas.
4. Recursos, cuadrillas, cortes y tablero operativo.
5. Persistencia PostgreSQL y migraciones Flyway.
6. Mensajería confiable con Inbox/Outbox, deduplicación y DLQ del Core.
7. API con `Idempotency-Key`, `ETag`/`If-Match` y errores Problem Details.
8. Asistente de Obras detrás de gateway, con timeout de cinco segundos, fallback y controles contra abuso.
9. Arranque local reproducible con Docker Compose.

## Requisitos no funcionales

- Secretos fuera de Git; variables documentadas en `.env.example`.
- CI obligatorio, cobertura mínima y mutation testing.
- p95 menor a 500 ms bajo 50 usuarios concurrentes en el tag final.
- Auditoría de seguridad sin alertas High/Critical no mitigadas.
- Front, Back y base accesibles durante la demo.

## Integraciones confirmadas y pendientes

- M6–M3–Core: flujo `infrastructureRepairRequested` → `workOrderScheduled` → `workOrderCompleted` confirmado E2E.
- M1–M3–Core: escenario `approved` de `publicWorksProjectApproved` → `caseFileResolved` confirmado E2E.
- Pendientes externos: variante M1 `rejected` y pruebas E2E de M2 y M7.

## Criterio de aceptación de la entrega

La versión se considera candidata solamente cuando las ramas estables y el tag tengan CI verde, no existan defectos Bloqueantes/Críticos conocidos sin informar, y se completen evidencias de seguridad, carga, Jira, Teams y demo en vivo. Este documento no transforma una prueba pendiente en aprobada.
