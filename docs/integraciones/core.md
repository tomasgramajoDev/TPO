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

## Contexto

La consigna original describe a Core como hub técnico de eventos. La instrucción vigente aclara que esa función no autoriza a tratarlo como consumidor funcional de todos los hechos. La separación exacta entre enrutamiento técnico y consumo de negocio queda pendiente de confirmación con M9.
