# Plan de testing funcional — release v0.2.0

## Objetivo y alcance

Este instructivo permite que Testing valide en Azure Test la entrega integrada de Front y Back del Módulo 3 — Obras Públicas. La prueba principal recorre un proyecto y una orden de trabajo con usuarios de distintos roles. También cubre autenticación, permisos, persistencia PostgreSQL, interfaz y reglas centrales del TPO.

No se considera aprobada una prueba solo porque la pantalla cargue: debe comprobarse la respuesta visible, el estado final y que un rol sin permiso sea rechazado.

## Ambiente y acceso

- Ambiente: `test`.
- Frontend: usar únicamente el enlace público entregado por DevOps.
- API: el navegador accede por rutas relativas `/api/...`; Testing no debe reemplazarlas por URLs de Azure ni por `localhost`.
- Base: PostgreSQL administrado en Azure; no se comparte su contraseña con Testing.
- Credenciales: DevOps entrega por un canal privado una contraseña temporal común para cinco cuentas. No debe copiarse en Git, capturas, Trello ni este documento.

| Usuario | Rol | Parte del flujo que prueba |
| --- | --- | --- |
| `personal.obras` | `PERSONAL_OBRAS` | Crea y presenta proyectos; crea órdenes, cuadrillas y cortes. |
| `responsable` | `RESPONSABLE_AUTORIZADO` | Aprueba o rechaza proyectos. |
| `jefe.cuadrilla` | `JEFE_CUADRILLA` | Programa, inicia, pausa y reanuda órdenes. |
| `operario` | `OPERARIO_CONTRATISTA` | Registra la finalización operativa. |
| `inspector` | `INSPECTOR_OBRA` | Valida o reabre el trabajo terminado. |

Usar nombres que comiencen con `QA-` y anotar todos los identificadores creados. No borrar evidencia antes de cerrar el informe.

## Preparación

1. DevOps confirma que Front, Back y PostgreSQL están encendidos y que `/api/health` responde correctamente.
2. Abrir el frontend en una ventana privada para evitar sesiones viejas.
3. Disponer de las cinco cuentas y la contraseña recibida en privado.
4. Crear una carpeta de evidencias con fecha. Para cada caso guardar captura inicial, captura final, usuario utilizado y resultado.
5. Si aparece un error, registrar hora, pantalla, acción anterior, usuario, datos ingresados y respuesta visible. No repetir muchas veces sin guardar la primera evidencia.

## Caso principal: proyecto y orden de trabajo

### QA-01 — Autenticación y rol persistido

1. Iniciar sesión con cada una de las cinco cuentas.
2. Comprobar que la interfaz muestra el rol correcto.
3. Recargar la página: la sesión debe continuar vigente.
4. Cerrar sesión e intentar reutilizar la pantalla protegida.

Resultado esperado: las credenciales válidas ingresan; una contraseña incorrecta es rechazada; la recarga conserva la sesión; después de cerrar sesión los recursos protegidos vuelven a pedir autenticación.

### QA-02 — Crear y presentar un proyecto

1. Ingresar como `personal.obras`.
2. Crear `QA-Proyecto-Plaza-<fecha>` con ubicación, descripción, alcance, presupuesto y plazo válidos.
3. Guardarlo como borrador y comprobar sus datos.
4. Presentarlo para aprobación.
5. Intentar aprobarlo con el mismo usuario.

Resultado esperado: el proyecto se persiste y cambia del estado borrador al estado pendiente de aprobación. `PERSONAL_OBRAS` no puede aprobarlo.

### QA-03 — Aprobar el proyecto

1. Cerrar sesión e ingresar como `responsable`.
2. Abrir el proyecto creado en QA-02.
3. Aprobarlo.
4. Recargar y comprobar que el estado permanece aprobado.

Resultado esperado: solo `RESPONSABLE_AUTORIZADO` realiza la aprobación y el estado persiste en PostgreSQL. Como variante, crear un segundo proyecto y verificar el rechazo con su motivo.

### QA-04 — Crear una orden vinculada al proyecto

1. Ingresar como `personal.obras`.
2. Desde el proyecto aprobado, crear `QA-OT-Proyecto-<fecha>` con origen `PROYECTO`.
3. Comprobar que la respuesta y el detalle muestran el `projectId` correcto.
4. Intentar crear otra orden con origen `PROYECTO` sin proyecto y otra con un identificador inexistente.

Resultado esperado: la orden válida queda vinculada al proyecto; la falta de `projectId` se rechaza como petición inválida y un proyecto inexistente se informa como no encontrado. Las órdenes manuales anteriores siguen siendo compatibles.

### QA-05 — Programar y ejecutar la orden

1. Como `personal.obras`, crear o elegir una cuadrilla disponible y asignarla a la orden.
2. Ingresar como `jefe.cuadrilla` y programar la orden.
3. Iniciarla, pausarla, comprobar el estado, reanudarla y volver a comprobarlo.
4. Ingresar como `operario` y completar la orden.

Resultado esperado: se respeta el orden de estados permitido; no se inicia sin cuadrilla; cada cambio persiste después de recargar. Un usuario de otro rol recibe una denegación y no altera el estado.

### QA-06 — Inspeccionar y cerrar

1. Ingresar como `inspector`.
2. Abrir la orden completada y validarla.
3. Crear o reutilizar otra orden completada para probar “rechazar/reabrir”.

Resultado esperado: la primera termina `VALIDADA`; la segunda queda `REABIERTA` o en el estado de revisión definido por la interfaz. Completar la tarea no equivale a validarla: son acciones de roles diferentes.

## Casos complementarios del TPO

| ID | Qué probar | Resultado esperado |
| --- | --- | --- |
| QA-07 | Acceder sin sesión a proyectos, órdenes y demás recursos protegidos. | HTTP 401 o regreso al login; nunca datos del sistema. |
| QA-08 | Ejecutar una acción de escritura con un rol incorrecto. | HTTP 403 o mensaje equivalente; ningún cambio persistido. |
| QA-09 | Campos obligatorios, importes negativos, textos vacíos e identificadores inexistentes. | Mensaje comprensible, sin pantalla rota ni registro incompleto. |
| QA-10 | Listados, filtros y detalle de proyectos, órdenes, recursos, cuadrillas y cortes. | Los datos creados aparecen una sola vez y sobreviven a la recarga. |
| QA-11 | Solicitar un corte asociado a una orden. | Se conserva el vínculo y se informa el estado de la solicitud. No asumir autorización de M7 si no existe respuesta real. |
| QA-12 | Dashboard después de crear y cambiar estados. | Indicadores coherentes con los datos del ambiente. |
| QA-13 | Vista de escritorio y móvil; textos, botones, carga y error. | Interfaz utilizable en español, sin desbordes ni acciones invisibles. |
| QA-14 | Intentar abrir la app usando solo el enlace del Front. | Todo el tráfico funcional pasa por `/api`; no aparecen `localhost` ni URLs directas del Back. |

## Controles técnicos a cargo de DevOps

- La imagen de Back corresponde al commit aprobado y ejecuta Flyway V3 y V4 al iniciar.
- La imagen de Front corresponde al commit aprobado y usa el contrato actualizado.
- `/api/health` informa aplicación y base disponibles.
- Las variables `DB_*`, `JWT_SECRET`, `AUTH_PASSWORD` y `AUTH_BOOTSTRAP_USERS` se inyectan como secretos y no aparecen en el repositorio ni en el navegador.
- Al reiniciar Back, las cuentas persisten: el bootstrap no sobrescribe contraseñas ni roles existentes.
- El despliegue conserva el mismo artefacto inmutable que superó CI.

## Límites y pruebas pendientes

Los eventos de M2, M6 y M7 siguen sin contrato bilateral confirmado. Se puede revisar la pantalla o el punto de extensión, pero no declarar una integración real aprobada ni inventar payloads. Tampoco debe marcarse como aprobado aquello que la versión no implemente todavía, especialmente solapamiento de cuadrillas, evidencia y materiales obligatorios, autorización externa del corte antes de iniciar, hitos/ampliaciones/suspensión/cierre de proyecto o permisos definitivos de `INGENIERO_ARQUITECTO`.

Estos hallazgos se registran como brechas funcionales del TPO, no como errores del tester.

## Criterio de salida

La release puede aceptarse para la demostración cuando QA-01 a QA-06 pasan de punta a punta, QA-07 y QA-08 prueban la seguridad por rol, no hay defectos críticos abiertos, Front no presenta errores bloqueantes y DevOps adjunta health, SHA desplegados y ejecución de migraciones. Todo resultado debe quedar como `APROBADO`, `FALLÓ`, `BLOQUEADO` o `NO IMPLEMENTADO`, con evidencia.

## Formato del informe

| Caso | Resultado | Usuario | Datos/ID | Evidencia | Observación |
| --- | --- | --- | --- | --- | --- |
| QA-01 | APROBADO/FALLÓ |  |  | archivo o enlace |  |

Un defecto debe incluir: título breve, severidad (`Crítica`, `Alta`, `Media`, `Baja`), pasos exactos, resultado esperado, resultado obtenido, hora y captura.
