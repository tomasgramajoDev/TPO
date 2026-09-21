# Auditoría de entrega integral del TPO — 2026-09-21

## Criterio de alcance

Fuente académica: `TPO - Desarrollo de Apps II - Gestión de municipalidad.pdf`, especialmente las páginas 2–4, 9–10 y 22. Este control distingue la **demo operativa de la primera entrega** del **TPO completo**. La matriz QA-01 a QA-14 del informe de testing cierra el recorrido implementado, no todos los requisitos de la cátedra.

## Verificado

| Área | Evidencia | Estado |
| --- | --- | --- |
| Despliegue compartido | Front y Back públicos en Azure Test; PostgreSQL respondió `up` por `/api/health`; recorrido de roles y caso de uso QA documentado. | Verificado para demo. |
| Git y CI | PR de aplicación anteriores integrados a ramas de release; Front PR `#12` integró 58 pruebas y gate de cobertura en `develop`; Back PR `#9` incorpora JaCoCo y espera CI/merge. | Parcial hasta fusionar y ejecutar CI de Back. |
| Cobertura Front | `npm run test:coverage` con inclusión explícita de todo `src`: 85,84% líneas y 86,05% sentencias; 58 pruebas. El pipeline falla si cae bajo 85% en esas dos métricas. | Verificado local y CI del PR `#12`. Cobertura de ramas: 77,81%. |
| Cobertura Back | 60 pruebas H2 y JaCoCo: 85,18% de líneas en la medición previa; `clean verify` con el nuevo gate terminó correctamente en Windows. | Verificado local; CI de PR `#9` pendiente. Cobertura de ramas: ~72%, no 85%. |
| Arquitectura de Back | Capas Controller, Service, Repository, Mapper, Model y patrón Strategy para creación de órdenes según origen. | Verificado en código; no equivale a microservicios. |

## Pendiente para declarar completo el TPO

| Requisito | Evidencia actual y brecha | Dependencia/acción |
| --- | --- | --- |
| Eventos reales entre módulos | `LoggingProjectEventPublisher` solo escribe en logs; no hay publicador real en Azure ni consumidores, idempotencia o DLQ. Event Grid está aprovisionado sin suscripciones. | Acordar contratos con M2/M6/M7 y Core. Implementar publicación/consumo, pruebas de duplicados/fallos y observabilidad. No tomar nombres propuestos como acuerdos. |
| Evidencia y materiales de OT | Existen entidades/repositories, pero no endpoints para cargar evidencia/materiales. `OrdenTrabajoService.completar` no exige foto; la demo pudo completar una OT sin ella. | Back/Front/DevOps: diseñar flujo de carga, storage real y validación; migración Flyway si se modifica esquema. |
| Planificación integral de obra | El API de proyectos expone alta/edición/envío/aprobación/rechazo, sin endpoints de etapas, hitos, suspensiones, reanudación, ampliaciones justificadas ni cierre formal. | Back/Front: implementar reglas del ciclo administrativo y controles de cierre. |
| Reglas operativas completas | El código valida estados y exige cuadrilla al iniciar, pero no consta verificación de solapamiento de cuadrillas ni de proyecto aprobado antes de iniciar una OT vinculada. | Back: pruebas negativas y reglas transaccionales; Front: mensajes coherentes. |
| Corte de calle con Tránsito | La solicitud local persiste, pero autorización/rechazo M7 no existe como integración real. | Contrato y sistema M7; luego consumo de respuesta y bloqueo temporal de ejecución. |
| Pruebas de aceptación finales | QA-01 a QA-14 pasó en el alcance existente; no hay prueba end-to-end de los requisitos ausentes. | Repetir en Azure Test al completar los flujos y registrar evidencia de eventos, evidencia fotográfica y reglas. |

## Decisión de publicación

La aplicación actualmente desplegada es **candidata para una demostración acotada** del flujo proyecto → aprobación → orden → ejecución → inspección. No debe presentarse como TPO integral terminado. El cambio de cobertura agrega pruebas y controles de CI, no una funcionalidad nueva; por sí solo no justifica un redespliegue costoso de Azure. Antes de etiquetar una release como final, cerrar las brechas anteriores o acordar explícitamente con la cátedra qué corresponde a la entrega actual.
