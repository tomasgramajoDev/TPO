# Integración con Atención Ciudadana — Módulo 2

## Estado vigente

M2 entregó el 2026-10-20 la guía Eventos v1.78 y el paquete de JSON Schema Draft 2020-12. v1.78 reemplaza las versiones anteriores. M3 consume `ticketUpdated`, filtra `responsibleAreaId=M3` y publica hechos mediante `updateTicketStatus`; M2 conserva la autoridad sobre estado, prioridad y categoría.

El 2026-11-15 M2 confirmó la recepción y aplicación de `STARTED`, los dos `PROGRESS` y `RESOLVED` del circuito real. El ticket `TK-2026-000045` quedó `RESOLVED`, con área responsable `M3`. La aplicación funcional bilateral queda `CONFIRMED`. El cierre técnico integral permanece `CORE_PENDING` hasta que Core confirme enrutamiento, intentos y ausencia de registros asociados en DLQ.

El paquete `m2-eventos-v1.78-schemas.zip` tiene SHA-256 `f20347c6cea5e9197e11d73cb3aef77db6fffd4c342ab75232381775c671b27f`. La diferencia funcional frente a v1.77 es `updatedBy.id`, que ahora valida UUID o `null`.

## Evento recibido por Obras

### `ticketUpdated`

- M3 se suscribe mediante Core y lo recibe en `q.obras`.
- Core rutea por `eventType`, no por `responsibleAreaId`; cada consumidor debe filtrar sus eventos.
- M3 procesa únicamente `data.responsibleAreaId=M3`; `ticketCreated` no se consume.
- M3 actúa ante `ROUTED`, `INFORMATION_PROVIDED`, `REOPENED`, `CANCELLED`, `PRIORITY_CHANGED` y `ESCALATION_CHANGED` cuando corresponden a su gestión.
- Los mensajes con `purpose=RECLASSIFICATION` se ignoran operacionalmente hasta un `ROUTED` posterior.
- El consumidor compara `data.updatedAt`, estado y última versión aplicada; no depende del orden de RabbitMQ.
- M3 deduplica por `eventId` y no crea un segundo ticket u orden ante reentregas.

## Evento publicado por Obras

### `updateTicketStatus`

- Variantes: `STARTED`, `PROGRESS`, `INFORMATION_REQUIRED`, `RETURNED`, `RESOLVED` y `REJECTED`.
- Campos comunes obligatorios: `ticketId`, `updateType`, `updatedBy` y `updateOccurredAt`.
- `STARTED` precede a `PROGRESS` cuando el ticket todavía está `ROUTED`.
- `progress` es opcional y representa un porcentaje físico medido; no se inventa un valor cuando no existe medición.
- `RESOLVED` requiere `publicMessage` y `details.resolution.type`.
- `updatedBy.type=EXTERNAL_USER` usa el UUID de la persona en M3; `null` queda reservado para `SYSTEM` o ausencia de una persona identificable.
- `RETURNED` y `REJECTED` requieren el `reasonCode` correspondiente y un mensaje público o interno.
- Cuando deriva de un evento de M2, conserva `correlationId` y usa como `causationId` el `eventId` recibido.

## Reglas técnicas

- Entrega `at-least-once`, sin orden garantizado.
- Un reenvío del mismo hecho conserva el mismo `eventId`.
- Ante fallo se usa `nack(requeue=false)`.
- Los archivos `*.data.schema.json` validan únicamente `data`; el envelope se valida por separado en Core.
- `data` debe estar siempre presente como objeto.

## Evidencia bilateral — 2026-11-15

### Entrada M2 → M3

- `ticketUpdated`: `b99c2981-d7a5-476e-b748-23e31ed75647`.
- `ticketId`: `f2e7fb86-8ea6-490c-8aa8-c71213a91f36`.
- `publicId`: `TK-2026-000045`.
- `correlationId`: `fd8aa7f3-c7e0-43c1-be5a-6d6c49511239`.
- Inbox M3: `PROCESSED`.

### Salida M3 → M2

- `STARTED`: `e9d0e937-95c1-4999-83b3-ef1258c20b7b`.
- `PROGRESS` de programación: `d1163f06-1951-4843-bad2-b5295e6afd2d`.
- `PROGRESS` de inicio: `868c43db-9600-47f1-b306-ac3aa22155c3`.
- `RESOLVED`: `c889727e-db9e-4bd6-a064-7ff1ad5b32b6`.

M2 confirmó para `RESOLVED`:

- Inbox `PROCESSED`.
- Disposición `APPLIED`.
- `producerModuleId=M3`.
- `error=NULL`.
- Transición `IN_PROGRESS → RESOLVED` aplicada correctamente.
- Ticket final `RESOLVED`, responsable `M3`.
- `currentProgress=NULL`, resultado esperado porque los dos `PROGRESS` no incluyeron el campo opcional `data.progress`.

M2 también dio por validados `STARTED` y ambos `PROGRESS`. Esta evidencia confirma el procesamiento funcional de extremo a extremo entre M2 y M3.

## Pendiente único del circuito probado

Core debe confirmar para los cuatro eventos salientes `ROUTED/DELIVERED`, cola de destino, cantidad de intentos y ausencia o presencia de registros asociados en DLQ/retry. Hasta recibir esa evidencia, el transporte se conserva como `CORE_PENDING` y no se infiere solo a partir del Outbox de M3.
