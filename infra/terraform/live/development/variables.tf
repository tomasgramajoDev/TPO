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
