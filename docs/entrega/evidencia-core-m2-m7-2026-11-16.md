# Cierre de auditoría Core — M2 y M7

**Fecha de recepción:** 16 de noviembre de 2026  
**Fuente:** Equipo Core/M9, auditorías de solo lectura compartidas con M2, M3 y M7.  
**Estado documental:** `CONFIRMED` para los recorridos descritos.

## M2 — cierre `RESOLVED`

Core auditó `updateTicketStatus`:

- `eventId`: `c889727e-db9e-4bd6-a064-7ff1ad5b32b6`.
- `correlationId`: `fd8aa7f3-c7e0-43c1-be5a-6d6c49511239`.
- origen: `obras`.
- `eventVersion`: `1.0`.
- estado en Core: `ROUTED`.
- entrega a `q.atencion-ciudadana`: `DELIVERED`, un intento y sin error.
- entrega adicional a `q.ciudadanos`: `DELIVERED`, un intento y sin error.
- `retry_audit`: cero registros asociados.
- `dead_letters`: cero registros asociados.

M2 había confirmado de forma independiente Inbox `PROCESSED`, disposición `APPLIED`, error `NULL` y la transición del ticket `TK-2026-000045` a `RESOLVED`. Con ambas fuentes queda cerrado el recorrido E2E del cierre solicitado.

Core observó bajo la misma correlación un `ticketUpdated` de M2 y cuatro `updateTicketStatus` de M3. Los tres anteriores tienen otros `eventId`; Core no los clasificó como duplicados ni reintentos porque no contó con evidencia suficiente. Esta observación no modifica el resultado del evento auditado.

## M7 — variantes A, B y C de cortes v1.1

Core encontró los siete eventos en `event_log`, todos `ROUTED`, y registró once entregas `DELIVERED` en el primer intento y sin errores:

- tres entregas a `q.transito`;
- cuatro entregas a `q.obras`;
- cuatro entregas a `q.ambiente`.

### A — rechazo

- `streetClosureRequested`: `d5f328ec-5b71-4bdb-8edb-653a6de2fd22`.
- `streetClosureRejected`: `04edb9b6-9a45-4a68-b81f-4bd1c20979aa`.
- estado funcional confirmado por M3/M7: `REJECTED`.

### B — activación y cierre automático

- `streetClosureRequested`: `458a93ea-19b9-49a8-bd09-c1a01f87c781`.
- `streetClosureApproved`: `43597886-72a5-4028-9c75-822847197a3d`.
- `streetClosureEnded`: `a6fe83e5-5339-4686-b399-6c1239571e34`.
- estado funcional confirmado por M3/M7: `ENDED`.

### C — aprobación sin activación

- `streetClosureRequested`: `1d6ae7a0-eae8-485c-9469-fbd964beb965`.
- `streetClosureApproved`: `1d426b5a-ac1b-428b-81dc-7f3890a6a35f`.
- estado funcional confirmado por M3/M7: `EXPIRED`.
- Core no encontró `streetClosureEnded` en esa correlación, de acuerdo con el contrato: un corte que nunca estuvo activo vence internamente y no publica finalización.

Cada circuito conservó su `correlationId`; todas las respuestas usaron como `causationId` el `eventId` de la solicitud original. Los siete eventos mantuvieron `eventVersion="1.0"`, aunque el documento bilateral sea v1.1.

Core no encontró reintentos, fallos ni dead letters relacionados. Al momento de la consulta, `q.obras`, `q.transito`, `q.ambiente` y `q.dlq` no tenían mensajes pendientes; las tres colas funcionales tenían consumidor.

M7 confirmó además el cierre de A, B y C de su lado. La validación de Core fue de solo lectura y no consumió mensajes ni modificó configuración.

## Conclusión

- M2 ↔ M3: el recorrido probado `ticketUpdated → STARTED/PROGRESS/RESOLVED`, con auditoría detallada del cierre `RESOLVED`, queda `CONFIRMED`.
- M7 ↔ M3: rechazo, cierre automático y expiración sin activación del contrato documental v1.1 quedan `CONFIRMED`.
- No se requiere repetir estos casos para cerrar la integración. Una transición negativa fuera de orden puede mantenerse como cobertura adicional de QA.
