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
