# Alcance general

## Objetivo

Gestionar de forma integral proyectos de obra pública, órdenes de trabajo e intervenciones sobre calles, veredas, luminarias, edificios, desagües y espacios públicos.

## Fase actual

El usuario autorizó el inicio de la fase de desarrollo DevOps el 2026-08-11. Están incluidos el diseño cloud, Terraform, automatización y pipelines para los ambientes de desarrollo y prueba. El frontend, backend y demás código de aplicación requieren una solicitud específica y no forman parte del primer incremento DevOps.

## Componente de interfaz

- Único frontend: portal web responsive.
- Interfaz de usuario: español.
- No habrá una aplicación móvil independiente.
- El ciudadano común no ingresa directamente al módulo; reporta problemas mediante Atención Ciudadana.

## Capacidades funcionales incluidas

- Proyectos de obra pública, presupuestos, etapas e hitos.
- Avance físico y presupuestario.
- Órdenes de trabajo e intervenciones de infraestructura.
- Cuadrillas, maquinaria, materiales y tiempos de trabajo.
- Evidencias, certificaciones e inspección.
- Ampliaciones de plazo y presupuesto.
- Solicitudes de cortes de calle.
- Validación y reapertura de trabajos.
- Consulta, auditoría e indicadores de obras finalizadas.

## Integraciones de negocio

| Módulo | Obras recibe | Obras publica |
| --- | --- | --- |
| Atención Ciudadana — M2 | Derivaciones y escalamiento de reclamos de infraestructura. | Estados relevantes de las órdenes originadas por reclamos. |
| Ambiente, Higiene y Servicios Urbanos — M6 | Solicitudes de reparación, daños de contenedores y riesgos de arbolado que requieren Obras. | Resultados de las órdenes relacionadas. |
| Tránsito — M7 | Incidentes viales y autorización o rechazo de cortes. | Solicitudes de cortes requeridos por obras u órdenes. |
| Ciudadanos y Expedientes Digitales — M1 | Resoluciones administrativas relacionadas con obras. | Eventos del ciclo de la obra que ese módulo confirme necesitar. |
| Core Municipal — M9 | Convenciones técnicas comunes. | Catálogo y cambios de contratos; no se presume consumo funcional de todos los eventos. |

## Convenciones de documentación

- Texto funcional y UI en español.
- Identificadores técnicos en inglés.
- Atributos, funciones y eventos en `camelCase`.
- Endpoints, entidades y errores técnicos en inglés; su convención exacta de casing queda pendiente de confirmación.
- Las convenciones definitivas de envelope, versión y correlación pertenecen a Core y no se fijan como definitivas aquí.

## Fuera del primer incremento DevOps

- Implementación del frontend y backend.
- Diseño definitivo de APIs o topics/colas.
- Aprovisionamiento y configuración de la base de datos, mensajería y autenticación. PostgreSQL ya está elegido como motor, pero todavía deben definirse el servicio de Azure, la operación y las migraciones.
- Ambiente de producción hasta acordar su flujo de promoción.
- Aplicación móvil independiente.
- Acceso directo del ciudadano a Obras Públicas.
- Modificación directa de información perteneciente a otros módulos.

La consigna académica exige frontend, backend, base de datos propia, integración, autenticación, pruebas y despliegue. La plataforma DevOps se prepara de forma incremental para alojar esos componentes cuando el equipo defina e implemente el stack de aplicación.
