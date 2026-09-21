# Documentación — Obras Públicas, Infraestructura y Mantenimiento Urbano

Este repositorio conserva el alcance funcional, las reglas, los ciclos de vida, las integraciones, los eventos y las decisiones del Módulo 3. El 2026-08-11 el usuario autorizó el inicio de la fase de desarrollo DevOps. La infraestructura y los pipelines pueden implementarse; el desarrollo de la aplicación requiere una solicitud específica.

## Cómo navegar

- [Alcance general](alcance/alcance-general.md): objetivo, límites y capacidades del módulo.
- [Ciclo de vida de las obras](alcance/ciclo-de-vida-obras.md): estados, transiciones y restricciones.
- [Ciclo de vida de las órdenes](alcance/ciclo-de-vida-ordenes.md): estados conceptuales y diferencias entre completar, validar y reabrir.
- [Usuarios y responsabilidades](alcance/usuarios-y-responsabilidades.md): roles y acciones permitidas.
- [Reglas de negocio](alcance/reglas-de-negocio.md): reglas funcionales e invariantes.
- [Integraciones](integraciones/README.md): índice de contratos por módulo y reglas de certeza.
- [Catálogo de eventos](eventos/README.md): vista navegable de eventos recibidos y publicados.
- [Decisiones confirmadas](decisiones/decisiones-confirmadas.md): acuerdos e instrucciones con evidencia suficiente.
- [Decisiones pendientes](decisiones/decisiones-pendientes.md): contradicciones y definiciones aún abiertas.
- [Historial de cambios](decisiones/historial-de-cambios.md): evolución sin pérdida de contexto.
- [Decisión de cloud y CI/CD](arquitectura/adr-001-cloud-y-cicd.md): elección de Azure, Terraform y GitHub Actions.
- [Operación DevOps](arquitectura/operacion-devops.md): ambientes, despliegues y configuración requerida.
- [Pipeline de aplicaciones](arquitectura/pipeline-aplicaciones.md): contrato que deberán cumplir frontend y backend para construir, promover y desplegar imágenes.
- [Guía DevOps de GitFlow](arquitectura/guia-devops-gitflow.md): ramas, ambientes, cierre de sprint, autorizaciones y releases.
- [Guía DevOps desde cero](../output/pdf/Guia_DevOps_Obras_Publicas_Desde_Cero.pdf): explicación lógica y accesible del recorrido completo, desde GitHub y el código del equipo hasta Azure, con ejemplos, analogías, bitácora, operación diaria y pendientes reales.
- [Guía DevOps para memorizar](../output/pdf/Guia_DevOps_Para_Memorizar.pdf): versión breve para exposición oral, con guion de cinco minutos, frases ancla, hoja de repaso y recorridos completos hacia `development` y `test`.
- [Clase 2](fuentes/clase-2.md): contenidos de la clase clasificados como contexto, recomendaciones o decisiones pendientes.
- [Clase 4 — Integración de aplicaciones](fuentes/clase-4-integracion-aplicaciones.md): tipos, criterios, riesgos y resolución de los cinco escenarios.
- [Backlog, ciclos y prototipos del 2026-08-25](fuentes/backlog-y-ciclos-2026-08-25.md): nueva evidencia recibida y diferencias contractuales detectadas.
- [Diagramas](diagramas/README.md): secuencia propuesta y casos de uso del módulo.
- [Defensa, demo y arquitectura de órdenes](entrega/defensa-demo-arquitectura.md): estado real frente a los criterios de la entrega, guion por rol, demo ejecutable y trabajo pendiente de Front y Back.
- [Plan de testing de la release v0.2.0](entrega/plan-testing-release-v0.2.0.md): casos por rol, resultados esperados, brechas conocidas y formato de evidencia para el equipo de Testing.
- [Ejecución exploratoria de Test](entrega/ejecucion-testing-manual-2026-09-21.md): resultados reales desde el navegador, incidencias y cobertura pendiente.
- [Guion de video de un minuto](entrega/guion-video-demo-1-minuto.md): recorrido cronometrado para mostrar el caso de uso a los profesores.

## Dónde guardar información nueva

1. Identificar el módulo que la envió y su contexto.
2. Compararla con el archivo de la integración correspondiente.
3. Actualizar el catálogo de eventos si agrega, modifica o retira un evento.
4. Si coincide con lo existente, actualizar el contrato manteniendo su estado real.
5. Si contradice lo existente, registrar ambas versiones en [decisiones pendientes](decisiones/decisiones-pendientes.md); no elegir una versión arbitrariamente.
6. Si reemplaza información anterior de forma explícita, actualizar el documento vigente y registrar la sustitución en el [historial](decisiones/historial-de-cambios.md).
7. Si afecta convenciones compartidas, reflejarlo también en [Core Municipal](integraciones/core.md).

## Criterio de certeza

| Etiqueta documental | Significado |
| --- | --- |
| Confirmado | Decisión interna o acuerdo explícito con evidencia suficiente. |
| Propuesto | Diseño del equipo todavía no acordado externamente. |
| Recibido | Información enviada por otro equipo y aún no confirmada bilateralmente. |
| Pendiente | Requiere una decisión o aclaración. |

Los contratos usan los estados normalizados `PROPOSED`, `RECEIVED`, `AGREED`, `CORE_PENDING` y `CONFIRMED`, definidos en [integraciones/README.md](integraciones/README.md).

## Fuentes organizadas

- Consigna general del TPO de Municipalidad UADE: alcance mínimo del Módulo 3 y restricciones académicas para una fase de desarrollo posterior.
- Documento de alcance/requerimientos/eventos del Grupo 5: detalle funcional, ciclos de vida, roles, reglas y catálogo propuesto.
- Comunicación `M6-para-M3`: eventos y payloads tentativos enviados por Ambiente, Higiene y Servicios Urbanos.
- Matriz `Integraciones con Módulos`: enviada por el PO y recibida como fuente transversal de contratos; sus diferencias con comunicaciones directas permanecen pendientes de resolución.
- Clase 1 y cronograma de la asignatura: contexto académico y fechas de evaluación; no sustituyen las autorizaciones explícitas del usuario.
- Clase 2: eventos y sistemas asíncronos, metodologías ágiles, Definition of Done, Git y escalado ágil; se conserva como material docente y no como mandato automático del TPO.
- Clase 4 / Unidad IV: criterios y tipos de integración; se conserva como material docente y sustento de la actividad de MediConecta.
- Backlog, ciclos y prototipos recibidos el 2026-08-25: contexto funcional adicional en estado `RECEIVED`; sus contradicciones no sustituyen el catálogo vigente.
- Instrucciones del usuario de esta sesión: autoridad vigente para la fase de desarrollo DevOps, convenciones y clasificación de certeza.

Cuando dos fuentes difieren, prevalece una sustitución explícita y más reciente solo para el contenido reemplazado; la diferencia queda registrada en el historial o como decisión pendiente.
