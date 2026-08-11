# Ciclo de vida de las obras

## Estados

| Estado funcional | Identificador propuesto | Descripción |
| --- | --- | --- |
| Borrador | `DRAFT` | La información puede modificarse. |
| Pendiente de aprobación | `PENDING_APPROVAL` | Fue presentada para evaluación y no puede comenzar ni registrar avances. |
| Aprobada | `APPROVED` | Fue autorizada y puede prepararse para ejecución. |
| Rechazada | `REJECTED` | Fue rechazada y debe conservar el motivo. Puede corregirse desde Borrador. |
| En ejecución | `IN_PROGRESS` | Está activa y admite avances físicos y presupuestarios. |
| Suspendida | `SUSPENDED` | La ejecución está interrumpida temporalmente. |
| Finalizada | `COMPLETED` | Concluyó, no tiene órdenes pendientes y queda disponible para consulta. |

Los identificadores son propuestas técnicas sujetas a convenciones de Core; los estados y el flujo funcional están definidos por el equipo.

## Transiciones permitidas

```text
Borrador -> Pendiente de aprobación
Pendiente de aprobación -> Aprobada | Rechazada
Rechazada -> Borrador
Aprobada -> En ejecución
En ejecución -> Suspendida | Finalizada
Suspendida -> En ejecución
```

## Condiciones principales

- Para presentar una obra: alcance, ubicación, presupuesto, duración, responsable técnico y planificación inicial.
- Para iniciar: debe estar aprobada y registrar fecha real de inicio, responsable y planificación vigente.
- Una ampliación no cambia automáticamente el estado principal.
- Mientras esté suspendida no pueden iniciarse nuevas órdenes ni cargarse nuevos avances operativos.
- Para finalizar: etapas e hitos completos, avances y costos consolidados, documentación y evidencias de cierre, y ninguna orden pendiente.
- Una obra finalizada no puede recibir nuevas órdenes.

## Eventos asociados

| Transición o hecho | Evento propuesto |
| --- | --- |
| Creación en Borrador | `publicWorksProjectCreated` |
| Presentación | `publicWorksProjectSubmittedForApproval` |
| Aprobación | `publicWorksProjectApproved` |
| Rechazo | `publicWorksProjectRejected` |
| Inicio | `publicWorksProjectStarted` |
| Registro de avance | `publicWorksProgressRegistered` |
| Solicitud/aprobación/rechazo de ampliación | `publicWorksExtensionRequested`, `publicWorksExtensionApproved`, `publicWorksExtensionRejected` |
| Suspensión | `publicWorksProjectSuspended` |
| Reanudación | `publicWorksProjectResumed` |
| Finalización | `publicWorksProjectCompleted` |

El origen histórico de cada evento se conserva en [eventos publicados](../eventos/eventos-publicados.md).
