# Ejecución exploratoria del ambiente Test — 2026-09-21

## Alcance y método

Se abrió el Front público de Test en un navegador real y se interactuó con el formulario de acceso. Esta ejecución no sustituye las pruebas automatizadas ni demuestra los flujos internos: registra lo que un tester puede hacer desde la interfaz desplegada. Hora aproximada: 15:43-15:45 de Argentina. No se guardaron contraseñas ni tokens en este informe.

Ambiente: `https://ca-obras-publicas-tst-frontend.purpleisland-1134bab8.chilecentral.azurecontainerapps.io/`.

## Resultado

| Prueba ejecutada | Resultado | Evidencia observable |
| --- | --- | --- |
| Abrir el Front en escritorio | APROBADO | Carga la pantalla «Obras Públicas» con usuario, contraseña e ingreso. |
| Enviar usuario y contraseña vacíos | APROBADO | Muestra «Ingresá usuario y contraseña.» sin enviar el formulario. |
| Enviar usuario sin contraseña | APROBADO | Muestra el mismo aviso y no inicia sesión. |
| Enviar contraseña sin usuario | APROBADO | Muestra el mismo aviso y no inicia sesión. |
| Ingresar con una cuenta de demo válida (`ingeniero.arquitecto`) | FALLÓ, BLOQUEANTE | El navegador muestra «Error 403 al comunicarse con la API». La solicitud `POST /api/auth/login` devuelve HTTP 403. |
| Salud del backend y PostgreSQL a través del Front | APROBADO, control auxiliar | `GET /api/health` devuelve HTTP 200, `status: ok` y `database: up`. Esto no demuestra que el login funcione. |
| Comparación de la misma cuenta por HTTP | Diagnóstico | `POST /api/auth/login` devuelve HTTP 200 sin encabezado `Origin`, pero HTTP 403 cuando se envía `Origin` con la URL pública del Front. El navegador envía ese origen en su petición. |

## Incidencia crítica: el login del navegador está bloqueado

Pasos para reproducir: abrir la URL del Front, ingresar `ingeniero.arquitecto` y su contraseña de demo vigente, pulsar «Ingresar». Resultado actual: mensaje de error 403 y permanencia en el login. Resultado esperado: ingreso al tablero con el rol correspondiente.

La comparación con y sin `Origin` apunta a una configuración CORS del backend que no acepta el origen público del Front. El código de backend consultado como apoyo diagnóstico usa `CORS_ALLOWED_ORIGINS` y, en ausencia de esa variable, permite por defecto únicamente `http://localhost:3000` y `http://localhost:5173`; la infraestructura Test no declara actualmente esa variable. Esta es una hipótesis causal fuerte que debe verificarse al corregir y redesplegar. La API y la base responden; no es una caída general del servicio ni una contraseña incorrecta.

Severidad: **crítica/bloqueante** para la demo y para pruebas funcionales manuales. No se modificó el código ni la infraestructura durante esta ejecución.

## Cobertura pendiente

QA-01 falla en el ingreso desde navegador. QA-02 a QA-06 y QA-08 a QA-12 quedan **BLOQUEADOS**, porque requieren sesión y operaciones en pantalla. QA-07 (rutas sin sesión) y la parte móvil de QA-13 quedan **NO EJECUTADOS**; QA-14 solo está comprobado parcialmente por el acceso a `/api/health`, no por el flujo completo. No corresponde marcar la release como aceptada ni afirmar que las funcionalidades internas funcionan por el smoke test de API.

Luego de corregir CORS y desplegar, repetir el login desde un navegador común y recién entonces ejecutar el recorrido completo del [plan de testing](plan-testing-release-v0.2.0.md), incluyendo roles, proyecto, aprobación, orden de trabajo, programación, ejecución, inspección, cortes, permisos, validaciones, recarga y móvil. Registrar cada caso con evidencia y resultado.
