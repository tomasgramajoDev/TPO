output "resource_group_name" {
  description = "Resource group del ambiente."
  value       = var.resource_group_name
}

output "container_app_environment_id" {
  description = "ID del entorno Azure Container Apps."
  value       = azurerm_container_app_environment.this.id
}

output "log_analytics_workspace_id" {
  description = "ID del workspace de observabilidad."
  value       = azurerm_log_analytics_workspace.this.id
}
