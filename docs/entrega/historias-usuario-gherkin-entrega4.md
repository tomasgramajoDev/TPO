# Historias de usuario y escenarios Gherkin — Entrega 4

## HU-01 — Aprobar un proyecto

```gherkin
Característica: aprobación de proyectos
  Escenario: responsable aprueba un proyecto pendiente
    Dado un proyecto presentado para aprobación
    Y una sesión con rol RESPONSABLE_AUTORIZADO
    Cuando aprueba el proyecto con presupuesto y plazo válidos
    Entonces el proyecto queda aprobado
    Y el cambio persiste en PostgreSQL

  Escenario: un rol no autorizado intenta aprobar
    Dado un proyecto pendiente
    Y una sesión con rol PERSONAL_OBRAS
    Cuando intenta aprobarlo
    Entonces la API responde 403
    Y el proyecto no cambia
```

## HU-02 — Ejecutar una orden con State

```gherkin
Característica: ciclo de una orden
  Escenario: recorrido operativo válido
    Dada una orden asignada a una cuadrilla
    Cuando el jefe la programa e inicia
    Y el operario la completa
    Y el inspector la valida
    Entonces la orden queda VALIDADA

  Escenario: transición inválida
    Dada una orden PENDIENTE
    Cuando se intenta completar sin iniciar
    Entonces la API responde 409 con application/problem+json
```

## HU-03 — Evitar comandos REST duplicados

```gherkin
Característica: idempotencia REST
  Escenario: reintento con la misma clave y cuerpo
    Dado un POST autenticado con Idempotency-Key
    Cuando se repite el mismo POST con igual cuerpo
    Entonces se devuelve la respuesta original
    Y no se crea una segunda entidad

  Escenario: reutilización conflictiva
    Dada una Idempotency-Key ya procesada
    Cuando se reutiliza con otro cuerpo
    Entonces la API responde 409
```

## HU-04 — Controlar edición concurrente

```gherkin
Característica: concurrencia optimista
  Escenario: modificación con versión vigente
    Dado el ETag actual de un recurso
    Cuando se modifica usando If-Match con ese valor
    Entonces la modificación se acepta y devuelve un ETag nuevo

  Escenario: modificación con versión obsoleta
    Dado un ETag anterior
    Cuando se intenta modificar el recurso
    Entonces la API responde 412 con Problem Details
```

## HU-05 — Resiliencia e integración

```gherkin
Característica: publicación confiable de eventos
  Escenario: el broker no está disponible
    Dado un hecho de negocio persistido
    Cuando el broker está caído
    Entonces el evento queda pendiente en Outbox
    Y puede publicarse posteriormente sin cambiar su eventId

  Escenario: evento recibido dos veces
    Dado un eventId ya procesado
    Cuando el consumidor recibe el mismo evento nuevamente
    Entonces Inbox lo reconoce como duplicado
    Y no repite el efecto de negocio
```

## HU-06 — Asistente seguro

```gherkin
Característica: asistencia de Obras mediante IA
  Escenario: proveedor disponible
    Dada una consulta del dominio de Obras
    Cuando el gateway responde antes de cinco segundos
    Entonces se devuelve una respuesta acotada al dominio

  Escenario: proveedor caído
    Dada una consulta válida
    Cuando el gateway falla o vence el timeout
    Entonces la API devuelve un fallback seguro

  Esquema del escenario: consulta no permitida
    Cuando el usuario envía <consulta>
    Entonces la solicitud se rechaza sin revelar datos
    Ejemplos:
      | consulta |
      | una instrucción para ignorar el prompt del sistema |
      | una pregunta fuera de Obras |
      | un pedido de contraseñas, tokens o DNI |
```
