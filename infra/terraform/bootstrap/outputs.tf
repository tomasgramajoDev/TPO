output "resource_group_name" {
  description = "Resource group del backend Terraform."
  value       = azurerm_resource_group.terraform_state.name
}

output "storage_account_name" {
  description = "Storage account del backend Terraform."
  value       = azurerm_storage_account.terraform_state.name
}

output "container_name" {
  description = "Contenedor del backend Terraform."
  value       = azurerm_storage_container.terraform_state.name
}

output "storage_account_id" {
  description = "Scope recomendado para Storage Blob Data Contributor."
  value       = azurerm_storage_account.terraform_state.id
}

output "subscription_id" {
  description = "Subscription ID para AZURE_SUBSCRIPTION_ID."
  value       = data.azurerm_subscription.current.subscription_id
}

output "tenant_id" {
  description = "Tenant ID para AZURE_TENANT_ID."
  value       = azurerm_user_assigned_identity.github_actions.tenant_id
}

output "github_actions_client_id" {
  description = "Client ID de la identidad OIDC para AZURE_CLIENT_ID."
  value       = azurerm_user_assigned_identity.github_actions.client_id
}

output "github_actions_principal_id" {
  description = "Object ID de la identidad OIDC para auditoría de roles."
  value       = azurerm_user_assigned_identity.github_actions.principal_id
}

output "environment_resource_groups" {
  description = "Resource groups administrados por los pipelines."
  value       = { for name, group in azurerm_resource_group.environment : name => group.name }
}

output "container_registry_name" {
  description = "Nombre del Azure Container Registry compartido."
  value       = azurerm_container_registry.shared.name
}

output "container_registry_login_server" {
  description = "Servidor de login del Azure Container Registry compartido."
  value       = azurerm_container_registry.shared.login_server
}

output "backend_config" {
  description = "Valores no secretos para configurar el backend remoto."
  value = {
    resource_group_name  = azurerm_resource_group.terraform_state.name
    storage_account_name = azurerm_storage_account.terraform_state.name
    container_name       = azurerm_storage_container.terraform_state.name
  }
}
