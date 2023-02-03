variable "project" {
  type        = string
  description = "Project name"
  default     = "project"
}

variable "environment" {
  type        = string
  description = "Environment (dev / stage / prod)"
  default     = "dev"
}

variable "location" {
  type        = string
  description = "Azure region to deploy module to"
  default     = "East US"
}

variable "git_repo" {
  type        = string
  description = "Git repo url"
  default     = "https://github.com/<username>/<repo-name>"
}

variable "git_prod_brunch" {
  type        = string
  description = "Git production brunch name"
  default     = "main"
}



