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
  description = "Versión mayor de PostgreSQL para development."
  type        = string
  default     = "16"
}

variable "postgresql_zone" {
  description = "Zona de disponibilidad de PostgreSQL en development."
  type        = string
  default     = "3"
}

variable "postgresql_sku_name" {
  description = "SKU de PostgreSQL para development."
  type        = string
  default     = "B_Standard_B1ms"
}

variable "postgresql_storage_mb" {
  description = "Almacenamiento de PostgreSQL para development en MiB."
  type        = number
  default     = 32768
}

variable "postgresql_backup_retention_days" {
  description = "Retención de backups de PostgreSQL para development."
  type        = number
  default     = 7
}

variable "postgresql_database_name" {
  description = "Nombre de la base propia del módulo."
  type        = string
  default     = "obras_publicas"
}

variable "postgresql_allow_azure_services" {
  description = "Habilita la regla 0.0.0.0 para servicios Azure."
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
  description = "Imagen inmutable del backend para development."
  type        = string
  default     = "acrobraspublica302ceba6.azurecr.io/obras-publicas-backend:44e1f00ecb4de6f697dae460da91b1b58592faf1"
}

variable "frontend_image" {
  description = "Imagen inmutable del frontend para development."
  type        = string
  default     = "acrobraspublica302ceba6.azurecr.io/obras-publicas-frontend:d472da55fa5dca8f6c351a01805d35495f611486"
}

variable "application_auth_username" {
  description = "Usuario del ambiente development."
  type        = string
  default     = "devops.obras"
}

variable "application_auth_role" {
  description = "Rol funcional del usuario de development."
  type        = string
  default     = "RESPONSABLE_AUTORIZADO"
}

variable "application_messaging_enabled" {
  description = "Habilita la conexion AMQPS del backend development con Core."
  type        = bool
  default     = false
}

variable "application_ai_triage_enabled" {
  description = "Habilita el asistente de triaje de incidentes en development."
  type        = bool
  default     = true
}

variable "application_rabbitmq_password" {
  description = "Contraseña AMQPS de module_obras recibida mediante GitHub Environment secret."
  type        = string
  default     = ""
  sensitive   = true
}
