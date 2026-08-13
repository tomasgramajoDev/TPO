# Reglas de negocio

## Proyectos de obra

1. Una obra nace en Borrador y no comienza sin aprobación.
2. La presentación exige alcance, costos, tiempos, ubicación, responsable técnico y planificación inicial.
3. Pendiente de aprobación bloquea el inicio y los avances.
4. Todo rechazo requiere fundamento y permite corregir desde Borrador.
5. Toda ampliación requiere justificación e historial; no cambia automáticamente el estado de la obra.
6. Una suspensión bloquea nuevas órdenes y avances operativos.
7. Una obra no finaliza con etapas u órdenes pendientes ni sin documentación de cierre.
8. Una obra finalizada es consultable pero no admite nuevas órdenes.

## Órdenes y recursos

1. Una orden no inicia sin cuadrilla asignada.
2. Una cuadrilla no puede tener asignaciones temporalmente superpuestas.
3. La finalización requiere materiales consumidos y evidencia.
4. Completar, validar y reabrir son hechos diferentes.
5. Las reaperturas mantienen el vínculo con el proceso de origen.
6. Una orden que requiere corte de calle no inicia sin autorización de Tránsito.

## Integración y propiedad de datos

1. Cada dato tiene un único módulo propietario.
2. Obras no modifica directamente información de otros módulos.
3. Una solicitud externa y la orden derivada conservan un identificador de correlación.
4. Un evento repetido no debe producir efectos duplicados.
5. Debe existir trazabilidad de publicación y procesamiento.
6. La indisponibilidad temporal de otro módulo no bloquea la operación interna.
7. Los errores deben reintentarse y, agotados los reintentos, enviarse a una Dead Letter Queue.
8. Los cambios incompatibles de contrato deben versionarse y comunicarse a Core y consumidores afectados.
9. El nombre del envelope, la zona horaria y el mecanismo exacto de reintento/DLQ quedan pendientes de Core y de la futura fase técnica.

## Acceso

El ciudadano no accede directamente a Obras. Los reportes de infraestructura ingresan principalmente por Atención Ciudadana.
