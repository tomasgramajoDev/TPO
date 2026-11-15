# Runbook de seguridad y resiliencia para la demo

**Corte:** 15 de noviembre de 2026

Este runbook separa lo automatizado de las acciones que requieren una persona, dos identidades o coordinación con Core. No contiene usuarios, contraseñas, tokens ni datos reales.

## Preparación

1. Usar Azure Test y datos ficticios.
2. Definir las credenciales únicamente como variables de entorno locales.
3. Abrir Network del navegador y conservar capturas sin encabezados `Authorization`.
4. Registrar fecha, rol, recurso, resultado HTTP, estado anterior y estado posterior.

## Controles HTTP automatizables

```powershell
$env:TEST_BASE_URL = "https://<backend-test>"
$env:TEST_LOW_ROLE_USERNAME = "<usuario-de-rol-bajo>"
$env:TEST_LOW_ROLE_PASSWORD = "<secreto-local>"
./scripts/demo-security-live.ps1
```

El script comprueba health, OpenAPI, 401 sin sesión, 401 con JWT inválido, login, BFLA 403 e inyección como dato. La fuerza bruta solo se habilita con una cuenta descartable mediante `TEST_RATE_LIMIT_USERNAME`.

## BOLA/IDOR manual

1. Crear o elegir dos recursos de prueba accesibles desde identidades distintas.
2. Autenticarse como la identidad A y copiar el UUID del recurso A.
3. Autenticarse como la identidad B e intentar consultar o modificar el UUID de A.
4. Esperado: 403 o 404, sin datos sensibles ni mutación.
5. Si el dominio no posee ownership por usuario y ambos roles están autorizados sobre el recurso, registrar `NO APLICA` con la regla de autorización que lo justifica; no inventar un PASS.

## Mass assignment manual

1. Tomar un payload válido de Swagger.
2. Agregar campos internos como `role`, `status`, `owner`, `createdBy` o `version`.
3. Enviar con un rol autorizado para la operación normal.
4. Esperado: 400 o campos ignorados; nunca deben cambiar el rol, dueño, estado o versión por ese medio.
5. Volver a consultar el recurso y guardar la evidencia del estado intacto.

## JWT manual

Probar por separado token vencido, firma alterada, `alg=none` e issuer incorrecto. Cada caso debe devolver 401 uniforme, sin stack trace ni detalles criptográficos. No guardar los tokens en el repositorio o en Teams.

## Broker caído y recuperación

Esta prueba requiere coordinación porque el Core compartido es propiedad de M9.

1. Core acuerda la ventana y el mecanismo de indisponibilidad controlada.
2. M3 ejecuta una operación que genere un evento mientras la publicación no está disponible.
3. M3 verifica que la transacción funcional no pierda el evento y que Outbox quede pendiente.
4. Core restaura el servicio.
5. M3 verifica que el mismo `eventId` pase de pendiente a publicado; no debe crearse un segundo hecho.
6. El consumidor confirma un solo efecto funcional; Core informa intentos y DLQ.

No se debe apagar, modificar ni saturar infraestructura compartida sin la coordinación de Core.

## Proveedor de IA caído

1. En un ambiente controlado, configurar el adaptador de prueba para timeout o error.
2. Enviar un caso de clasificación.
3. Esperado: respuesta controlada, fallback manual y ninguna transición automática de obra u orden.
4. Verificar que logs y métricas no contengan la API key ni datos personales.

## Evidencia mínima

| Campo | Contenido |
| --- | --- |
| Caso | SEC/TC correspondiente |
| Fecha y ambiente | Hora argentina y Azure Test/local |
| Actor y rol | Sin contraseña ni token |
| Recurso | UUID ficticio |
| Entrada | Payload sanitizado |
| Resultado | HTTP, cuerpo no sensible y estado final |
| Evidencia | Captura, video o log sanitizado |
| Veredicto | PASS / FAIL / BLOQUEADO / NO APLICA |
| Defecto | Jira/Trello si corresponde |

## Cierre

Los controles automatizados ya cuentan con evidencia de CI, pero la cátedra puede seleccionar cualquier caso en vivo. BOLA/IDOR, la interrupción coordinada del broker y la exposición presencial siguen siendo acciones humanas hasta que exista evidencia observada.
