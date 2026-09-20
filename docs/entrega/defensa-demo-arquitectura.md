# Defensa, demo y arquitectura de órdenes de trabajo

## Objetivo

Este documento convierte los criterios recibidos el 2026-09-15 en tareas comprobables. Fue actualizado para la release `v0.2.0` y distingue lo implementado de aquello que todavía requiere desarrollo o confirmación externa.

## Estado real frente a los criterios

| Criterio | Estado | Evidencia o pendiente |
| --- | --- | --- |
| Cada integrante defiende lo que hizo y su criterio | Preparado | Se define abajo un bloque de defensa por rol. Cada persona debe explicar decisiones propias y mostrar evidencia. |
| Demo de un caso de uso | Verificado | La demo de creación manual y ciclo completo se ejecutó correctamente con `scripts/demo-orden-trabajo.ps1` en `development`. |
| Patrón de diseño aplicado en Back | Cumplido | La creación de órdenes aplica `WorkOrderCreationStrategy` y resuelve las variantes manual y por proyecto. Back debe mostrar las clases y explicar el criterio. |
| MVC | Cumplido en Back | Hay Controller, Service, Repository, Mapper, DTO y Model. La petición entra por Controller, la regla se ejecuta en Service y la persistencia se delega al Repository. |
| Aplicación bien separada | Parcial | Back está separado por capas. Front concentra demasiado código en `App.tsx` y debe dividir vistas, componentes, hooks y servicios. |
| “No aplicación monolítica” | Pendiente de aclaración | Back se despliega como un único servicio Spring Boot: es un monolito modular, no microservicios. La cátedra debe confirmar cuál de las dos interpretaciones exige. |
| Enganchar órdenes de trabajo | Parcial | Manual, proyecto y corte de calle están cubiertos. Los consumidores M6/M7 siguen pendientes de contratos confirmados. |

## Qué muestra el diagrama recibido

El diagrama plantea cinco entradas hacia una orden pendiente:

1. Desde un proyecto: seleccionar un proyecto y crear una orden asociada.
2. Desde M6: recibir un evento ambiental, evaluar si requiere intervención de Obras y crear la orden solo cuando corresponda.
3. Desde M7: recibir un incidente de tránsito, evaluarlo y crear la orden cuando requiera intervención.
4. Desde carga manual: un usuario crea directamente la orden.
5. Desde un corte de calle: asociar una orden existente o crear una preliminar y luego vincularla.

### Cobertura actual

| Entrada | Release `v0.1.0` | Próximo trabajo |
| --- | --- | --- |
| Proyecto | Implementada en `v0.2.0` | `origin=PROYECTO` exige un `projectId` válido; Back persiste la relación y Front permite seleccionarla. |
| M6 | No implementada | Esperar contratos confirmados; luego implementar consumidor idempotente y estrategia de origen. |
| M7 | No implementada | Esperar contratos confirmados; luego implementar consumidor idempotente y estrategia de origen. |
| Manual | Implementada | Usarla como demo estable. |
| Corte de calle | Parcialmente implementada | El corte referencia una orden existente; falta validar el recorrido exacto del diagrama en la interfaz. |

Los nombres `infrastructureRepairRequested`, `containerDamaged`, `treeRiskDetected` y `trafficIncidentRegistered` son información recibida. Mientras no exista confirmación bilateral, no deben presentarse como contratos definitivos ni codificarse como si lo fueran.

## Patrón aplicado en Back: Strategy

La creación de una orden cambia según el origen. Strategy permite encapsular cada variante sin llenar un único servicio de condicionales.

```text
WorkOrderController
        |
        v
WorkOrderCreationService
        |
        v
WorkOrderCreationStrategyResolver
        |
        +-- ManualWorkOrderCreationStrategy
        +-- ProjectWorkOrderCreationStrategy
        +-- M6WorkOrderCreationStrategy   (solo con contrato confirmado)
        +-- M7WorkOrderCreationStrategy   (solo con contrato confirmado)
```

El Controller continúa recibiendo HTTP; el Service coordina; la Strategy decide cómo validar y construir la orden; el Repository persiste. Esto mantiene MVC y permite agregar orígenes sin modificar todas las variantes existentes.

### Evidencia que debe defender Back

1. Mostrar la interfaz `WorkOrderCreationStrategy` y el resolvedor por origen.
2. Comparar `ManualWorkOrderCreationStrategy` con `ProjectWorkOrderCreationStrategy`.
3. Explicar cómo `projectId` se valida y persiste sin romper órdenes manuales anteriores.
4. Mostrar Flyway V3/V4 y las pruebas por estrategia y endpoint.
5. Explicar por qué agregar otro origen no obliga a llenar el Service de condicionales.

No corresponde crear todavía las estrategias M6/M7 con payloads inventados. Pueden definirse los puntos de extensión, pero los adaptadores concretos dependen de contratos confirmados.

## Evidencia que debe defender Front

1. Mostrar la selección de proyecto y el envío de `projectId` por `/api/...`.
2. Mostrar el proyecto relacionado en el detalle de la orden.
3. Explicar la separación existente y reconocer como mejora pendiente la división adicional de `App.tsx`; no duplicar reglas de negocio del backend.
4. Mantener rutas relativas `/api/...`; Azure resuelve el destino mediante el proxy del frontend.
5. Agregar pruebas del flujo de creación y de los estados de carga y error.

## Demo recomendada: ciclo manual de una orden

Se elige este caso porque está implementado y no depende de contratos externos. La demo prueba Front/Back, API, reglas de estado y PostgreSQL.

### Relato funcional

“Personal de Obras detecta un bache y crea una orden manual. El jefe la programa, la cuadrilla inicia y completa el trabajo, y el inspector valida el resultado.”

### Estados demostrados

```text
PENDIENTE -> PROGRAMADA -> EN_EJECUCION -> COMPLETADA -> VALIDADA
```

### Ejecución técnica de respaldo

Con PostgreSQL de `development` encendido, ejecutar desde la raíz del repositorio:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\demo-orden-trabajo.ps1
```

El script consulta `/api/health`, crea una orden, la programa, inicia, completa y valida. Imprime el identificador y cada estado. La orden queda como evidencia en la base de desarrollo; no debe ejecutarse repetidamente sin necesidad.

Verificación del 2026-09-15: `/api/health` informó aplicación disponible y PostgreSQL activo. La orden de evidencia `id=1` recorrió `PENDIENTE`, `PROGRAMADA`, `EN_EJECUCION`, `COMPLETADA` y `VALIDADA` sin errores.

### Guion oral de la demo

1. Mostrar el frontend de `development` y aclarar que `/api` pasa por el proxy hacia Back.
2. Crear la orden manual y señalar el estado `PENDIENTE`.
3. Programarla y explicar que el backend controla la transición a `PROGRAMADA`.
4. Iniciarla y completarla como cuadrilla.
5. Validarla como inspector y comprobar `VALIDADA`.
6. Mostrar, si se necesita evidencia técnica, la salida del script y el health con `database: up`.

## Qué defiende cada rol

### DevOps

- GitFlow: `feature/*` hacia `develop`; una `release/vX.Y.Z` promociona el mismo artefacto a `main` y `test`.
- CI: pruebas y construcción antes del merge.
- Docker: Front y Back viajan como imágenes identificadas por SHA.
- Terraform: infraestructura reproducible y revisada mediante `plan` antes de `apply`.
- Azure: Container Apps, PostgreSQL, Container Registry y Event Grid.
- Seguridad y operación: secretos fuera de Git, despliegue autorizado por DevOps, health checks y apagado de PostgreSQL cuando no se usa.
- Criterio propio: promover exactamente la imagen validada evita diferencias entre ambientes y reduce errores manuales.

### Back

- Separación MVC y responsabilidad de Controller, Service, Repository, Mapper y Model.
- Reglas de transición de estados y persistencia PostgreSQL con Flyway.
- Strategy para los distintos orígenes de una orden.
- Criterio propio: las reglas del dominio viven en Back y no se duplican en Front.

### Front

- Consumo mediante rutas relativas `/api` y proxy de Azure.
- Componentes, vistas, hooks, servicios y manejo de estados de interfaz.
- Criterio propio: Front representa el proceso, pero Back decide si una transición es válida.

## Criterio de aceptación antes de presentar

- La cátedra aclaró si exige microservicios o acepta monolito modular.
- Back puede explicar Strategy con pruebas.
- La orden se asocia a un proyecto de punta a punta.
- Front puede demostrar el flujo y explicar su separación actual sin ocultar pendientes.
- PostgreSQL de `test` está encendido solo durante la ventana acordada de pruebas y demo.
- Health informa aplicación y base disponibles.
- Cada integrante ensayó su parte y puede explicar una decisión, no solo enumerar herramientas.
