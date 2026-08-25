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
