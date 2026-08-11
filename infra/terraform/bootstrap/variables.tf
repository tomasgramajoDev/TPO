variable "project_name" {
  description = "Nombre técnico corto del proyecto."
  type        = string
  default     = "obras-publicas"

  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{2,29}$", var.project_name))
    error_message = "project_name debe tener entre 3 y 30 caracteres, comenzar con una letra y usar minúsculas, números o guiones."
  }
}

variable "location" {
  description = "Región Azure para el estado remoto."
  type        = string
  default     = "brazilsouth"
}

variable "github_repository" {
  description = "Repositorio GitHub autorizado para desplegar, en formato owner/name."
  type        = string

  validation {
    condition     = can(regex("^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$", var.github_repository))
    error_message = "github_repository debe usar el formato owner/name."
  }
}

variable "tags" {
  description = "Etiquetas adicionales."
  type        = map(string)
  default     = {}
}
