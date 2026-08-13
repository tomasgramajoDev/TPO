# Usuarios y responsabilidades

| Rol | Responsabilidades principales |
| --- | --- |
| Personal de Obras Públicas | Crear y modificar proyectos, crear órdenes, registrar información administrativa, solicitar cortes y consultar avances e indicadores. |
| Ingeniero o arquitecto | Definir etapas e hitos, planificar, registrar avances, controlar progreso físico/presupuestario, solicitar ampliaciones y adjuntar documentación. |
| Responsable autorizado | Aprobar o rechazar proyectos, autorizar ampliaciones, suspender o reanudar obras y validar su cierre. |
| Jefe de cuadrilla | Consultar órdenes, confirmar recursos, organizar, iniciar, pausar, demorar o reprogramar tareas y registrar observaciones. |
| Operario o contratista | Ejecutar tareas, registrar tiempos y consumos, cargar fotografías, informar inconvenientes y declarar finalización. |
| Inspector de obra | Consultar evidencias, inspeccionar, validar o rechazar resultados y reabrir una orden. |
| Ciudadano | No accede directamente. Registra problemas mediante Atención Ciudadana y recibe seguimiento por ese canal. |

## Rol del usuario

El usuario responsable de este repositorio cumple el rol **DevOps** dentro del equipo. En la futura fase de desarrollo será responsable de:

- Seleccionar el proveedor cloud que utilizará el proyecto.
- Diseñar, crear y administrar la infraestructura y los servicios cloud.
- Definir la infraestructura como código con Terraform, evitando que el aprovisionamiento ordinario dependa de ingresar manualmente a servidores.
- Preparar y administrar los pipelines de integración y despliegue.
- Lanzar o autorizar los despliegues del sistema.
- Mantener el flujo de promoción de versiones entre ambientes.

## Flujo de despliegue previsto

1. Al completarse el evento acordado sobre un pull request, la versión correspondiente se despliega en el ambiente de desarrollo.
2. Cuando se aprueba un release, la versión se despliega en el ambiente de prueba.
3. El lanzamiento o la autorización operativa del despliegue corresponde a DevOps.

El proveedor cloud, los servicios administrados, los mecanismos de aprobación y los eventos técnicos exactos de cada pipeline todavía deben definirse. Durante la fase documental, estas responsabilidades se registran como alcance futuro y no autorizan tareas de infraestructura, despliegue, automatización ni pipelines.

## Datos requeridos por acción

- Crear obra: nombre, descripción, alcance, ubicación, presupuesto estimado, inicio y duración estimados, responsable técnico y contratista cuando corresponda.
- Aprobar o rechazar: decisión, motivo u observación, presupuesto/plazo aprobados cuando aplique, fecha y responsable.
- Registrar avance: obra, etapa o hito, porcentaje físico, monto ejecutado, fecha, observaciones y evidencia.
- Finalizar orden: trabajo realizado, fecha/hora, materiales consumidos, fotografías, observaciones y resultado.
- Validar orden: resultado de inspección, conformidad o rechazo, observaciones, evidencia y motivo de reapertura cuando corresponda.

La matriz detallada de permisos técnicos queda fuera de la fase actual.
