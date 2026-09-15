# Pipeline de frontend y backend

## Estado

La release `v0.1.0` quedó desplegada y verificada en Azure `development` y `test` el 2026-09-15. El backend expone `/api/health`, consulta PostgreSQL y recibe sus credenciales mediante un secreto de Container Apps. El frontend expone `/health` y enruta `/api/*` al backend por HTTPS.

Este estado valida la plataforma, los pipelines, Flyway, la conectividad y los endpoints de consulta con una base vacía. La aceptación funcional del Product Owner y los flujos con escritura de datos continúan pendientes.

## Repositorios y comandos verificados

| Componente | Repositorio y rama predeterminada | Stack | Validación local verificada |
| --- | --- | --- | --- |
| Frontend | `NadineLewit/DesarrolloAppsII_Front`; trabajo en `develop`, release `v0.1.0` integrada en `main` | React 19, TypeScript 6, Vite 8, Node 24, Nginx 1.29 | `npm ci`, lint, 4 pruebas, build e imagen Docker aprobados. `/health` y proxy HTTPS `/api/*` verificados en ambos ambientes. |
| Backend | `ignacionogue/DesarrolloDeAplicacionesIIBack`; trabajo en `develop`, release `v0.1.0` integrada en `main` | Spring Boot 4.1.0, Java 17, Maven Wrapper, JPA, Flyway y PostgreSQL | 13 pruebas, empaquetado e imagen Docker aprobados. `/api/health`, Flyway y endpoints de consulta verificados. |

La propietaria del frontend otorgó permiso y DevOps pudo integrar los PR `#4`, `#5` y `#6` mediante revisión. Se mantiene la regla de no trabajar ni hacer push directo sobre `develop` o `main`.

## Implementación desplegada

- Backend: el PR `#3` fue fusionado en `develop` y el PR de release `#4` fue fusionado en `main`. La imagen promovida es `obras-publicas-backend:b70379b077881a4b03ff4a4e5244d2f8195cf9a2`.
- Frontend: los PR `#4` y `#5` fueron fusionados en `develop`; el PR de release `#6` fue fusionado en `main`. La imagen promovida es `obras-publicas-frontend:9175534aa57e003caaebb7df2479f6e076c8e066`.
- Publicación: `publish-development-images.yml` valida ambos repositorios, publica imágenes con etiquetas SHA en ACR y conserva su digest.
- Despliegue: Terraform administra ambos ambientes, Container Apps, PostgreSQL 16, Event Grid, ingress, probes, identidad para ACR, variables y secretos. DevOps aprobó por separado cada plan y cada `apply`.
- Verificación: en `development` y `test` se obtuvo HTTP `200` en frontend, `/health`, backend `/api/health`, proxy `/api/health`, proyectos, órdenes, cuadrillas, recursos, cortes y tablero. El health informó `database: up`.
- Release: la infraestructura se etiquetó como `v0.1.0`; el workflow `Deploy test` promovió las mismas imágenes inmutables ya probadas en `development`.

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

- Definir y proteger las ramas `release/*`, `develop` y `main` en ambos repositorios.
- Definir la estrategia de migraciones PostgreSQL y reemplazar la regla temporal de acceso desde servicios Azure por red privada antes de producción.
- Confirmar contratos y consumidores antes de crear suscripciones de Event Grid; no hay suscripciones configuradas por inferencia.
- Confirmar si Event Grid continúa siendo suficiente para producción cuando se cierren los contratos; si aparecen requisitos de orden estricto, transacciones o detección de duplicados, reevaluar Azure Service Bus.
- Ejecutar con el Product Owner la aceptación funcional de `v0.1.0` usando datos representativos y validar también los flujos de escritura.
