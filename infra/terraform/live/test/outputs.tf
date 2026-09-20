output "resource_group_name" {
  value = module.platform.resource_group_name
}

output "container_app_environment_id" {
  value = module.platform.container_app_environment_id
}

output "log_analytics_workspace_id" {
  value = module.platform.log_analytics_workspace_id
}

output "postgresql_fqdn" {
  value = module.platform.postgresql_fqdn
}

output "postgresql_database_name" {
  value = module.platform.postgresql_database_name
}

output "postgresql_administrator_login" {
  value = module.platform.postgresql_administrator_login
}

output "event_grid_topic_name" {
  value = module.platform.event_grid_topic_name
}

output "event_grid_topic_endpoint" {
  value = module.platform.event_grid_topic_endpoint
}

output "backend_fqdn" {
  value = module.platform.backend_fqdn
}

output "frontend_fqdn" {
  value = module.platform.frontend_fqdn
}

output "application_auth_username" {
  value = module.platform.application_auth_username
}

output "application_auth_password" {
  value     = module.platform.application_auth_password
  sensitive = true
}

output "application_demo_password" {
  value     = module.platform.application_demo_password
  sensitive = true
}

output "application_demo_usernames" {
  value = module.platform.application_demo_usernames
}
