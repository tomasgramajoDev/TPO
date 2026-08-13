# Obras Públicas - Módulo 3

Repositorio de documentación, infraestructura como código y automatización DevOps del módulo de Obras Públicas, Infraestructura y Mantenimiento Urbano.

## Estado actual

- Documentación funcional e integraciones: organizada en [`docs/`](docs/README.md).
- Decisión de cloud: Azure, región `Chile Central` por restricción de la suscripción Azure for Students.
- Infraestructura: Terraform con ambientes `development` y `test`.
- CI/CD: GitHub Actions con autorización de DevOps y autenticación OIDC.
- Bootstrap Azure desplegado: estado remoto, Container Registry, identidad OIDC, permisos y resource groups.
- Plataformas `development` y `test`: pendientes de aprobación y ejecución desde GitHub Actions.
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

1. Revisar y fusionar el pull request DevOps en `main`.
2. Aprobar el plan de `development` desde el environment protegido de GitHub.
3. Aprobar el `apply` del mismo plan.
4. Conectar los repositorios o artefactos de frontend y backend cuando el equipo defina sus stacks.

El bootstrap ya genera el costo del Azure Container Registry Basic. Los ambientes no se crean hasta que DevOps apruebe sus despliegues.
