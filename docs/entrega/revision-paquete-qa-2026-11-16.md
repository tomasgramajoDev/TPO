# Revisión del paquete QA contra los criterios de Clase 15

**Fecha:** 16 de noviembre de 2026  
**Paquete revisado:** `QA_16-11-26.zip`  
**Candidata vigente:** tag `v2.0-entrega4`, commit TPO `fa1fb579f5a6d374a287fb5cc7bab4ed3e4fb692`.

## Dictamen

El paquete de Tobias contiene el conjunto documental mínimo y evidencia manual valiosa, pero el PDF no puede entregarse sin actualización. Fue redactado contra una candidata anterior y por eso concluye `17/31` y `NO ACEPTADA`, aunque varias dependencias que computa como pendientes ya quedaron cerradas.

El contenido extraído del ZIP fue revisado con Gitleaks en modo `no-git`: no se detectaron secretos evidentes en aproximadamente 943 MB. Este resultado no reemplaza la revisión visual de videos y capturas antes de publicarlos.

No se debe cambiar un estado a PASS solo por esta revisión. Los cierres técnicos se incorporan como evidencia de DevOps/Core; los casos manuales afectados por una nueva versión deben repetirse en Azure Test.

## Correcciones documentales obligatorias

1. Cambiar Backend `f45e6daf...` por `00e0be1167180cf95d678a720915f3057652016c` y Frontend `7c57e3c5...` por `4d1a885fe029c991a3f224a036622fae209baa41`.
2. Actualizar las suites a 140 pruebas Back y 64 pruebas Front, con 7 E2E después de incorporar la regresión responsive a 768 px.
3. Reemplazar la corrida antigua de k6 por el gate del tag `43890063632`: arranque limpio 140 s, 50 VUs durante 301,2 s, 44.746 requests, p95 7,84 ms, tasa de fallos 0 y checks 100%.
4. Marcar SonarCloud, JWT expirado/firma alterada/`alg=none`/issuer, Gitleaks, ZAP, logs y resiliencia automatizada con la evidencia final ya disponible.
5. Cerrar como evidencia externa M1 `approved/rejected/completed`, M2 `STARTED/PROGRESS/RESOLVED`, M6 principal/secundarios y M7 circuito base, variantes A/B/C y accidente.
6. Eliminar `Core: habilitar 57.156.67.226/32` como pendiente: la conectividad de `module_obras` y el consumidor de `q.obras` fueron recuperados y verificados.
7. No computar `TC-017`, `TC-019`, `TC-021`, `TC-023` ni la resiliencia de Outbox como pendientes generales cuando ya existe evidencia confirmada. Los escenarios alternativos no ejecutados deben quedar separados como cobertura adicional.
8. Reclasificar D-10 y D-14 como `CORREGIDO - REQUIERE RETEST`. El Backend final acepta 301 caracteres, rechaza más de 1000 con 400 y exige motivo para rechazar un proyecto.
9. Reclasificar D-01 como `REQUIERE RETEST EN CANDIDATA FINAL`: el Front final alinea el formulario y valida el rango temporal antes de enviar.
10. No presentar D-15 como funcionalidad ausente sin revisar el menú **Integraciones** de la candidata final. Existe una pantalla de eventos emitidos/recibidos con estado, origen, correlación, timestamps, errores y refresco automático. Si la HU exige métricas agregadas de broker, registrar la diferencia de alcance; no afirmar que no existe observabilidad.
11. Reclasificar D-08 como `CORREGIDO - REQUIERE RETEST`: el Front PR #25 amplió el breakpoint compacto y agregó una regresión E2E que confirma cero overflow horizontal a 768 px.
12. Corregir la declaración de IA: no afirmar un modelo de Claude que el equipo no pueda acreditar y completar versión/herramienta por integrante. Mantener la firma nominal humana pendiente.
13. Confirmar los legajos de Juan José D'Agosto y Nadine Lewit; el PDF muestra el mismo legajo para ambos.
14. Corregir el índice de evidencias: el PDF declara `Testing/Jira_Import_Casos_QA.csv`, pero ese archivo no está incluido en `QA_16-11-26.zip`. Debe agregarse o retirarse la referencia.

## Casos manuales nuevos o a repetir

| Caso | Pasos mínimos | Resultado esperado | Evidencia |
| --- | --- | --- | --- |
| RETEST-D01-A | Crear un corte con una OT existente, fechas futuras y fin posterior al inicio. | Solicitud creada, sin 400/404. | Video y captura del estado persistido tras recarga. |
| RETEST-D01-B | En el formulario de corte, colocar fin anterior al inicio. | Bloqueo en Front con mensaje claro; no se envía request. | Video que muestre formulario y ausencia de alta. |
| RETEST-D10-A | Crear proyecto con descripción de 301 caracteres. | Alta exitosa. | Video o captura de proyecto creado. |
| RETEST-D10-B | Probar por API una descripción de 1001 caracteres. | 400 `VALIDATION_ERROR`, sin 500 ni alta. | Request/response sanitizado. |
| RETEST-D14-A | Rechazar un proyecto sin motivo. | Front no envía; muestra motivo obligatorio. | Video. |
| RETEST-D14-B | Rechazar con motivo válido. | Proyecto `RECHAZADO` y observación persistida tras recarga. | Video y captura. |
| RETEST-D08 | Abrir Órdenes a 768 x 1024. | Sin overflow horizontal ni texto/acciones cortados. | Captura completa y medición de overflow. |
| RETEST-D15 | Abrir **Integraciones**, esperar el refresco y filtrar emitidos/recibidos. | Lista observable con estado, origen, correlación y timestamps; errores visibles si existen. | Video corto. |
| SEC-LIVE | Elegir BFLA y uno de los cuatro JWT inválidos. | 403/401 uniforme y sin mutación. | Request/response sin token visible. |

## Actividades que no se resuelven con otro test

- Firmar nominalmente la declaración de IA.
- Cargar el PDF único y sus enlaces de evidencia en Teams antes del horario indicado.
- Confirmar legajos y responsables.
- Ensayar la tarea aleatoria con el manual y la demo en vivo.
- Mantener documentados los riesgos ZAP Medium/Low aceptados y el límite de no apagar unilateralmente el broker compartido de Core.

## Criterio para recalcular el porcentaje

El porcentaje debe recalcularse después de incorporar la evidencia vigente y ejecutar los retests. No corresponde conservar `55%`, pero tampoco declarar `>=95%` sin revisar cada fila de la matriz. La fuente de verdad final debe ser una sola matriz con HU, criterio, caso, resultado, evidencia y defecto.
