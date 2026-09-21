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

## Segunda ejecución manual: seis perfiles y flujo nuevo

Se continuó en el Front público de Test el 2026-09-21, aproximadamente entre las 19:07 y las 19:17 de Argentina. Se ingresó desde la interfaz con `ingeniero.arquitecto` (en la primera ejecución), `personal.obras`, `responsable`, `jefe.cuadrilla`, `operario` e `inspector`. La contraseña compartida se obtuvo del secreto del ambiente mediante un intercambio cifrado temporal; no se incorporó a Git ni a este informe. El workflow temporal de recuperación se retiró al terminar (PR `#37` y `#38`). Una solicitud de login recibió inicialmente HTTP 503 durante el arranque; `/api/health` respondió luego 200 con `database: up` y el segundo intento de login funcionó. No se interpreta el 503 aislado como caída persistente.

| Caso | Resultado observado | Evidencia de interfaz y límite |
| --- | --- | --- |
| QA-01 | APROBADO en los seis ingresos; PARCIAL en carga inicial | La pantalla mostró cada rol correcto. La sesión sobrevivió una recarga y «Salir» volvió al login. La primera navegación tras ingresar volvió a mostrar en algunos perfiles «Se requiere un token valido»; recargar normalizó los datos. |
| QA-02 | APROBADO | `personal.obras` creó el proyecto ficticio `QA-UI-Proyecto-20260921-1907`, ID `2`, en Borrador; el formulario vacío informó errores por campo. «Enviar» lo pasó a Pendiente aprobación. El botón de aprobar permaneció deshabilitado para ese rol. |
| QA-03 | APROBADO | `responsable` aprobó el proyecto #2 por $1.500.000 y 15 días, con observación QA. Tras recarga, lista y detalle mostraron Aprobado, presupuesto, plazo y fecha de aprobación. |
| QA-04 | APROBADO para vínculo y ausencia; NO EJECUTADO para ID inexistente | El formulario rechazó una orden de origen Proyecto sin seleccionar proyecto, con «Seleccioná un proyecto válido». Al elegir proyecto #2 y la cuadrilla existente, se creó la OT #2 en estado Asignada. El detalle mostró origen Proyecto, vínculo #2 y cuadrilla. No se probó un proyecto ID inexistente porque el selector no lo permite desde la UI. |
| QA-05 | PARCIAL / BLOQUEADO para Programar y Completar | `jefe.cuadrilla` inició la OT #2, la pausó y la reanudó; lista y detalle mostraron las transiciones hasta En ejecución. «Programar» no avanzó porque este navegador integrado no admite el `window.prompt()` que invoca el Front; consola: `Error: prompt() is not supported.` El mismo límite impidió a `operario` completar la OT. No se marca Programar ni Completar como aprobados, ni como falla comprobada en un navegador estándar. |
| QA-06 | BLOQUEADO por QA-05 | `inspector` ingresó y vio la OT #2 En ejecución; «Validar» estuvo deshabilitado, conforme al estado. No se pudo probar Validar/Reabrir con una OT recién completada desde este navegador. |
| QA-07 | PARCIAL | Se mantiene el control previo de recurso protegido sin sesión: HTTP 401. No se recorrieron todas las rutas anónimas. |
| QA-08 | PARCIAL | La UI deshabilitó aprobar para Personal, crear proyecto/orden para roles no autorizados, y validar antes de completar. La comprobación previa de denegación HTTP 403 por rol permanece documentada en la bitácora de despliegue; esta ejecución no envió nuevas escrituras ilegales. |
| QA-09 | PARCIAL | Proyecto vacío, orden Proyecto sin proyecto y corte vacío mostraron errores específicos sin crear datos. No se probaron importes negativos ni todos los límites. |
| QA-10 | PARCIAL | Proyecto #2, OT #2, cuadrilla y detalle fueron visibles; el filtro «En ejecución» dejó solo la OT #2. Los datos sobrevivieron a cambios de rol y recarga. |
| QA-11 | APROBADO para solicitud local; M7 NO IMPLEMENTADO | `personal.obras` creó una solicitud de corte ficticia para OT #2 del 2026-09-23 al 2026-09-24, ID `c18ef086-83da-4def-a62c-a0f5a9c5fb42`, en Pendiente. Persistió tras recarga. La pantalla aclara que autorización/rechazo de Tránsito depende de la integración externa. |
| QA-12 | PARCIAL | Tras recarga, el tablero mostró 2 obras activas, 1 orden abierta y ambos proyectos con 0% de avance. No se completó la OT ni se midió el impacto de ese estado. |
| QA-13 | FALLÓ en móvil | Persiste el solapamiento de navegación a 390 px registrado arriba. Escritorio permitió el flujo parcial descrito. |
| QA-14 | PARCIAL | Las operaciones observadas se hicieron desde el Front público y su `/api`; no se cubrieron todas las rutas. La etiqueta `development - /api` persiste en Test. |

### Incidencias y restricciones diferenciadas

- **Media, Front:** al cambiar de perfil inmediatamente después de enviar/aprobar el proyecto, la lista mostraba el estado nuevo, pero el panel de detalle que había quedado abierto seguía mostrando `Borrador` y campos «Sin aprobar». Al volver a abrir el detalle tras recargar, mostró correctamente `Aprobado`. Parece estado de detalle no invalidado después de la mutación; no es evidencia de pérdida en PostgreSQL.
- **Media, Front:** la carga inicial tras login sigue mostrando esporádicamente «Se requiere un token valido» hasta reintento/recarga.
- **Media, usabilidad y automatización:** Programar, Completar y Validar dependen de cuadros nativos `window.prompt()`. Este navegador de prueba no los implementa; requiere verificación manual en Chrome/Edge normal o formularios/modales dentro de la aplicación. No atribuir el error del navegador integrado al backend.
- **Baja, presentación:** `development - /api` aparece en el ambiente Test.
- **Baja, dato explicativo por revisar:** el tablero mostró «Ordenes externas 0 — origen no manual» aunque las OT #1 y #2 figuran como origen Proyecto. Confirmar si el contador excluye deliberadamente Proyecto; de ser así, la leyenda es imprecisa.
- **Fuera de alcance confirmado:** autorización M7 y contratos/eventos M2/M6/M7 no se aceptan por ver una pantalla.

**Estado de aceptación al cierre:** no se puede declarar terminado el flujo completo QA-01 a QA-06. Proyecto, aprobación, orden y parte de la ejecución se verificaron con interacción real; programación, finalización e inspección quedan por probar en un navegador que admita los diálogos o tras sustituirlos en el Front. La OT de prueba #2 permanece En ejecución y el corte de prueba permanece Pendiente. No se alteraron datos reales fuera de Test.

## Tercera ejecución: Front corregido e infraestructura v0.2.8

Se publicó en Test el Front del commit `f8d6a585e0f8e17fb19fa0a76d2e9de72ca6fc30` mediante la release de infraestructura `v0.2.8`. El workflow `35646785528` terminó correctamente: aplicó el plan aprobado, inició PostgreSQL, y verificó los seis logins por el proxy del Front. Esta ejecución de navegador continuó con datos ficticios `QA-` en el mismo ambiente.

| Caso | Resultado comprobado en esta ejecución | Pendiente o límite |
| --- | --- | --- |
| QA-01 | APROBADO: el pipeline verificó seis logins; por interfaz se volvió a ingresar con Personal, Jefe, Operario e Inspector y apareció el rol correcto. No reapareció el error inicial de token. | No se repitió contraseña incorrecta de cada usuario; esa variante se había probado antes. |
| QA-02 y QA-03 | APROBADOS en la ejecución anterior: proyecto #2 creado, presentado y aprobado desde la interfaz. | No se creó otro proyecto innecesario. |
| QA-04 | APROBADO: Personal creó OT #3 de origen Proyecto, vinculada al proyecto #2 y a la cuadrilla QA. El listado confirmó ID, origen y vínculo. Una petición con `projectId=999999` devolvió HTTP 404 y el total de órdenes siguió en 3. | El selector impide ingresar el ID inexistente por interfaz; esa variante se comprobó por API. |
| QA-05 | APROBADO: Jefe programó OT #3 para 2026-09-22; se rechazó primero la fecha vacía. Después la inició, pausó y reanudó, con cada estado visible tras consultar el backend. Operario completó la orden con resultado; el resultado vacío mostró error obligatorio. | La evidencia fotográfica no es obligatoria en la versión actual. |
| QA-06 | APROBADO: Inspector rechazó la OT #3 y la dejó Reabierta; el motivo vacío fue rechazado. Jefe reanudó el retrabajo, Operario la completó de nuevo con resultado corregido e Inspector la dejó Validada. | No implica cierre automático del proyecto. |
| QA-07 | PARCIAL: sin token, `GET /api/public-works/projects` y `GET /api/public-works/work-orders` devolvieron HTTP 401. | No se repitieron todas las rutas protegidas. |
| QA-08 | APROBADO: la interfaz deshabilitó acciones ajenas a cada rol. Además, `operario` intentó `POST /api/public-works/projects` y recibió HTTP 403; el total permaneció en dos proyectos. | No se probaron todas las combinaciones rol/acción. |
| QA-09 | PARCIAL: se comprobaron campos obligatorios en Programar, Completar y Reabrir. Un presupuesto estimado `-1` fue rechazado con HTTP 400; consultar el proyecto `999999` devolvió HTTP 404. El total siguió en dos proyectos. | Faltan longitudes extremas y todas las reglas de validación. |
| QA-10 | PARCIAL: la OT #3 permaneció Validada tras recargar. El filtro Validada mostró solo las OT #1 y #3; el detalle de #3 conservó proyecto #2 y cuadrilla. | No se recorrieron todos los filtros y recursos otra vez. |
| QA-11 | APROBADO para solicitud local: tras recargar, el corte QA `c18ef086-83da-4def-a62c-a0f5a9c5fb42` siguió vinculado a OT #2 y Pendiente. | Autorización de M7 no implementada. |
| QA-12 | PARCIAL: tras validar la OT #3, el tablero mostró una orden abierta (la OT #2), dos proyectos activos y la leyenda precisa que excluye origen Proyecto del indicador externo. | El progreso físico del proyecto permaneció en 0%; esta prueba no registró avances de etapa. |
| QA-13 | APROBADO para navegación móvil a 390 px: los seis botones ocupan dos columnas sin superponerse ni exceder los 390 px; medición DOM: `bodyScrollWidth=375`, `innerWidth=390`. | Resto de vistas móviles no revisadas exhaustivamente. |
| QA-14 | APROBADO para el flujo recorrido: Front mostró `test - /api` y todas las operaciones se hicieron en el origen del Front. | No es una auditoría de todas las rutas de red. |

El navegador integrado se cerró inesperadamente al intentar abrir su selector nativo de fecha; se reabrió la página y se ingresó la fecha directamente en el campo. La programación persistió, por lo que no se atribuye ese fallo del selector al código de la aplicación. La OT #3 quedó **Validada**; la OT #2 y el corte ficticio de la ejecución anterior permanecen como datos de prueba, no como trabajo real.

**Criterio de salida actualizado:** el caso de uso principal QA-01 a QA-06 está demostrado de punta a punta con roles y PostgreSQL. Sigue sin corresponder declarar cumplido el TPO completo: las integraciones bilaterales M2/M6/M7, evidencia/materiales obligatorios y otras brechas del plan no están implementadas o confirmadas. La release es candidata a demo del alcance vigente, con estas limitaciones explícitas.
