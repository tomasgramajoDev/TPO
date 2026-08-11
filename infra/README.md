# Infraestructura y pipeline

La infraestructura del Módulo 3 se administra con Terraform sobre Microsoft Azure. Los despliegues normales se ejecutan desde GitHub Actions y deben ser autorizados por DevOps.

## Alcance actual

El código prepara:

- estado remoto de Terraform en Azure Blob Storage;
- identidad administrada con OIDC para GitHub Actions, sin `client secret`;
- permisos `Contributor` limitados a los resource groups de `development` y `test`;
- permiso `Storage Blob Data Contributor` para el estado;
- Azure Container Registry compartido con permiso `AcrPush`;
- resource groups separados por ambiente;
- Log Analytics y Azure Container Apps Environment por ambiente.

Todavía no crea las aplicaciones frontend/backend, la base de datos ni la mensajería. Esos recursos dependen del stack y de los repositorios de aplicación.

## Estructura

```text
terraform/
  bootstrap/              Recursos compartidos, estado, identidad OIDC y permisos.
  modules/platform/       Plataforma común por ambiente.
  live/development/       Ambiente de desarrollo.
  live/test/              Ambiente de prueba.
```

## Requisitos

- Terraform `1.15.8`.
- Azure CLI con una sesión administrativa iniciada.
- Una suscripción Azure activa.
- Un repositorio GitHub definitivo.
- Permiso para crear asignaciones de roles en Azure.

Antes del primer `apply`, DevOps debe confirmar que estén registrados los resource providers `Microsoft.Storage`, `Microsoft.ManagedIdentity`, `Microsoft.ContainerRegistry`, `Microsoft.OperationalInsights` y `Microsoft.App`. Terraform no los registra silenciosamente durante el plan.

## 1. Configurar el bootstrap

Copiar el ejemplo sin versionar datos reales:

```powershell
Set-Location infra/terraform/bootstrap
Copy-Item terraform.tfvars.example terraform.tfvars
```

El ejemplo ya contiene el repositorio confirmado `tomasgramajoDev/TPO`. Si el repositorio cambia, actualizar `github_repository`; el valor debe coincidir exactamente con GitHub porque se incorpora al `subject` de las credenciales federadas.

## 2. Crear los recursos compartidos

La primera ejecución usa estado local porque el Storage Account todavía no existe:

```powershell
terraform init -backend=false
terraform fmt -check
terraform validate
terraform plan -out bootstrap.tfplan
terraform apply bootstrap.tfplan
terraform output
```

El plan debe ser revisado antes del `apply`. Esta etapa crea recursos facturables, especialmente Azure Container Registry Basic.

## 3. Migrar el estado del bootstrap a Azure

Completar una copia local de `backend.hcl.example` con los valores de `terraform output backend_config`:

```powershell
Copy-Item backend.tf.example backend.tf
Copy-Item backend.hcl.example backend.hcl
terraform init -migrate-state -backend-config=backend.hcl
```

`backend.tf` activa el backend remoto solamente después de que existe. Comprobar que `terraform.tfstate` ya no sea la fuente activa antes de eliminar o archivar cualquier copia local. `backend.tf`, `backend.hcl`, `terraform.tfvars`, planes y estados están ignorados por Git.

## 4. Configurar GitHub

Crear los environments `development` y `test`. En cada uno cargar estas variables:

| Variable | Output del bootstrap |
| --- | --- |
| `AZURE_CLIENT_ID` | `github_actions_client_id` |
| `AZURE_TENANT_ID` | `tenant_id` |
| `AZURE_SUBSCRIPTION_ID` | `subscription_id` |
| `TF_STATE_RESOURCE_GROUP` | `resource_group_name` |
| `TF_STATE_STORAGE_ACCOUNT` | `storage_account_name` |
| `TF_STATE_CONTAINER` | `container_name` |
| `AZURE_CONTAINER_REGISTRY` | `container_registry_login_server` |

Variable opcional de repositorio:

| Variable | Valor | Efecto |
| --- | --- | --- |
| `ENABLE_AUTOMATIC_DEPLOYMENTS` | `true` | Permite que un push a `main` o una release inicien el flujo automáticamente. Si no existe o vale distinto de `true`, solo DevOps puede iniciarlo con `workflow_dispatch`. |

Configurar a DevOps como revisor obligatorio de ambos environments. No crear `AZURE_CLIENT_SECRET`.

En GitHub Free, los revisores obligatorios para environments solo están disponibles en repositorios públicos. Si el repositorio es privado, se necesita un plan compatible o un control manual alternativo mediante `workflow_dispatch`.

## 5. Flujo automatizado

### Pull request

`terraform-ci.yml` ejecuta:

1. `terraform fmt -check`;
2. `terraform init -backend=false`;
3. `terraform validate` para bootstrap, development y test.

No utiliza credenciales ni modifica Azure.

### Development

De forma predeterminada, DevOps inicia manualmente `deploy-development.yml` después de fusionar el PR. Si se habilita `ENABLE_AUTOMATIC_DEPLOYMENTS=true`, un cambio fusionado en `main` también puede iniciarlo:

1. DevOps autoriza el job que genera el plan.
2. Terraform genera un plan contra `development.terraform.tfstate`.
3. El plan queda visible en el resumen y como artefacto por siete días.
4. DevOps revisa y autoriza el job `apply`.
5. Se aplica exactamente el plan aprobado sobre el mismo commit.

### Test

De forma predeterminada, DevOps inicia `deploy-test.yml` e indica el tag de una release aprobada. Si se habilita `ENABLE_AUTOMATIC_DEPLOYMENTS=true`, una release publicada que no sea prerelease también puede iniciarlo. El procedimiento usa `test.terraform.tfstate` y siempre despliega el tag elegido.

## Validación local

```powershell
terraform fmt -check -recursive infra/terraform
terraform -chdir=infra/terraform/bootstrap init -backend=false -lockfile=readonly
terraform -chdir=infra/terraform/bootstrap validate
terraform -chdir=infra/terraform/live/development init -backend=false -lockfile=readonly
terraform -chdir=infra/terraform/live/development validate
terraform -chdir=infra/terraform/live/test init -backend=false -lockfile=readonly
terraform -chdir=infra/terraform/live/test validate
```

## Reglas de seguridad

- No versionar estados, planes, `tfvars`, `backend.hcl`, tokens ni contraseñas.
- Usar OIDC y permisos limitados por resource group.
- Revisar el plan antes de cada aplicación.
- No ejecutar dos `apply` simultáneos sobre el mismo ambiente.
- No reconstruir una imagen al promoverla de development a test: se debe promover el mismo digest.
- Cualquier cambio manual en Azure debe documentarse y reconciliarse en Terraform.
