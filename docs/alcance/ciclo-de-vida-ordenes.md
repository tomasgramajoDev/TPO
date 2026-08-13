# Ciclo de vida de las órdenes de trabajo

Una `WorkOrder` representa una intervención concreta, creada manualmente o a partir de una solicitud externa.

## Estados conceptuales

| Estado | Sentido funcional |
| --- | --- |
| `CREATED` | Orden registrada. |
| `SCHEDULED` | Tiene fecha u horario previstos. |
| `ASSIGNED` | Tiene cuadrilla responsable. |
| `IN_PROGRESS` | La cuadrilla inició la ejecución. |
| `PAUSED` | Ejecución detenida temporalmente. |
| `DELAYED` | No puede cumplir el momento previsto. |
| `COMPLETED` | La cuadrilla declaró terminada la ejecución y cargó evidencia. |
| `VALIDATED` | Un inspector confirmó que el resultado es correcto. |
| `REOPENED` | La inspección exige correcciones y la orden vuelve al circuito operativo. |

## Distinciones que no deben mezclarse

- `workOrderCompleted`: finalización física informada por la cuadrilla; no prueba por sí sola la conformidad final.
- `workOrderValidated`: conformidad del inspector.
- `workOrderReopened`: resultado no satisfactorio que requiere correcciones.

## Reglas confirmadas

- No se inicia una orden sin cuadrilla asignada.
- Una cuadrilla no puede tener tareas temporalmente superpuestas.
- El cierre operativo requiere materiales consumidos y evidencia.
- Si la obra está suspendida, no pueden iniciarse nuevas órdenes asociadas.
- Si la intervención requiere corte de calle, no puede comenzar sin autorización de Tránsito.
- Una orden originada externamente debe conservar el identificador de origen.
- Una reapertura mantiene la correlación con el proceso original.

## Secuencia mínima conocida

La documentación confirma la progresión conceptual `CREATED` → programación/asignación → `IN_PROGRESS` → `COMPLETED` → `VALIDATED` o `REOPENED`. No está cerrada una matriz exhaustiva de transiciones, en especial para `PAUSED`, `DELAYED`, reprogramaciones y reingreso desde `REOPENED`; se registra como decisión pendiente.

## Eventos propuestos

`workOrderCreated`, `workOrderScheduled`, `workOrderAssigned`, `workOrderStarted`, `workOrderPaused`, `workOrderDelayed`, `workOrderRescheduled`, `workOrderCompleted`, `workOrderValidated` y `workOrderReopened`.
