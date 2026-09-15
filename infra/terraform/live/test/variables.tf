variable "project_name" {
  description = "Nombre técnico corto del proyecto."
  type        = string
  default     = "obras-publicas"
}

variable "location" {
  description = "Región Azure."
  type        = string
  default     = "chilecentral"
}

variable "tags" {
  description = "Etiquetas adicionales."
  type        = map(string)
  default     = {}
}

variable "postgresql_version" {
  description = "Versión mayor de PostgreSQL para test."
  type        = string
  default     = "16"
}

variable "postgresql_zone" {
  description = "Zona de disponibilidad de PostgreSQL en test."
  type        = string
  default     = "3"
}

variable "postgresql_sku_name" {
  description = "SKU de PostgreSQL para test."
  type        = string
  default     = "B_Standard_B1ms"
}

variable "postgresql_storage_mb" {
  description = "Almacenamiento de PostgreSQL para test en MiB."
  type        = number
  default     = 32768
}

variable "postgresql_backup_retention_days" {
  description = "Retención de backups de PostgreSQL para test."
  type        = number
  default     = 7
}

variable "postgresql_database_name" {
  description = "Nombre de la base propia del módulo en test."
  type        = string
  default     = "obras_publicas"
}

variable "postgresql_allow_azure_services" {
  description = "Habilita temporalmente conexiones desde servicios Azure."
  type        = bool
  default     = true
}

variable "container_registry_server" {
  description = "Servidor ACR compartido."
  type        = string
  default     = "acrobraspublica302ceba6.azurecr.io"
}

variable "container_registry_identity_id" {
  description = "Identidad administrada compartida con acceso al ACR."
  type        = string
  default     = "/subscriptions/a73a7c37-3892-40df-821d-09c80677031f/resourceGroups/rg-obras-publicas-shared/providers/Microsoft.ManagedIdentity/userAssignedIdentities/id-obras-publicas-github"
}

variable "backend_image" {
  description = "Imagen inmutable del backend promovida a test."
  type        = string
  default     = "acrobraspublica302ceba6.azurecr.io/obras-publicas-backend:b70379b077881a4b03ff4a4e5244d2f8195cf9a2"
}

variable "frontend_image" {
  description = "Imagen inmutable del frontend promovida a test."
  type        = string
  default     = "acrobraspublica302ceba6.azurecr.io/obras-publicas-frontend:9175534aa57e003caaebb7df2479f6e076c8e066"
}
