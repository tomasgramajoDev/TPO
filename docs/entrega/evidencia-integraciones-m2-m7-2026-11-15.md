# Evidencia de integraciones M2 y M7 — 2026-11-15

## Fuente y alcance

Esta ficha registra observaciones verificadas directamente en Azure Test del Módulo 3. La fuente fue la revisión `ca-obras-publicas-tst-backend--latest`, sus logs en Azure Log Analytics y el endpoint autenticado `GET /api/public-works/integration-events`. No contiene credenciales ni payloads con datos personales.

La evidencia del consumidor M3 no reemplaza la constancia de Core sobre `ROUTED`, `DELIVERED`, intentos y DLQ. Por eso se separa lo comprobado de lo pendiente.

## M7 — circuito de cortes

| Etapa | eventId | correlationId | Evidencia M3 | Estado |
| --- | --- | --- | --- | --- |
| `streetClosureRequested` | `2d6893aa-9482-4dfd-98c3-85607f36bdab` | `afca371d-ddfd-497c-a437-f9152bef52bf` | Publicado por M3; Core y M7 confirmaron entrega y procesamiento | `CONFIRMED` |
| `streetClosureApproved` | `6f521edf-177f-43c4-b3ec-0a3eb1245fd5` | `afca371d-ddfd-497c-a437-f9152bef52bf` | Azure log: `received` y `processed`; API: `PROCESSED` | Funcionalmente comprobado |
| `streetClosureEnded` | `c8479b39-4741-49f3-a3ea-f255d16416c2` | `afca371d-ddfd-497c-a437-f9152bef52bf` | Azure log: `received` y `processed`; API: `PROCESSED` | Funcionalmente comprobado |

La consulta funcional del corte en Azure Test confirmó:

- `closureRequestId=44555606-a4b7-4a0b-984b-94255b49faa8`.
- `streetClosureId=c5941b88-1caa-4e6f-bc3d-439879f31408`.
- estado final `ENDED`.
- ventana autorizada `2026-11-15T17:35:08Z` a `2026-11-15T19:34:08Z`.
- finalización registrada a las `2026-11-15T14:36:05.254816765-03:00`.

Pendiente externo: Core debe confirmar las dos entregas de respuesta, intentos y DLQ. También queda una prueba específica del vencimiento automático para distinguir un cierre por expiración de un cierre iniciado manualmente.

## M7 — accidente con daño de infraestructura

- `eventId`: `9d7b06ec-dfa3-4ca6-9d28-acc17ed82523`.
- `correlationId`: `dca92b7c-b533-438e-99de-cebc6446d4ef`.
- Intentos observados en M3: 17:10:45, 17:10:50, 17:11:21 y 17:13:21 UTC.
- Resultado de cada entrega: `received` seguido de `error`.
- El evento falló antes de persistirse en Inbox; no produjo proyección ni segundo efecto.

Conclusión: la prueba no está aprobada. El patrón temporal coincide con la entrega original y tres reintentos de `maxAttempts=4`. Se necesita el sobre exacto emitido por M7 y la constancia final de Core/DLQ para identificar la incompatibilidad contractual y repetir el caso.

## M2 — ticket derivado

- `eventId`: `b99c2981-d7a5-476e-b748-23e31ed75647`.
- `correlationId`: `fd8aa7f3-c7e0-43c1-be5a-6d6c49511239`.
- `sourceModule`: `atencion-ciudadana`.
- Resultado M3: `PROCESSED` en logs y endpoint operativo.

Conclusión: la entrada `ticketUpdated` está comprobada. Falta publicar una respuesta `updateTicketStatus` del mismo hilo y que M2/Core confirmen su aplicación. No se observó una salida asociada durante esta revisión.

## Mensajes para coordinación

### Para M7 y Core

> M3 confirma que procesó `streetClosureApproved` (`6f521edf-177f-43c4-b3ec-0a3eb1245fd5`) y `streetClosureEnded` (`c8479b39-4741-49f3-a3ea-f255d16416c2`), ambos con `correlationId=afca371d-ddfd-497c-a437-f9152bef52bf`. La solicitud `44555606-a4b7-4a0b-984b-94255b49faa8` quedó `ENDED` y vinculada al corte `c5941b88-1caa-4e6f-bc3d-439879f31408`. Core, ¿pueden confirmar `ROUTED`/`DELIVERED`, intentos, DLQ y `causationId` de ambos? El accidente `9d7b06ec-dfa3-4ca6-9d28-acc17ed82523` llegó cuatro veces a M3 y falló antes de Inbox. Necesitamos el payload exacto y el estado final/DLQ para cruzarlo con el contrato y repetir la prueba.

### Para M2 y Core

> M3 confirma que procesó `ticketUpdated` (`b99c2981-d7a5-476e-b748-23e31ed75647`, `correlationId=fd8aa7f3-c7e0-43c1-be5a-6d6c49511239`). Para completar la vuelta, indíquennos el `ticketId` del caso y el estado inicial esperado; publicaremos `updateTicketStatus` conservando la correlación. Core puede verificar luego entrega, intentos y DLQ, y M2 la transición funcional.
