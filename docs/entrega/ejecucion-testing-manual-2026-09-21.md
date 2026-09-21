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

## Cobertura pendiente al cierre de la primera ejecución

QA-01 falla en el ingreso desde navegador. QA-02 a QA-06 y QA-08 a QA-12 quedan **BLOQUEADOS**, porque requieren sesión y operaciones en pantalla. QA-07 (rutas sin sesión) y la parte móvil de QA-13 quedan **NO EJECUTADOS**; QA-14 solo está comprobado parcialmente por el acceso a `/api/health`, no por el flujo completo. No corresponde marcar la release como aceptada ni afirmar que las funcionalidades internas funcionan por el smoke test de API.

Luego de corregir CORS y desplegar, repetir el login desde un navegador común y recién entonces ejecutar el recorrido completo del [plan de testing](plan-testing-release-v0.2.0.md), incluyendo roles, proyecto, aprobación, orden de trabajo, programación, ejecución, inspección, cortes, permisos, validaciones, recarga y móvil. Registrar cada caso con evidencia y resultado.

## Reprueba después de la release de infraestructura v0.2.7

DevOps publicó [v0.2.7](https://github.com/tomasgramajoDev/TPO/releases/tag/v0.2.7) y el [workflow de Test](https://github.com/tomasgramajoDev/TPO/actions/runs/35640984823) finalizó correctamente. El plan tenía 0 altas, 2 cambios in-place y 0 bajas. Terraform inyectó `CORS_ALLOWED_ORIGINS` con el origen público exacto del Front; el smoke test de los seis usuarios incluyó `Origin`. No se cambiaron imágenes de aplicación ni credenciales.

En un navegador real, `ingeniero.arquitecto` ingresó correctamente y la interfaz mostró «Ingeniero o Arquitecto». Se abrieron Proyectos, Órdenes, Recursos, Cortes e Integraciones. El proyecto #1 y la orden #1 continuaron disponibles después del despliegue; el detalle de la orden mostró origen Proyecto, vínculo con Proyecto #1, cuadrilla y estado Validada. La búsqueda de una orden inexistente mostró un estado vacío y al limpiar el texto reapareció la orden. El filtro Pendiente también mostró estado vacío coherente. La sesión persistió tras recargar; «Salir» volvió al login y la recarga posterior no restauró la sesión. Una contraseña incorrecta mostró «Credenciales invalidas». `GET /api/public-works/projects` sin sesión respondió HTTP 401 como control auxiliar.

| Caso | Estado de esta reprueba | Límite de evidencia |
| --- | --- | --- |
| QA-01 | PARCIAL | Login, rol, recarga, logout y clave incorrecta aprobados para `ingeniero.arquitecto`; faltan cinco cuentas por interfaz. |
| QA-02 a QA-06 | PENDIENTE | El rol de ingeniería no puede ejecutar las acciones de esos flujos. |
| QA-07 | PARCIAL | La API protegida rechaza acceso anónimo con 401; no se probaron todas las rutas de pantalla. |
| QA-09 y QA-10 | PARCIAL | Búsqueda, filtro y detalles existentes aprobados; faltan formularios y persistencia de nuevos datos. |
| QA-11 | PENDIENTE | La pantalla de Cortes carga; el rol no puede solicitar. La autorización externa M7 está expresamente fuera de esta entrega. |
| QA-12 | PARCIAL | El tablero cargó desde backend y mostró los datos existentes; faltan cambios de estado nuevos. |
| QA-13 | FALLÓ EN MÓVIL | A 390 px de ancho, los seis botones de navegación se superponen; «Integraciones» termina fuera del viewport. Se midieron botones de ~94 px colocados cada ~58-59 px. |
| QA-14 | PARCIAL | Login y lecturas reales usaron `/api` desde el origen del Front; no se recorrieron todos los flujos. |

### Incidencias nuevas observadas

1. **Media — carga inicial tras login:** inmediatamente después de ingresar, Dashboard y «Cumplimiento por obra» mostraron «Se requiere un token valido»; al abrir Órdenes, Recursos y Cortes ocurrió lo mismo. «Reintentar» cargó los datos correctamente y una recarga de página normalizó la navegación. En la primera carga fallida de Órdenes no salió petición HTTP; al reintentar, `GET /api/public-works/work-orders` respondió 200. Parece un problema de inicialización del token en el Front, no una denegación del backend; debe confirmarlo Front.
2. **Media — menú móvil:** a 390 × 844 px, la navegación se solapa y se recorta. El documento no muestra desplazamiento horizontal para alcanzar el último botón.
3. **Baja — etiqueta de ambiente:** el encabezado del Front desplegado en Test indica `development - /api`. Las peticiones observadas sí llegan al ambiente Test; la etiqueta es confusa para la demo.

La pantalla Integraciones declara «La integración completa entre módulos queda fuera de esta primera entrega». No se marcaron como aprobados contratos o eventos externos solo por aparecer listados. Las acciones de Ingeniería/Arquitectura que faltan no se etiquetan como defecto definitivo hasta acordar su alcance funcional.

**Estado de aceptación:** la incidencia CORS quedó resuelta, pero la prueba funcional de los cinco roles operativos y el flujo nuevo proyecto → orden → ejecución → inspección continúa pendiente. El menú móvil falló. Esta evidencia no basta para aceptar el TPO completo.
