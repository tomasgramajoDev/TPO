# Guía DevOps — GitFlow, ambientes y releases

## Decisión vigente

Las aplicaciones frontend y backend seguirán este flujo:

```text
feature/* → develop → release/vX.Y.Z → main
                ↓              ↓
       Azure development   Azure test
```

Una rama no es un ambiente. Las ramas organizan estados del código en GitHub; los ambientes ejecutan versiones en Azure.

## Mapa de ramas

| Rama | Nace desde | Recibe | Resultado |
| --- | --- | --- | --- |
| `feature/*` | `develop` | Commits de una historia o cambio pequeño | Pull request hacia `develop` |
| `develop` | Permanente | Features aprobadas por revisión y CI | Digest desplegable en `development` |
| `release/vX.Y.Z` | `develop` al cerrar el sprint | Solo correcciones de estabilización | Digest candidato desplegable en `test` |
| `main` | Permanente | Releases aprobadas | Tag `vX.Y.Z` y registro estable |
| `hotfix/*` | `main` | Corrección urgente de producción | No se usa hasta que exista producción |

## Qué debe automatizar el pipeline de aplicaciones

### Pull request hacia `develop`

1. Instalar dependencias usando el lockfile.
2. Ejecutar formato, lint, pruebas y build.
3. Construir la imagen Docker sin publicarla.
4. Bloquear el merge si falla un control obligatorio.

### Merge a `develop`

1. Repetir las validaciones sobre el commit definitivo.
2. Construir y etiquetar la imagen con el SHA.
3. Publicarla en Azure Container Registry.
4. Resolver y registrar el digest inmutable.
5. Solicitar autorización de DevOps mediante el environment `development` de GitHub.
6. Desplegar el digest en Azure `development`.
7. Ejecutar smoke tests y registrar la evidencia.

### Cierre del sprint

1. Confirmar que las historias incluidas cumplen la Definition of Done.
2. Crear `release/vX.Y.Z` desde el commit probado de `develop`.
3. Reutilizar el digest ya probado si el commit no cambió.
4. Solicitar autorización de DevOps mediante el environment `test` de GitHub.
5. Desplegar el digest en Azure `test`.
6. Ejecutar smoke tests.
7. Habilitar la validación funcional del Product Owner.

### Correcciones durante la validación

Los defectos encontrados en `test` se corrigen en `release/vX.Y.Z`. Cada cambio genera un nuevo SHA y un nuevo digest, que vuelve a pasar las validaciones y la autorización DevOps. Las correcciones deben fusionarse también en `develop` para evitar que el error reaparezca.

### Cierre de la release

1. Obtener la aprobación funcional del Product Owner.
2. Confirmar logs, health checks, configuración y rollback.
3. Fusionar la release en `main`.
4. Crear el tag `vX.Y.Z` y las notas de versión.
5. Fusionar la release en `develop`.
6. Conservar el digest aprobado como referencia auditable.

No existe despliegue a producción en el incremento actual.

## Autoridad de DevOps

El pipeline puede iniciarse automáticamente, pero el despliegue no continúa hasta que DevOps revisa y autoriza el environment correspondiente. El Product Owner aprueba la funcionalidad; DevOps aprueba la operación. Ninguna aprobación reemplaza a la otra.

Antes de autorizar, DevOps verifica:

- rama, commit SHA, tag y digest;
- resultado de CI y construcción Docker;
- plan o cambios de infraestructura, si existen;
- variables y secretos requeridos;
- health check y smoke tests;
- migraciones y riesgos de datos;
- observabilidad y logs;
- estrategia de rollback.

## Diferencia con los workflows Terraform actuales

Los workflows presentes en este repositorio despliegan la plataforma Azure y usan `main` o una release publicada como disparadores. La publicación de imágenes se realiza por separado con `publish-development-images.yml`; Terraform promueve luego las referencias inmutables aprobadas. Los repositorios, stacks, Dockerfiles, puertos y health checks ya fueron recibidos y verificados.

No se deben cambiar los disparadores de Terraform para simular el pipeline de aplicación: son responsabilidades distintas.

## Convención inicial de nombres

- Feature: `feature/descripcion-corta`
- Corrección normal: `fix/descripcion-corta`
- Release: `release/v0.1.0`
- Hotfix futuro: `hotfix/v1.0.1`
- Tags: `v0.1.0`, `v0.2.0`, `v1.0.0`

## Checklist de la release `v0.1.0` al 2026-09-15

- [x] Todas las historias incluidas están fusionadas en `develop`.
- [x] CI, build y Docker están aprobados.
- [x] La versión integrada funciona en `development`.
- [x] Se eligió el número de versión.
- [x] Se creó `release/v0.1.0` desde el commit correcto.
- [x] Se identificaron y promovieron las imágenes inmutables.
- [x] DevOps autorizó el despliegue a `test`.
- [x] Los smoke tests técnicos de `test` fueron exitosos.
- [ ] El Product Owner aprobó funcionalmente el sprint.
- [x] La release se fusionó en `main`; `develop` conserva los commits que originaron la release.
- [x] Se creó el tag y se guardaron las notas de versión.
- [x] El rollback técnico consiste en volver a fijar en Terraform el SHA anterior y repetir plan, aprobación y `apply`.

## Próximo control pendiente

El Product Owner debe validar `v0.1.0` en `test` con datos representativos. Los eventos todavía no tienen suscripciones porque los consumidores y contratos externos no fueron confirmados; no deben crearse por suposición.
