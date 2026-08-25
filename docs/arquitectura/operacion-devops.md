# Operación DevOps

## Ambientes

El flujo GitFlow siguiente corresponde a los futuros pipelines de frontend y backend. Los workflows existentes en este repositorio administran la plataforma Terraform y conservan sus disparadores actuales hasta que se diseñe una estrategia de ramas específica para infraestructura.

| Ambiente | Disparador de aplicación acordado | Control de DevOps | Estado Terraform |
| --- | --- | --- | --- |
| `development` | Pull request de aplicación fusionado en `develop` | Autorización del despliegue y revisión de smoke tests | `development.terraform.tfstate` |
| `test` | Rama `release/vX.Y.Z` creada o actualizada al cerrar el sprint | Autorización del despliegue y revisión de smoke tests | `test.terraform.tfstate` |

La versión candidata se prueba en `test`; luego el Product Owner la aprueba funcionalmente. Esa aprobación no reemplaza el control operativo de DevOps. Al finalizar, la rama de release se fusiona en `main` y se etiqueta. `main` representa una versión aprobada, pero no despliega a producción mientras ese ambiente no exista.

Estado operativo al 2026-08-13:

- `development` está desplegado en `Chile Central` con Log Analytics y Azure Container Apps Environment;
- `test` continúa pendiente de una release aprobada;
- todavía no hay aplicaciones frontend/backend ejecutándose en los ambientes.

## Recursos del primer incremento

Cada ambiente contiene:

- un resource group propio;
- un workspace de Log Analytics;
- un entorno Azure Container Apps con plan Consumption.

El bootstrap compartido crea:

- el resource group, Storage Account y contenedor privado para el estado remoto;
- los resource groups de `development` y `test`;
- un Azure Container Registry compartido;
- una identidad administrada para GitHub Actions;
- las credenciales federadas OIDC y los roles mínimos necesarios.

## Configuración requerida en GitHub

Crear los ambientes `development` y `test`, agregar al DevOps como revisor obligatorio y definir estas variables en cada ambiente o en el repositorio. Cada job que referencia el ambiente debe superar sus reglas, por lo que DevOps controla por separado el plan y el `apply`:

| Variable | Contenido |
| --- | --- |
| `AZURE_CLIENT_ID` | Client ID de la aplicación o identidad usada por GitHub Actions. |
| `AZURE_TENANT_ID` | Tenant ID de Microsoft Entra. |
| `AZURE_SUBSCRIPTION_ID` | Subscription ID de Azure. |
| `TF_STATE_RESOURCE_GROUP` | Resource group devuelto por el bootstrap. |
| `TF_STATE_STORAGE_ACCOUNT` | Storage account devuelto por el bootstrap. |
| `TF_STATE_CONTAINER` | Contenedor devuelto por el bootstrap; valor predeterminado `tfstate`. |
| `AZURE_CONTAINER_REGISTRY` | Login server del registro compartido, reservado para el pipeline de aplicaciones. |

`ENABLE_AUTOMATIC_DEPLOYMENTS` está configurada en `true` para los workflows Terraform actuales. Un merge a `main` o una release publicada pueden iniciar el flujo de plataforma, pero los jobs de plan y `apply` permanecen bloqueados por la aprobación del environment y conservan la autoridad operativa de DevOps. Esto no define los disparadores de las aplicaciones: al recibir frontend y backend se implementarán con `develop` para `development` y `release/*` para `test`.

Estos identificadores no son contraseñas. No se debe crear `AZURE_CLIENT_SECRET`.

Los revisores obligatorios de ambientes privados requieren un plan GitHub compatible; en GitHub Free están disponibles para repositorios públicos. Si DevOps es la única persona autorizada, no se debe activar `Prevent self-review`.

## Identidad federada

El bootstrap crea una identidad administrada y una credencial federada por environment de GitHub. El subject debe corresponder exactamente a cada ambiente:

- `repo:tomasgramajoDev/TPO:environment:development`
- `repo:tomasgramajoDev/TPO:environment:test`

La identidad recibe `Contributor` solamente en los resource groups de ambos ambientes, `Storage Blob Data Contributor` sobre el Storage Account de estado y `AcrPush` sobre el registro de contenedores. No recibe permisos generales sobre toda la suscripción.

## Secuencia de puesta en marcha

1. Activar Azure for Students o una suscripción equivalente.
2. Crear el repositorio GitHub y subir esta base.
3. Definir `github_repository` y ejecutar una vez `infra/terraform/bootstrap` con una sesión Azure administrativa.
4. Migrar el estado local del bootstrap al backend Azure creado.
5. Configurar variables y revisores de los ambientes GitHub con los outputs del bootstrap.
6. Ejecutar el workflow de desarrollo para verificar acceso y desplegar la plataforma inicial. Completado el 2026-08-13.
7. Ejecutar el workflow de prueba cuando exista una release aprobada.
8. Mantener los disparadores actuales para Terraform y crear por separado los pipelines de aplicación con el GitFlow acordado.

## Reglas operativas

- Revisar el archivo de plan generado antes de aprobar el job `apply`.
- No ejecutar `terraform apply` simultáneamente sobre el mismo ambiente.
- No guardar `.tfstate`, `.tfvars` reales, tokens ni contraseñas en Git.
- Los cambios manuales de emergencia deben documentarse y reconciliarse de inmediato en Terraform.
- Destruir recursos es una acción excepcional y requiere revisar el plan y el ambiente objetivo.

## Definition of Done DevOps propuesta

La Clase 2 presenta una Definition of Done general y otra estricta. Para este proyecto se propone que una historia solo pueda promoverse cuando:

- cumple sus criterios de aceptación;
- las pruebas unitarias, funcionales y de integración aplicables están aprobadas;
- el cambio fue revisado por pares mediante pull request;
- se cumplieron los requisitos no funcionales definidos;
- la documentación técnica fue actualizada;
- cualquier configuración manual posterior al despliegue está identificada;
- el release incluye notas de versión cuando corresponda;
- el Product Owner aceptó la historia.

Estos criterios están `PROPOSED` hasta que el equipo adopte formalmente su Definition of Done. El ejemplo docente de desplegar a producción con el feature toggle desactivado no se aplica todavía: el ambiente de producción y la estrategia de feature flags continúan pendientes.
