# Guion de video — demo de 1 minuto

## Preparación antes de grabar

Dejar abiertas las sesiones necesarias o usar cortes breves entre roles. Preparar un proyecto aprobado y una orden vinculada para evitar esperas. Ocultar contraseñas, pestañas personales y Azure Portal. Grabar el frontend de Azure Test, no `localhost`.

## Guion cronometrado

**0:00–0:08 — Inicio y propósito**  
Pantalla: login y luego tablero.  
Voz: “Este es el módulo de Obras Públicas de la Municipalidad. Está desplegado en Azure y permite gestionar proyectos y órdenes de trabajo con permisos distintos para cada rol.”

**0:08–0:20 — Proyecto**  
Pantalla: proyecto de demo y su estado aprobado.  
Voz: “Personal de Obras crea el proyecto y lo presenta. El Responsable Autorizado lo revisa y aprueba; el sistema impide que el mismo rol se saltee esa autorización.”

**0:20–0:34 — Orden vinculada**  
Pantalla: crear o mostrar una orden con origen `PROYECTO` y su proyecto asociado.  
Voz: “Desde el proyecto aprobado creamos una orden de trabajo. La orden conserva el vínculo con el proyecto y el backend valida esa relación aplicando el patrón Strategy según su origen.”

**0:34–0:49 — Ejecución por roles**  
Pantalla: cambios rápidos de estado o historial preparado.  
Voz: “El Jefe de Cuadrilla la programa e inicia; el Operario completa el trabajo y el Inspector realiza una validación independiente. Cada usuario solo puede ejecutar las acciones de su responsabilidad.”

**0:49–1:00 — Arquitectura y cierre**  
Pantalla: orden `VALIDADA`, luego una placa simple de GitHub a Azure.  
Voz: “Front y Back están separados, el backend usa MVC y PostgreSQL con migraciones Flyway. GitHub Actions valida y construye imágenes, y Terraform despliega la misma versión en Azure Test con los secretos fuera del código.”

## Toma de respaldo

Si una transición tarda, no improvisar ni mostrar Azure Portal: cortar a la orden ya `VALIDADA`. No afirmar que M2, M6 o M7 están integrados hasta que existan contratos y pruebas reales. El mensaje final debe ser que se demuestra un caso completo, seguro y persistido, no todas las capacidades futuras del sistema.
