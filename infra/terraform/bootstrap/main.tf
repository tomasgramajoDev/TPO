locals {
  storage_project         = substr(replace(lower(var.project_name), "/[^a-z0-9]/", ""), 0, 12)
  resource_group_location = coalesce(var.resource_group_location, var.location)
  environment_short = {
    development = "dev"
    test        = "tst"
  }
  common_tags = merge(var.tags, {
    managedBy = "terraform"
    project   = var.project_name
  })
}

data "azurerm_client_config" "current" {}

data "azurerm_subscription" "current" {}

resource "random_id" "storage_suffix" {
  byte_length = 4
}

resource "azurerm_resource_group" "terraform_state" {
  name     = "rg-${var.project_name}-tfstate"
  location = local.resource_group_location
  tags = merge(local.common_tags, {
    purpose = "terraform-state"
  })
}

resource "azurerm_resource_group" "shared" {
  name     = "rg-${var.project_name}-shared"
  location = local.resource_group_location
  tags = merge(local.common_tags, {
    purpose = "shared-platform"
  })
}

resource "azurerm_resource_group" "environment" {
  for_each = local.environment_short

  name     = "rg-${var.project_name}-${each.value}"
  location = local.resource_group_location
  tags = merge(local.common_tags, {
    environment = each.key
    purpose     = "application-platform"
  })
}

resource "azurerm_storage_account" "terraform_state" {
  name                            = "st${local.storage_project}${random_id.storage_suffix.hex}"
  resource_group_name             = azurerm_resource_group.terraform_state.name
  location                        = var.location
  account_tier                    = "Standard"
  account_replication_type        = "LRS"
  min_tls_version                 = "TLS1_2"
  default_to_oauth_authentication = true
  allow_nested_items_to_be_public = false
  tags                            = local.common_tags

  blob_properties {
    versioning_enabled = true

    delete_retention_policy {
      days = 7
    }

    container_delete_retention_policy {
      days = 7
    }
  }

  lifecycle {
    prevent_destroy = true
  }
}

resource "azurerm_storage_container" "terraform_state" {
  name                  = "tfstate"
  storage_account_id    = azurerm_storage_account.terraform_state.id
  container_access_type = "private"

  lifecycle {
    prevent_destroy = true
  }
}

resource "azurerm_user_assigned_identity" "github_actions" {
  name                = "id-${var.project_name}-github"
  location            = var.location
  resource_group_name = azurerm_resource_group.shared.name
  tags                = local.common_tags
}

resource "azurerm_federated_identity_credential" "github_environment" {
  for_each = local.environment_short

  name                      = "github-${each.key}"
  user_assigned_identity_id = azurerm_user_assigned_identity.github_actions.id
  audience                  = ["api://AzureADTokenExchange"]
  issuer                    = "https://token.actions.githubusercontent.com"
  subject                   = "repo:${var.github_repository}:environment:${each.key}"
}

resource "azurerm_role_assignment" "github_environment_contributor" {
  for_each = azurerm_resource_group.environment

  scope                            = each.value.id
  role_definition_name             = "Contributor"
  principal_id                     = azurerm_user_assigned_identity.github_actions.principal_id
  skip_service_principal_aad_check = true
}

resource "azurerm_role_assignment" "github_state" {
  scope                            = azurerm_storage_account.terraform_state.id
  role_definition_name             = "Storage Blob Data Contributor"
  principal_id                     = azurerm_user_assigned_identity.github_actions.principal_id
  skip_service_principal_aad_check = true
}

resource "azurerm_role_assignment" "bootstrap_operator_state" {
  scope                = azurerm_storage_account.terraform_state.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = data.azurerm_client_config.current.object_id
}

resource "azurerm_container_registry" "shared" {
  name = substr(
    "acr${local.storage_project}${substr(md5(data.azurerm_subscription.current.subscription_id), 0, 8)}",
    0,
    50
  )
  resource_group_name = azurerm_resource_group.shared.name
  location            = var.location
  sku                 = "Basic"
  admin_enabled       = false
  tags                = local.common_tags
}

resource "azurerm_role_assignment" "github_acr_push" {
  scope                            = azurerm_container_registry.shared.id
  role_definition_name             = "AcrPush"
  principal_id                     = azurerm_user_assigned_identity.github_actions.principal_id
  skip_service_principal_aad_check = true
}
