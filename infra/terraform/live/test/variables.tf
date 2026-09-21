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
  default     = "acrobraspublica302ceba6.azurecr.io/obras-publicas-backend:91f30e4c7b5e03d0fd33fb831a30c63fae09ada3"
}

variable "frontend_image" {
  description = "Imagen inmutable del frontend promovida a test."
  type        = string
  default     = "acrobraspublica302ceba6.azurecr.io/obras-publicas-frontend:f8d6a585e0f8e17fb19fa0a76d2e9de72ca6fc30"
}

variable "application_auth_username" {
  description = "Usuario del ambiente test."
  type        = string
  default     = "devops.obras"
}

variable "application_auth_role" {
  description = "Rol funcional del usuario de test."
  type        = string
  default     = "RESPONSABLE_AUTORIZADO"
}

variable "application_demo_password" {
  description = "Contraseña secreta compartida por las cuentas de prueba de Test."
  type        = string
  default     = null
  nullable    = true
  sensitive   = true
}

variable "application_bootstrap_users_json" {
  description = "JSON privado de las cuentas de Test. Se recibe solo desde el secreto GitHub TEST_BOOTSTRAP_USERS."
  type        = string
  default     = null
  nullable    = true
  sensitive   = true
}
