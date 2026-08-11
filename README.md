# Obras Públicas - Módulo 3

Repositorio de documentación, infraestructura como código y automatización DevOps del módulo de Obras Públicas, Infraestructura y Mantenimiento Urbano.

## Estado actual

- Documentación funcional e integraciones: organizada en [`docs/`](docs/README.md).
- Decisión de cloud: Azure, región `Brazil South`.
- Infraestructura: Terraform con ambientes `development` y `test`.
- CI/CD: GitHub Actions con autorización de DevOps y autenticación OIDC.
- Recursos Azure desplegados: ninguno todavía.
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

1. Elegir el repositorio GitHub definitivo.
2. Activar la suscripción Azure.
3. Ejecutar el bootstrap siguiendo [`infra/README.md`](infra/README.md).
4. Crear y proteger los environments de GitHub.
5. Ejecutar manualmente el despliegue de `development`.

Hasta completar esos pasos, el código puede validarse pero no modifica servicios externos ni genera costos.
