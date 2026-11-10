# Manual de usuario — M3 Obras Públicas

## Acceso

1. Abrir la URL del Front indicada por DevOps.
2. Ingresar usuario y contraseña entregados por canal privado.
3. Verificar que el rol mostrado coincida con la cuenta.
4. Para salir, usar **Cerrar sesión**. No compartir capturas con credenciales o tokens.

## Tareas principales

### Crear y presentar un proyecto

1. Ingresar como Personal de Obras.
2. Abrir **Proyectos** y seleccionar **Crear**.
3. Completar nombre, ubicación, alcance, presupuesto y plazo.
4. Guardar y revisar los datos.
5. Presentar el proyecto para aprobación.

### Aprobar o rechazar

1. Ingresar como Responsable Autorizado.
2. Abrir la bandeja de pendientes.
3. Revisar presupuesto y plazo.
4. Elegir **Aprobar** o **Rechazar** y confirmar el resultado.

### Crear y ejecutar una orden

1. Como Personal de Obras, abrir **Órdenes** y crear una orden.
2. Si el origen es `PROYECTO`, seleccionar el proyecto correspondiente.
3. Asignar cuadrilla y fecha.
4. Como Jefe de Cuadrilla, iniciar, pausar o reanudar según corresponda.
5. Como Operario, completar la tarea con el resultado.
6. Como Inspector, validar o reabrir la orden.

Una transición fuera de orden debe mostrar un conflicto y no modificar los datos.

### Consultar tablero, recursos y cortes

- **Dashboard** resume obras, órdenes y demoras.
- **Recursos** muestra cuadrillas, maquinaria y materiales.
- **Cortes** permite consultar o solicitar cortes asociados a una orden. Una solicitud no equivale a una autorización de Tránsito.

## Mensajes frecuentes

- `401`: sesión ausente, vencida o token inválido. Volver a ingresar.
- `403`: el rol no tiene permiso para esa acción.
- `409`: conflicto de estado o reutilización incorrecta de una clave idempotente.
- `412`: otro proceso modificó el recurso; recargar y repetir con la versión actual.
- `429`: demasiados intentos de login; esperar el tiempo indicado.
- `application/problem+json`: error estructurado con código y detalle.

## Asistente

El asistente responde únicamente sobre Obras. No se deben introducir secretos, datos personales ni instrucciones internas. Si el proveedor está caído, el sistema informa un fallback; eso no altera proyectos ni órdenes.

## Recuperación básica

1. Recargar una sola vez.
2. Confirmar que la URL sea la oficial.
3. Registrar hora, usuario, pantalla, acción y mensaje.
4. No repetir escrituras varias veces sin guardar evidencia.
5. Informar el defecto al equipo QA.
