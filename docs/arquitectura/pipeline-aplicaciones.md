# Pipeline de frontend y backend

## Estado

Repositorios y comandos base verificados el 2026-08-25. La validación CI puede prepararse, pero el despliegue integral continúa bloqueado por la falta de una API ejecutable en el backend, la integración con PostgreSQL y los permisos/configuración Azure de los repositorios.

El pipeline Terraform crea la plataforma. El pipeline de aplicación deberá construir y desplegar frontend y backend cuando cada repositorio entregue los siguientes datos:

- URL y visibilidad del repositorio;
- lenguaje y versión;
- comando de instalación;
- comando de pruebas;
- comando de build;
- ruta del `Dockerfile` y contexto Docker;
- puerto interno;
- endpoint de health check;
- variables públicas y secretos requeridos.

## Repositorios y comandos verificados

| Componente | Repositorio y rama predeterminada | Stack | Validación local verificada |
| --- | --- | --- | --- |
| Frontend | `NadineLewit/DesarrolloAppsII_Front`, `main` | React 19, TypeScript 6, Vite 8, Node 24, Nginx 1.29 | `npm ci`, `npm run lint`, `npm test` y `npm run build`: 2 archivos y 4 pruebas aprobadas; imagen Docker disponible. |
| Backend | `ignacionogue/DesarrolloDeAplicacionesIIBack`, `master` | Spring Boot 4.1.0, Java 17, Maven Wrapper | `./mvnw test`: 1 prueba aprobada y build correcto. No contiene todavía API web, persistencia PostgreSQL, health check ni Dockerfile en la versión recibida. |

El usuario autenticado en GitHub tiene permiso `WRITE` sobre el backend y solo `READ` sobre el frontend. El CI del frontend deberá ingresar mediante un pull request desde un fork o después de que el propietario otorgue permisos de escritura.

## Implementación preparada

- Backend: pull request `ignacionogue/DesarrolloDeAplicacionesIIBack#1`, con Maven `clean verify`, construcción de imagen Docker y ejecución no privilegiada. GitHub Actions completó correctamente pruebas, empaquetado y build del contenedor.
- Frontend: pull request `NadineLewit/DesarrolloAppsII_Front#1`, con `npm ci`, lint, pruebas, build y construcción de imagen. La ejecución equivalente en el fork completó correctamente todas las etapas; el repositorio propietario todavía debe aceptar el pull request.
- Ningún workflow publica imágenes ni despliega todavía; esta separación evita consumir Azure o exponer credenciales antes de configurar OIDC, environments y recursos de aplicación.

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

- Crear y proteger las ramas `develop` y `release/*`; actualmente los repositorios solo publican `main` en frontend y `master` en backend.
- Revisar y aceptar el pull request para incorporar el workflow del frontend.
- Implementar en el backend una API web, health check y configuración PostgreSQL antes de desplegarlo con ingress.
- Servicio PostgreSQL de Azure y estrategia de migraciones.
- Servicio de mensajería.
- Gestión de secretos de las aplicaciones.
- Health checks y criterios de rollback.
