# Pipeline de frontend y backend

## Estado

Frontend, backend y PostgreSQL están desplegados y verificados en Azure `development` desde el 2026-08-25. El backend expone `/api/health`, consulta PostgreSQL con `SELECT 1` y recibe sus credenciales mediante un secreto de Container Apps. El frontend expone `/health` y enruta `/api/*` al backend por HTTPS.

Este estado valida la plataforma, el pipeline y la conectividad técnica. No implica que estén implementados el esquema, las migraciones ni los endpoints funcionales del dominio de Obras Públicas.

## Repositorios y comandos verificados

| Componente | Repositorio y rama predeterminada | Stack | Validación local verificada |
| --- | --- | --- | --- |
| Frontend | `tomasgramajoDev/DesarrolloAppsII_Front`, `develop` para el despliegue; PR abierto hacia `NadineLewit/DesarrolloAppsII_Front` | React 19, TypeScript 6, Vite 8, Node 24, Nginx 1.29 | `npm ci`, lint, 4 pruebas, build e imagen Docker aprobados. `/health` y proxy HTTPS `/api/*` verificados. |
| Backend | `ignacionogue/DesarrolloDeAplicacionesIIBack`, `develop` | Spring Boot 4.1.0, Java 17, Maven Wrapper, Spring JDBC y PostgreSQL | 2 pruebas, empaquetado e imagen Docker aprobados. `/api/health` y conexión PostgreSQL verificados. |

El usuario autenticado en GitHub tiene permiso `WRITE` sobre el backend y solo `READ` sobre el frontend. El CI del frontend deberá ingresar mediante un pull request desde un fork o después de que el propietario otorgue permisos de escritura.

## Implementación desplegada

- Backend: el pull request `ignacionogue/DesarrolloDeAplicacionesIIBack#1` fue fusionado en `develop`. La imagen desplegada es `obras-publicas-backend:662ad1efc318377e93d73399ff94099153941a31`.
- Frontend: la imagen desplegada es `obras-publicas-frontend:c5161311424f8029c126310ebd54e0038f771624`. El pull request `NadineLewit/DesarrolloAppsII_Front#1` sigue pendiente; mientras tanto, el pipeline usa la rama `develop` del fork autorizado.
- Publicación: `publish-development-images.yml` valida ambos repositorios, publica imágenes con etiquetas SHA en ACR y conserva su digest.
- Despliegue: Terraform administra ambos Container Apps, ingress, probes, identidad para ACR, variables y secretos. DevOps aprueba por separado el plan y el `apply`.
- Verificación: frontend HTTP `200`, `/health` correcto, backend `/api/health` con `database: up` tanto directo como a través del proxy del frontend.

## Flujo acordado — GitFlow simplificado

Las ramas y los ambientes son conceptos distintos. La rama indica el estado del código en GitHub; el ambiente indica dónde se ejecuta una versión en Azure.

| Rama | Propósito | Ambiente asociado |
| --- | --- | --- |
| `feature/*` | Desarrollo aislado de una historia o cambio. Nace desde `develop`. | Ninguno; se prueba localmente y en CI. |
| `develop` | Integración continua de las historias del sprint. | `development`, después de autorización DevOps. |
| `release/vX.Y.Z` | Estabilización de la versión candidata al cerrar el sprint. | `test`, después de autorización DevOps. |
| `main` | Historial de versiones aprobadas. Será la fuente de producción cuando ese ambiente exista. | Ninguno en el incremento actual. |
| `hotfix/*` | Corrección urgente de una versión productiva. Nace desde `main`. | No se usa hasta que exista producción. |

### Pull request de `feature/*` hacia `develop`

1. Instalar dependencias con versiones bloqueadas.
2. Ejecutar lint y pruebas.
3. Construir la aplicación.
4. Construir la imagen Docker sin publicarla.
5. Bloquear el merge si falla una validación obligatoria.

### Merge a `develop`

1. Repetir las validaciones.
2. Construir una imagen etiquetada con el SHA del commit.
3. Publicarla en Azure Container Registry.
4. Resolver y registrar su digest inmutable.
5. Esperar autorización de DevOps.
6. Desplegar ese digest en `development`.
7. Ejecutar un smoke test y registrar el resultado.

### Cierre de sprint y rama `release/vX.Y.Z`

1. Confirmar que las historias incluidas cumplen la Definition of Done en `develop`.
2. Crear `release/vX.Y.Z` desde el commit probado de `develop`.
3. Seleccionar el digest correspondiente; no reconstruir la imagen si el commit no cambió.
4. Esperar autorización de DevOps.
5. Promover ese digest a `test`.
6. Ejecutar smoke tests y registrar la versión desplegada.
7. Corregir en la rama de release únicamente defectos de estabilización. Cada corrección genera un nuevo digest verificable.
8. Incorporar las correcciones de la release nuevamente en `develop`.

### Aprobación y cierre de la release

1. El Product Owner valida funcionalmente el sprint en `test`.
2. DevOps confirma que la versión, la configuración, los logs y el rollback son operables.
3. Fusionar `release/vX.Y.Z` en `main` y crear el tag `vX.Y.Z`.
4. Fusionar también la release en `develop` para conservar todas las correcciones.
5. No desplegar en producción: ese ambiente todavía no forma parte del incremento actual.

### Hotfix futuro

Cuando exista producción, un incidente crítico se corregirá en `hotfix/*` creado desde `main`. La corrección aprobada deberá volver tanto a `main` como a `develop`. Hasta entonces, los defectos encontrados en `test` se corrigen en la rama de release.

## Responsabilidades

- Frontend/backend mantienen sus pruebas, build, `Dockerfile` y health check.
- DevOps mantiene Azure, Terraform, permisos, environments, workflows, observabilidad, promoción y rollback.
- El PO aprueba funcionalmente la release; esa aprobación no reemplaza la autorización operativa de DevOps.

## Decisiones pendientes

- Definir y proteger las ramas `release/*` y acordar la protección definitiva de `develop` en ambos repositorios.
- Revisar y aceptar el pull request del frontend en el repositorio propietario para dejar de depender del fork.
- Implementar el esquema, las migraciones y los endpoints funcionales del backend.
- Definir la estrategia de migraciones PostgreSQL y reemplazar la regla temporal de acceso desde servicios Azure por red privada antes de producción.
- Confirmar si Event Grid continúa siendo suficiente para `test`/producción cuando se cierren los contratos; si aparecen requisitos de orden estricto, transacciones o detección de duplicados, reevaluar Azure Service Bus.
- Criterios funcionales de smoke test y rollback, además de los health checks técnicos ya implementados.
