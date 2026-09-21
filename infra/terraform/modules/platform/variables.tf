variable "project_name" {
  description = "Nombre técnico corto del proyecto."
  type        = string

  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{2,29}$", var.project_name))
    error_message = "project_name debe tener entre 3 y 30 caracteres, comenzar con una letra y usar minúsculas, números o guiones."
  }
}

variable "environment" {
  description = "Ambiente de despliegue."
  type        = string

  validation {
    condition     = contains(["development", "test"], var.environment)
    error_message = "environment debe ser development o test."
  }
}

variable "location" {
  description = "Región Azure."
  type        = string
}

variable "resource_group_name" {
  description = "Resource group precreado por el bootstrap para el ambiente."
  type        = string
}

variable "tags" {
  description = "Etiquetas comunes para los recursos."
  type        = map(string)
  default     = {}
}

variable "enable_postgresql" {
  description = "Crea Azure Database for PostgreSQL Flexible Server en el ambiente."
  type        = bool
  default     = false
}

variable "postgresql_version" {
  description = "Versión mayor de PostgreSQL."
  type        = string
  default     = "16"

  validation {
    condition     = contains(["14", "15", "16", "17", "18"], var.postgresql_version)
    error_message = "postgresql_version debe ser una versión soportada entre 14 y 18."
  }
}

variable "postgresql_zone" {
  description = "Zona de disponibilidad asignada al servidor PostgreSQL."
  type        = string
  default     = null

  validation {
    condition     = var.postgresql_zone == null || contains(["1", "2", "3"], var.postgresql_zone)
    error_message = "postgresql_zone debe ser null, 1, 2 o 3."
  }
}

variable "postgresql_sku_name" {
  description = "SKU de Azure Database for PostgreSQL Flexible Server."
  type        = string
  default     = "B_Standard_B1ms"
}

variable "postgresql_storage_mb" {
  description = "Almacenamiento máximo de PostgreSQL en MiB. Azure no permite reducirlo."
  type        = number
  default     = 32768

  validation {
    condition     = contains([32768, 65536, 131072, 262144, 524288, 1048576], var.postgresql_storage_mb)
    error_message = "postgresql_storage_mb debe usar un tamaño soportado de al menos 32768 MiB."
  }
}

variable "postgresql_backup_retention_days" {
  description = "Días de retención de backups de PostgreSQL."
  type        = number
  default     = 7

  validation {
    condition     = var.postgresql_backup_retention_days >= 7 && var.postgresql_backup_retention_days <= 35
    error_message = "postgresql_backup_retention_days debe estar entre 7 y 35."
  }
}

variable "postgresql_database_name" {
  description = "Nombre de la base de datos propia del módulo."
  type        = string
  default     = "obras_publicas"

  validation {
    condition     = can(regex("^[a-z][a-z0-9_]{2,62}$", var.postgresql_database_name))
    error_message = "postgresql_database_name debe ser un identificador PostgreSQL en minúsculas."
  }
}

variable "postgresql_allow_azure_services" {
  description = "Permite conexiones desde direcciones de servicios Azure. Solo se habilita de forma explícita."
  type        = bool
  default     = false
}

variable "enable_event_grid" {
  description = "Crea un tópico de Azure Event Grid para los eventos del módulo."
  type        = bool
  default     = false
}

variable "enable_applications" {
  description = "Crea las Container Apps de frontend y backend."
  type        = bool
  default     = false
}

variable "container_registry_server" {
  description = "Servidor del Azure Container Registry que contiene las imágenes."
  type        = string
  default     = null
}

variable "container_registry_identity_id" {
  description = "Resource ID de la identidad administrada con permiso AcrPull."
  type        = string
  default     = null
}

variable "backend_image" {
  description = "Referencia inmutable de la imagen del backend."
  type        = string
  default     = null
}

variable "frontend_image" {
  description = "Referencia inmutable de la imagen del frontend."
  type        = string
  default     = null
}

variable "application_auth_username" {
  description = "Usuario de demostración entregado al backend mediante configuración."
  type        = string
  default     = "devops.obras"
}

variable "application_auth_role" {
  description = "Rol funcional del usuario de demostración."
  type        = string
  default     = "RESPONSABLE_AUTORIZADO"
}

variable "application_demo_password" {
  description = "Contraseña opcional para las cuentas de prueba por rol. Si se omite, Terraform genera una."
  type        = string
  default     = null
  nullable    = true
  sensitive   = true
}

variable "application_bootstrap_users_json" {
  description = "Array JSON opcional de cuentas iniciales suministrado como secreto por ambiente. No actualiza cuentas existentes."
  type        = string
  default     = null
  nullable    = true
  sensitive   = true

  validation {
    condition     = var.application_bootstrap_users_json == null ? true : can(jsondecode(var.application_bootstrap_users_json))
    error_message = "application_bootstrap_users_json debe ser JSON valido."
  }
}
