# Runbook simple de pruebas de integración pendientes

Fecha de corte: 2026-11-10  
Ambiente: Azure Test + Core AWS  
Responsable M3: DevOps coordina; cada módulo confirma su procesamiento funcional.

Este documento no agrega endpoints ni contratos. Usa únicamente los eventos acordados y deja la acción concreta de cada sistema en manos de su equipo propietario.

## Antes de empezar

1. Abrir el Front de Azure Test y comprobar que permite iniciar sesión.
2. Abrir `/api/health` y comprobar `status=ok` y `database=up`.
3. Confirmar en logs que existe una conexión AMQPS de `module_obras`.
4. Pedir a Core que observe eventos, entregas, colas y DLQ durante la ventana.
5. Usar datos ficticios. No publicar contraseñas, tokens, DNI ni secretos.
6. Para cada evento guardar `eventId`, `correlationId`, identificador de negocio, hora y resultado del consumidor.

Para los controles HTTP no destructivos se puede ejecutar `scripts/demo-security-live.ps1`. El script exige `TEST_BASE_URL`, `TEST_LOW_ROLE_USERNAME` y `TEST_LOW_ROLE_PASSWORD` como variables de entorno; nunca contiene ni imprime las credenciales. La fuerza bruta solo se activa si se define `TEST_RATE_LIMIT_USERNAME` con una cuenta descartable, porque puede bloquearla temporalmente.

## Prueba 1 — M1 `rejected`

Objetivo: comprobar la variante que falta del circuito ya aprobado con M1.

### Secuencia

1. M3 inicia un proyecto de prueba y publica `publicWorksProjectApproved`.
2. M3 comparte con M1 y Core `eventId`, `publicWorksProjectId` y `correlationId`.
3. M1 confirma la creación del expediente institucional.
4. M1 registra una resolución administrativa `rejected` y publica `caseFileResolved` v1.0.
5. M1 comparte `eventId`, `caseFileId`, `caseFileNumber`, `publicWorksProjectId`, `correlationId` y `resolution=rejected`.
6. Core confirma validación, estado `ROUTED`, entrega a `q.obras` y ausencia en DLQ.
7. M3 confirma que registró el expediente y el rechazo como resultado funcional, sin tratarlo como un fallo técnico ni republicarlo.

### Aprobación

- Los dos eventos conservan el mismo `correlationId`.
- `externalReference.id` coincide con `publicWorksProjectId`.
- M3 persiste `caseFileId` y el resultado `rejected`.
- No hay mensaje pendiente ni DLQ atribuible al circuito.

### Mensaje listo para M1 y Core

> Hola M1 y Core. Proponemos ejecutar la variante pendiente `rejected` del circuito M3–M1. M3 publicará `publicWorksProjectApproved` y compartirá `eventId`, `publicWorksProjectId` y `correlationId`. M1 deberá resolver el expediente con `caseFileResolved.resolution=rejected`, conservando la correlación. Core verificará validación, enrutamiento a `q.obras` y DLQ. M3 cerrará confirmando el procesamiento funcional del rechazo.

## Prueba 2 — M2 Atención Ciudadana

Objetivo: comprobar derivación de un ticket a Obras y devolución de avances.

### Secuencia

1. M2 publica `ticketUpdated` con `responsibleAreaId=M3` y un `updateType` acordado para la derivación inicial.
2. M2 comparte `eventId`, `ticketId` y `correlationId`.
3. Core confirma entrega a `q.obras`.
4. M3 confirma que filtró el evento por `responsibleAreaId=M3` y registró o vinculó la atención operativa.
5. Al iniciar el trabajo, M3 publica `updateTicketStatus` con `STARTED`.
6. Si se demuestra progreso, M3 publica después `PROGRESS`; nunca se envía `PROGRESS` antes de `STARTED`.
7. Al existir una solución para el ciudadano, M3 publica `RESOLVED` con el mensaje público y los detalles exigidos por M2.
8. M2 confirma las transiciones aplicadas. Core confirma entrega, intentos y DLQ.

### Aprobación

- Los eventos usan el mismo hilo de correlación.
- El evento saliente de M3 usa `sourceModule=obras`.
- `causationId` referencia el evento que originó cada respuesta cuando corresponde.
- M3 ignora sin error eventos cuyo `responsibleAreaId` no sea `M3`.
- M2, como autoridad del ticket, confirma el cambio funcional.

### Mensaje listo para M2 y Core

> Hola M2 y Core. Queremos coordinar la prueba pendiente M2–M3. M2 publica un `ticketUpdated` de prueba dirigido a `responsibleAreaId=M3` y comparte `eventId`, `ticketId` y `correlationId`. M3 confirmará el consumo y publicará `updateTicketStatus` primero `STARTED` y luego `RESOLVED`, conservando correlación y causalidad. M2 valida las transiciones y Core verifica enrutamiento, intentos y DLQ.

## Prueba 3 — M7 Tránsito

Objetivo: comprobar una solicitud de corte y su respuesta por el contrato v1.0.

### Secuencia recomendada: aprobación

1. M3 crea la necesidad de corte asociada a una orden y publica `streetClosureRequested`.
2. M3 comparte `eventId`, `closureRequestId`, `sourceRef` y `correlationId`.
3. M7 confirma recepción y publica `streetClosureApproved`.
4. La respuesta conserva `correlationId` y usa como `causationId` el `eventId` de la solicitud.
5. M3 confirma que vinculó la aprobación con la solicitud y usa `endDate` como fin operativo autorizado.
6. Core confirma entrega a ambas partes y DLQ vacía.
7. Si la ventana permite demostrarlo, M7 finaliza un corte activo y publica `streetClosureEnded` con el nombre correcto.

### Aprobación

- `affectedSections` viaja estructurado con `street`, `from`, `to` y `direction`.
- `direction` usa `FORWARD`, `REVERSE` o `BOTH`.
- El envelope de M3 usa `sourceModule=obras`; el de M7 usa `sourceModule=transito`.
- M3 recibe `streetClosureApproved`, `streetClosureRejected` o `streetClosureEnded` sin usar el nombre histórico con typo.
- Core no registra rechazos ni DLQ del circuito.

### Mensaje listo para M7 y Core

> Hola M7 y Core. Proponemos la prueba pendiente del contrato M3–M7 v1.0. M3 publicará `streetClosureRequested` con tramos estructurados y compartirá `eventId`, `closureRequestId`, `sourceRef` y `correlationId`. M7 responderá `streetClosureApproved` conservando la correlación y usando el evento solicitado como `causationId`. M3 confirmará el vínculo y Core verificará enrutamiento y DLQ. Si es posible, cerramos también con `streetClosureEnded` escrito sin typo.

## Evidencia mínima por prueba

| Campo | Valor |
| --- | --- |
| Fecha y hora | |
| Ambiente | Azure Test / Core AWS |
| Evento inicial | |
| `eventId` inicial | |
| `correlationId` | |
| Evento de respuesta | |
| `eventId` de respuesta | |
| Identificador de negocio | |
| Estado en Core | |
| Entrega e intentos | |
| Cola pendiente | |
| DLQ | |
| Confirmación del productor | |
| Confirmación del consumidor | |
| Resultado | APROBADO / FALLIDO / BLOQUEADO |

## Si algo falla

- `422` por HTTP: guardar el error; el sobre no ingresó al hub.
- Rechazo del schema de `data`: conservar el mismo `eventId` si se reenvía el mismo hecho después de corregirlo.
- `nack`: usar `requeue=false`; Core controla los reintentos.
- Timeout de red: registrar hora, IP efectiva y error; no cambiar contratos ni credenciales.
- Mensaje en DLQ: no declararlo procesado aunque el productor haya recibido confirmación del broker.

## Cierre para la defensa

Una prueba E2E se considera cerrada cuando Core acredita validación y entrega, y el módulo receptor confirma el efecto funcional. Ver únicamente `ROUTED` no demuestra por sí solo que la aplicación consumió y procesó el evento.
