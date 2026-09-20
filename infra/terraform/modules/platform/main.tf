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

  application_demo_password = coalesce(var.application_demo_password, try(random_password.application_demo[0].result, null))
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

resource "random_password" "application_auth" {
  count            = var.enable_applications ? 1 : 0
  length           = 24
  special          = true
  min_lower        = 2
  min_numeric      = 2
  min_special      = 2
  min_upper        = 2
  override_special = "!#$%&*()-_=+[]{}:?"
}

resource "random_password" "application_demo" {
  count            = var.enable_applications ? 1 : 0
  length           = 24
  special          = true
  min_lower        = 2
  min_numeric      = 2
  min_special      = 2
  min_upper        = 2
  override_special = "!#$%&*()-_=+[]{}:?"
}

resource "random_password" "jwt_secret" {
  count   = var.enable_applications ? 1 : 0
  length  = 48
  special = false
}

resource "azurerm_postgresql_flexible_server" "this" {
  count = var.enable_postgresql ? 1 : 0

  name                          = "psql-${local.resource_prefix}-${random_id.postgresql_suffix[0].hex}"
  resource_group_name           = var.resource_group_name
  location                      = var.location
  zone                          = var.postgresql_zone
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

resource "azurerm_eventgrid_topic" "events" {
  count = var.enable_event_grid ? 1 : 0

  name                          = "egt-${local.resource_prefix}-events"
  location                      = var.location
  resource_group_name           = var.resource_group_name
  input_schema                  = "CloudEventSchemaV1_0"
  public_network_access_enabled = true
  local_auth_enabled            = true
  tags                          = local.common_tags

  lifecycle {
    prevent_destroy = true
  }
}

resource "azurerm_container_app" "backend" {
  count = var.enable_applications ? 1 : 0

  name                         = "ca-${local.resource_prefix}-backend"
  container_app_environment_id = azurerm_container_app_environment.this.id
  resource_group_name          = var.resource_group_name
  revision_mode                = "Single"
  workload_profile_name        = "Consumption"
  tags                         = local.common_tags

  identity {
    type         = "UserAssigned"
    identity_ids = [var.container_registry_identity_id]
  }

  registry {
    server   = var.container_registry_server
    identity = var.container_registry_identity_id
  }

  secret {
    name  = "db-password"
    value = random_password.postgresql_admin[0].result
  }

  secret {
    name  = "auth-password"
    value = random_password.application_auth[0].result
  }

  secret {
    name = "auth-bootstrap-users"
    value = jsonencode([
      { username = "personal.obras", password = local.application_demo_password, role = "PERSONAL_OBRAS" },
      { username = "responsable", password = local.application_demo_password, role = "RESPONSABLE_AUTORIZADO" },
      { username = "jefe.cuadrilla", password = local.application_demo_password, role = "JEFE_CUADRILLA" },
      { username = "operario", password = local.application_demo_password, role = "OPERARIO_CONTRATISTA" },
      { username = "inspector", password = local.application_demo_password, role = "INSPECTOR_OBRA" }
    ])
  }

  secret {
    name  = "jwt-secret"
    value = random_password.jwt_secret[0].result
  }

  dynamic "secret" {
    for_each = var.enable_event_grid ? [1] : []

    content {
      name  = "event-grid-access-key"
      value = azurerm_eventgrid_topic.events[0].primary_access_key
    }
  }

  ingress {
    external_enabled = true
    target_port      = 8080
    transport        = "auto"

    traffic_weight {
      latest_revision = true
      percentage      = 100
    }
  }

  template {
    min_replicas = 0
    max_replicas = 1

    container {
      name   = "backend"
      image  = var.backend_image
      cpu    = 0.5
      memory = "1Gi"

      env {
        name  = "DB_URL"
        value = "jdbc:postgresql://${azurerm_postgresql_flexible_server.this[0].fqdn}:5432/${azurerm_postgresql_flexible_server_database.this[0].name}?sslmode=require"
      }

      env {
        name  = "DB_USERNAME"
        value = "obrasadmin"
      }

      env {
        name        = "DB_PASSWORD"
        secret_name = "db-password"
      }

      env {
        name  = "AUTH_USERNAME"
        value = var.application_auth_username
      }

      env {
        name        = "AUTH_PASSWORD"
        secret_name = "auth-password"
      }

      env {
        name        = "AUTH_BOOTSTRAP_USERS"
        secret_name = "auth-bootstrap-users"
      }

      env {
        name  = "AUTH_ROLE"
        value = var.application_auth_role
      }

      env {
        name        = "JWT_SECRET"
        secret_name = "jwt-secret"
      }

      dynamic "env" {
        for_each = var.enable_event_grid ? [1] : []

        content {
          name  = "EVENT_GRID_TOPIC_ENDPOINT"
          value = azurerm_eventgrid_topic.events[0].endpoint
        }
      }

      dynamic "env" {
        for_each = var.enable_event_grid ? [1] : []

        content {
          name        = "EVENT_GRID_ACCESS_KEY"
          secret_name = "event-grid-access-key"
        }
      }

      liveness_probe {
        transport               = "HTTP"
        port                    = 8080
        path                    = "/api/health"
        initial_delay           = 15
        interval_seconds        = 30
        timeout                 = 5
        failure_count_threshold = 3
      }

      readiness_probe {
        transport               = "HTTP"
        port                    = 8080
        path                    = "/api/health"
        interval_seconds        = 10
        timeout                 = 5
        failure_count_threshold = 6
      }
    }
  }

  lifecycle {
    prevent_destroy = true
  }
}

resource "azurerm_container_app" "frontend" {
  count = var.enable_applications ? 1 : 0

  name                         = "ca-${local.resource_prefix}-frontend"
  container_app_environment_id = azurerm_container_app_environment.this.id
  resource_group_name          = var.resource_group_name
  revision_mode                = "Single"
  workload_profile_name        = "Consumption"
  tags                         = local.common_tags

  identity {
    type         = "UserAssigned"
    identity_ids = [var.container_registry_identity_id]
  }

  registry {
    server   = var.container_registry_server
    identity = var.container_registry_identity_id
  }

  ingress {
    external_enabled = true
    target_port      = 8080
    transport        = "auto"

    traffic_weight {
      latest_revision = true
      percentage      = 100
    }
  }

  template {
    min_replicas = 0
    max_replicas = 1

    container {
      name   = "frontend"
      image  = var.frontend_image
      cpu    = 0.25
      memory = "0.5Gi"

      env {
        name  = "BACKEND_HOST"
        value = azurerm_container_app.backend[0].ingress[0].fqdn
      }

      liveness_probe {
        transport               = "HTTP"
        port                    = 8080
        path                    = "/health"
        initial_delay           = 10
        interval_seconds        = 30
        timeout                 = 5
        failure_count_threshold = 3
      }

      readiness_probe {
        transport               = "HTTP"
        port                    = 8080
        path                    = "/health"
        interval_seconds        = 10
        timeout                 = 5
        failure_count_threshold = 6
      }
    }
  }

  lifecycle {
    prevent_destroy = true
  }
}
