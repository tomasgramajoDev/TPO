# Casos de uso — Obras Públicas

## Actores internos

| Actor | Casos de uso principales |
| --- | --- |
| Personal de Obras | Crear y editar proyecto; solicitar aprobación; crear orden desde alerta. |
| Ingeniero/Arquitecto | Planificar etapas y avances; solicitar ampliación. |
| Responsable autorizado | Aprobar o rechazar proyecto; suspender, reanudar o cerrar obra. |
| Jefe de Cuadrilla | Programar y asignar orden; iniciar, pausar o reprogramar. |
| Operario/Contratista | Registrar materiales y evidencia; finalizar tarea operativa. |
| Inspector de Obra | Validar, rechazar o reabrir la orden. |

## Sistemas externos

| Actor externo | Interacción representada | Estado |
| --- | --- | --- |
| M2 Atención Ciudadana | Enviar reclamo o escalamiento; recibir estados de orden. | `RECEIVED` |
| M6 Ambiente | Enviar alerta ambiental; recibir estados de orden. | `RECEIVED` |
| M7 Tránsito | Recibir solicitud de corte; responder autorización o rechazo. | `RECEIVED` |
| M1 Expedientes | Recibir hitos del proyecto; enviar resolución administrativa. | `RECEIVED` |
| Core M9 / Broker | Enrutar eventos y aplicar convenciones compartidas. | `CORE_PENDING` |

La referencia del backlog a una aplicación móvil se interpreta únicamente como uso responsive del portal hasta que el equipo autorice una aplicación independiente. Esta interpretación permanece registrada como diferencia pendiente.
