locals {
  environment_short = {
    development = "dev"
    test        = "tst"
  }

  resource_prefix = "${var.project_name}-${local.environment_short[var.environment]}"
  common_tags = merge(var.tags, {
    environment = var.environment
    managedBy   = "terraform"
    project     = var.project_name
  })
}

resource "azurerm_log_analytics_workspace" "this" {
  name                = "log-${local.resource_prefix}"
  location            = var.location
  resource_group_name = var.resource_group_name
  sku                 = "PerGB2018"
  retention_in_days   = 30
  tags                = local.common_tags
}

resource "azurerm_container_app_environment" "this" {
  name                       = "cae-${local.resource_prefix}"
  location                   = var.location
  resource_group_name        = var.resource_group_name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.this.id
  tags                       = local.common_tags

  workload_profile {
    name                  = "Consumption"
    workload_profile_type = "Consumption"
    minimum_count         = 0
    maximum_count         = 0
  }
}

resource "random_id" "postgresql_suffix" {
  count       = var.enable_postgresql ? 1 : 0
  byte_length = 3
}

resource "random_password" "postgresql_admin" {
  count            = var.enable_postgresql ? 1 : 0
  length           = 24
  special          = true
  min_lower        = 2
  min_numeric      = 2
  min_special      = 2
  min_upper        = 2
  override_special = "!#$%&*()-_=+[]{}:?"
}

resource "azurerm_postgresql_flexible_server" "this" {
  count = var.enable_postgresql ? 1 : 0

  name                          = "psql-${local.resource_prefix}-${random_id.postgresql_suffix[0].hex}"
  resource_group_name           = var.resource_group_name
  location                      = var.location
  version                       = var.postgresql_version
  administrator_login           = "obrasadmin"
  administrator_password        = random_password.postgresql_admin[0].result
  public_network_access_enabled = true
  sku_name                      = var.postgresql_sku_name
  storage_mb                    = var.postgresql_storage_mb
  storage_tier                  = "P4"
  backup_retention_days         = var.postgresql_backup_retention_days
  geo_redundant_backup_enabled  = false
  tags                          = local.common_tags

  authentication {
    active_directory_auth_enabled = false
    password_auth_enabled         = true
  }

  lifecycle {
    prevent_destroy = true
  }
}

resource "azurerm_postgresql_flexible_server_database" "this" {
  count = var.enable_postgresql ? 1 : 0

  name      = var.postgresql_database_name
  server_id = azurerm_postgresql_flexible_server.this[0].id
  charset   = "UTF8"
  collation = "en_US.utf8"

  lifecycle {
    prevent_destroy = true
  }
}

resource "azurerm_postgresql_flexible_server_firewall_rule" "azure_services" {
  count = var.enable_postgresql && var.postgresql_allow_azure_services ? 1 : 0

  name             = "allow-azure-services"
  server_id        = azurerm_postgresql_flexible_server.this[0].id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "0.0.0.0"
}
