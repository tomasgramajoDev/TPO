# Obras Públicas - Módulo 3

Repositorio de documentación, infraestructura como código y automatización DevOps del módulo de Obras Públicas, Infraestructura y Mantenimiento Urbano.

## Estado actual

- Documentación funcional e integraciones: organizada en [`docs/`](docs/README.md).
- Decisión de cloud: Azure, región `Chile Central` por restricción de la suscripción Azure for Students.
- Infraestructura: Terraform con ambientes `development` y `test`.
- CI/CD: GitHub Actions con autorización de DevOps y autenticación OIDC.
- Bootstrap Azure desplegado: estado remoto, Container Registry, identidad OIDC, permisos y resource groups.
- Plataforma `development` desplegada: Log Analytics y Azure Container Apps Environment en `Chile Central`.
- Plataforma `test`: pendiente de una release aprobada y de la autorización DevOps.
- Aplicaciones frontend/backend: sus repositorios y stack continúan pendientes.

## Accesos rápidos

- [Decisión de arquitectura](docs/arquitectura/adr-001-cloud-y-cicd.md)
- [Operación DevOps](docs/arquitectura/operacion-devops.md)
- [Pipeline de aplicaciones](docs/arquitectura/pipeline-aplicaciones.md)
- [Infraestructura y puesta en marcha](infra/README.md)
- [Terraform CI](.github/workflows/terraform-ci.yml)
- [Despliegue de development](.github/workflows/deploy-development.yml)
- [Despliegue de test](.github/workflows/deploy-test.yml)

## Próxima activación

1. Conectar los repositorios o artefactos de frontend y backend cuando el equipo defina sus stacks.
2. Incorporar al pipeline la construcción y publicación de imágenes en Azure Container Registry.
3. Crear una release aprobada cuando exista una versión candidata para desplegar en `test`.

El bootstrap y la plataforma de `development` ya están activos. `test` no se crea hasta que DevOps apruebe su plan y su despliegue.
