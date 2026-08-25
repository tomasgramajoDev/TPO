# Backlog, ciclos y prototipos recibidos el 2026-08-25

## Estado de las fuentes

El usuario aportó `Backlog.pdf`, `Ciclo Administrativo Proyecto Obra Publica.pdf`, `Ciclo Ordenes de Trabajo e Integraciones.pdf` y prototipos de interfaz manuscritos y digitales. Se registran como información **RECEIVED**. El nombre interno “PO” del backlog no alcanza para confirmar por sí solo su autoría ni convierte los contratos descritos en acuerdos bilaterales.

## Cobertura funcional observada

Las fuentes describen creación y aprobación de proyectos, planificación y avances, ampliaciones, suspensión y cierre; creación de órdenes desde alertas externas; programación, asignación, ejecución, materiales y evidencia; validación o reapertura por inspección; y solicitudes de corte de calle. Los roles visibles son Personal de Obras, Ingeniero/Arquitecto, Responsable autorizado, Jefe de Cuadrilla, Operario/Contratista e Inspector de Obra.

Los dos documentos de ciclo ya son diagramas de secuencia. Por esa razón, el entregable faltante era un diagrama de casos de uso. Se agregó además una secuencia controlada de aprobación y publicación asíncrona para mostrar la participación de PostgreSQL y del broker sin ocultar las decisiones todavía abiertas.

## Diferencias que no deben resolverse de forma implícita

- `ticketCreated` frente a `complaintRouted` para el ingreso desde M2.
- `streetClosureApproved` frente a `streetClosureAuthorized` para la respuesta de M7.
- `updateTicketStatus` aparece en un ciclo, pero no en el catálogo vigente.
- El backlog asigna `workOrderCompleted` definitivo a la inspección; el ciclo y el catálogo separan `workOrderCompleted`, `workOrderValidated` y `workOrderReopened`.
- El backlog indica que el borrador no publica evento; la matriz recibida del PO incluye `publicWorksProjectCreated`.
- La mención a “App Móvil” entra en tensión con el alcance confirmado de un portal web responsive sin aplicación móvil independiente.

Estas diferencias permanecen abiertas en `docs/decisiones/decisiones-pendientes.md`.
