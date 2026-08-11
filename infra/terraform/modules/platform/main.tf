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
}
