# Integración con Core Municipal — Módulo 9

## Responsabilidad acordada

Core es responsable de las convenciones comunes de integración: formato de eventos, nombres técnicos, envelope, versionado, correlación y convenciones compartidas.

Obras debe informar a Core cada incorporación, eliminación o modificación de eventos. Core no se considera consumidor funcional de todos los eventos de negocio, salvo que una integración específica lo requiera.

## Contrato común

**Estado:** `CORE_PENDING`.

El contrato común debe permitir, como mínimo:

- identificar de forma única el evento y su tipo;
- registrar fecha/hora y módulo de origen;
- transportar los datos funcionales;
- correlacionar hechos del mismo proceso;
- identificar la versión del contrato.

Los siguientes nombres son solo candidatos y no deben fijarse: `eventId`, `eventType`, `occurredAt`, `source`, `version`, `correlationId` y `data`.

## Definiciones técnicas recibidas del PO

**Estado:** `RECEIVED`, pendiente de confirmación con M9.

La matriz enviada por el PO menciona UUID para identificadores, `camelCase`, fechas ISO 8601, versión del contrato y esquemas compartidos mediante JSON Schema. También indica que Obras informa al catálogo de Core todos los eventos incorporados, modificados o retirados.

Estas definiciones son compatibles con el rol técnico de Core, pero no se consideran aún convenciones `CONFIRMED`: falta validar nombres exactos, zona horaria, estructura del envelope y versión con M9. La notificación al catálogo no convierte a Core en consumidor funcional del evento.

## Acuerdos vigentes

- Identificadores técnicos en inglés.
- Atributos, funciones y eventos en `camelCase`.
- La UI permanece en español.
- Core mantiene las convenciones y el catálogo común.
- Obras conserva la propiedad de sus datos y reglas de negocio.

## Pendientes

- Nombres definitivos, tipos y obligatoriedad del envelope.
- Formato y zona horaria de fechas.
- Convención de versiones compatibles e incompatibles.
- Semántica de correlación y causalidad.
- Registro de productores, consumidores y canales.
- Alcance técnico de Core como hub frente a su no participación como consumidor funcional.
- Estrategia común de reintentos, idempotencia, auditoría y DLQ.

## Evidencia operativa M6 → M3 → M6 — 2026-11-05

**Estado de transporte y prueba funcional M6–M3–Core:** `CONFIRMED`.

Esta evidencia sustituye únicamente las pendientes de disponibilidad de infraestructura. No resuelve por sí sola las definiciones contractuales históricas listadas arriba.

- Core informó `infrastructureRepairRequested` con `eventId=a53fc8ee-5200-4949-b333-480f21be7e5d`, un mensaje pendiente en `q.obras` y ausencia de consumidores y de la conexión `module_obras`.
- Se comprobó que Azure Test había escalado el backend a cero porque Terraform declaraba `min_replicas=0`. Al despertar la aplicación, M3 abrió la conexión AMQPS y procesó el evento con `correlationId=84cd1a26-c21b-4d57-a292-d4fb7daff878`.
- El PR `#54` cambió la regla a `min_replicas = application_messaging_enabled ? 1 : 0`, pasó todos los controles, se fusionó y se desplegó con el tag `v1.0-testing.2` mediante el workflow `42087566180`.
- La verificación posterior confirmó `minReplicas=1`, `maxReplicas=1`, una réplica activa, mensajería habilitada, health `ok`, PostgreSQL `up` y `module_obras` conectado al vhost `core`.
- M3 creó, programó, inició y completó la orden interna `id=5` con `sourceRequestId=6fdddb92-78fe-4220-a9c2-0c5395623f6a`.
- M3 publicó `workOrderScheduled` con `eventId=8d109cc9-1802-4b30-89ea-0dd9df8b1843` y `workOrderCompleted` con `eventId=916449bf-9cfb-4449-ae74-65b9825f7693`; ambos conservaron la correlación original y registraron `result=published`.
- Las cuentas técnicas usadas para respetar la separación de roles quedaron únicamente en secretos protegidos de Azure Test y GitHub Environment `test`; no se almacenaron contraseñas en Git.
- A las 16:10 de Argentina, M6 confirmó que el pedido `6fdddb92-78fe-4220-a9c2-0c5395623f6a` quedó `Cerrado` y que las métricas de Core mostraban recibidos `workOrderScheduled` y `workOrderCompleted`.
- A las 16:14 de Argentina, Core confirmó en sus registros de AWS que `infrastructureRepairRequested`, `workOrderScheduled` y `workOrderCompleted` quedaron `ROUTED` y compartieron el mismo `correlationId`.
- Core verificó además `q.obras` y `q.ambiente` sin mensajes pendientes y la DLQ vacía. Con la confirmación funcional de M6, la prueba M6 → M3 → M6 queda cerrada satisfactoriamente.

## Contexto

La consigna original describe a Core como hub técnico de eventos. La instrucción vigente aclara que esa función no autoriza a tratarlo como consumidor funcional de todos los hechos. La separación exacta entre enrutamiento técnico y consumo de negocio queda pendiente de confirmación con M9.
