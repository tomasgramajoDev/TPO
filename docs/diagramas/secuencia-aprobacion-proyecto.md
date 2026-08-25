# Secuencia propuesta — aprobación de un proyecto

## Alcance y certeza

La secuencia muestra un diseño técnico posible con portal React, backend Spring Boot, PostgreSQL y un broker de Azure todavía no elegido. React y Spring Boot provienen de la tarjeta DevOps recibida; deben confirmarse contra los repositorios reales. Los eventos hacia M1 siguen en estado `RECEIVED`.

```mermaid
sequenceDiagram
    actor Personal as Personal de Obras
    actor Responsable as Responsable autorizado
    participant Portal as Portal React
    participant API as Backend Spring Boot
    participant DB as PostgreSQL
    participant Broker as Message Broker
    participant M1 as M1 Expedientes

    Personal->>Portal: Completar y confirmar nuevo proyecto
    Portal->>API: POST /api/projects
    API->>DB: INSERT project (status = BORRADOR)
    DB-->>API: projectId
    API-->>Portal: HTTP 201 Created

    Personal->>Portal: Solicitar aprobación
    Portal->>API: PUT /api/projects/{id}/submit
    API->>DB: UPDATE status = PENDIENTE_APROBACION
    API->>Broker: publicWorksProjectSubmittedForApproval
    API-->>Portal: HTTP 200

    Responsable->>Portal: Aprobar proyecto
    Portal->>API: PUT /api/projects/{id}/approve
    API->>DB: TX: status = APROBADO + registro outbox
    DB-->>API: COMMIT
    API->>Broker: publicWorksProjectApproved
    Broker->>M1: Entregar publicWorksProjectApproved
    M1-->>Broker: ACK
    API-->>Portal: HTTP 200 (Aprobado)
```

La publicación confiable mediante outbox, reintentos y DLQ es una propuesta DevOps. Service Bus frente a Event Grid, y las convenciones definitivas del evento, siguen pendientes.
