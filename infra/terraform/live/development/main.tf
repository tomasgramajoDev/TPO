module "platform" {
  source = "../../modules/platform"

  project_name        = var.project_name
  environment         = "development"
  location            = var.location
  resource_group_name = "rg-${var.project_name}-dev"
  tags                = var.tags

  enable_postgresql                = true
  postgresql_version               = var.postgresql_version
  postgresql_zone                  = var.postgresql_zone
  postgresql_sku_name              = var.postgresql_sku_name
  postgresql_storage_mb            = var.postgresql_storage_mb
  postgresql_backup_retention_days = var.postgresql_backup_retention_days
  postgresql_database_name         = var.postgresql_database_name
  postgresql_allow_azure_services  = var.postgresql_allow_azure_services

  enable_applications            = true
  container_registry_server      = var.container_registry_server
  container_registry_identity_id = var.container_registry_identity_id
  backend_image                  = var.backend_image
  frontend_image                 = var.frontend_image
}
