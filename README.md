# Obras Públicas - Módulo 3

Repositorio de documentación, infraestructura como código y automatización DevOps del módulo de Obras Públicas, Infraestructura y Mantenimiento Urbano.

## Inicio local para Testing (G1)

Requisitos: Git y Docker Desktop con Docker Compose. Desde un clon limpio:

1. Copiar `.env.example` como `.env`.
2. Completar `DB_PASSWORD`, `JWT_SECRET` (mínimo 32 caracteres), `DEMO_PASSWORD` y `RABBITMQ_PASSWORD` con valores locales no reutilizados.
3. Ejecutar un único comando:

```powershell
docker compose up --build
```

El comando construye Front y Back desde los commits inmutables registrados en `compose.yaml`, inicia PostgreSQL y RabbitMQ y espera sus health checks. La candidata de la cuarta entrega fija Back `1f2606e216ca6d9c59507b110a8f0647eee6e8a2` y Front `d472da55fa5dca8f6c351a01805d35495f611486`. Si falta una variable obligatoria, Compose corta antes de crear recursos con un mensaje que identifica la variable. Las credenciales no se imprimen ni se almacenan en Git.

Accesos de verificación:

- Aplicación: `http://localhost:8080`
- Salud del Front: `http://localhost:8080/health`
- Salud del Back: `http://localhost:8081/api/health`
- RabbitMQ local: `http://localhost:15672`

Las seis cuentas usan la contraseña local de `DEMO_PASSWORD`: `personal.obras`, `responsable.autorizado`, `jefe.cuadrilla`, `operario.contratista`, `inspector.obra` e `ingeniero.arquitecto`. El broker local se incluye para disponibilidad y pruebas controladas; la mensajería del Back queda deshabilitada por defecto para no confundirla con el Core compartido, que requiere credenciales AMQPS privadas. El asistente de IA queda habilitado con el proveedor determinista `mock`, de modo que el arranque reproducible no necesita una API key externa; Azure Test usa Gemini mediante un secreto administrado fuera del repositorio.

Para detener el stack sin borrar datos: `docker compose down`. Para una repetición desde base vacía: `docker compose down --volumes` y luego el comando de inicio.

## Estado actual

- Documentación funcional e integraciones: organizada en [`docs/`](docs/README.md).
- Decisión de cloud: Azure, región `Chile Central` por restricción de la suscripción Azure for Students.
- Infraestructura: Terraform con ambientes `development` y `test`.
- CI/CD: GitHub Actions con autorización de DevOps y autenticación OIDC.
- Bootstrap Azure desplegado: estado remoto, Container Registry, identidad OIDC, permisos y resource groups.
- Plataforma `development` desplegada: Log Analytics y Azure Container Apps Environment en `Chile Central`.
- Plataforma `test`: desplegada en Azure Container Apps mediante Terraform y GitHub Actions.
- Aplicaciones frontend/backend: repositorios separados, integrados por el `compose.yaml` local de Testing y desplegados mediante imágenes inmutables por SHA.

## Accesos rápidos

- [Decisión de arquitectura](docs/arquitectura/adr-001-cloud-y-cicd.md)
- [Operación DevOps](docs/arquitectura/operacion-devops.md)
- [Pipeline de aplicaciones](docs/arquitectura/pipeline-aplicaciones.md)
- [Infraestructura y puesta en marcha](infra/README.md)
- [Terraform CI](.github/workflows/terraform-ci.yml)
- [Despliegue de development](.github/workflows/deploy-development.yml)
- [Despliegue de test](.github/workflows/deploy-test.yml)

## Cierre de la cuarta entrega

1. Ejecutar el gate del tag `v2.0-entrega4` desde un clon limpio.
2. Conservar los artefactos de arranque, ZAP, Gitleaks y k6 producidos por GitHub Actions.
3. Verificar que Azure Test ejecute las mismas revisiones inmutables fijadas en esta candidata.
4. Mantener credenciales, tokens y API keys únicamente en GitHub Environments y secretos de Azure.
