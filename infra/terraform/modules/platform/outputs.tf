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

output "postgresql_fqdn" {
  description = "FQDN del servidor PostgreSQL o null cuando está deshabilitado."
  value       = try(azurerm_postgresql_flexible_server.this[0].fqdn, null)
}

output "postgresql_database_name" {
  description = "Nombre de la base PostgreSQL o null cuando está deshabilitada."
  value       = try(azurerm_postgresql_flexible_server_database.this[0].name, null)
}

output "postgresql_administrator_login" {
  description = "Usuario administrador de PostgreSQL o null cuando está deshabilitado."
  value       = var.enable_postgresql ? "obrasadmin" : null
}

output "event_grid_topic_name" {
  description = "Nombre del tópico Event Grid o null cuando está deshabilitado."
  value       = try(azurerm_eventgrid_topic.events[0].name, null)
}

output "event_grid_topic_endpoint" {
  description = "Endpoint del tópico Event Grid o null cuando está deshabilitado."
  value       = try(azurerm_eventgrid_topic.events[0].endpoint, null)
}

output "backend_fqdn" {
  description = "FQDN público del backend o null cuando está deshabilitado."
  value       = try(azurerm_container_app.backend[0].ingress[0].fqdn, null)
}

output "frontend_fqdn" {
  description = "FQDN público del frontend o null cuando está deshabilitado."
  value       = try(azurerm_container_app.frontend[0].ingress[0].fqdn, null)
}

output "application_auth_username" {
  description = "Usuario de demostración de la aplicación."
  value       = var.enable_applications ? var.application_auth_username : null
}

output "application_auth_password" {
  description = "Contraseña generada para el usuario de demostración."
  value       = try(random_password.application_auth[0].result, null)
  sensitive   = true
}
