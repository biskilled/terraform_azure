module "init" {
  source = "./init_azure"
}

variable "resource_group_name" {
  type        = string
  description = "Resource group name"
  default     = module.init.resource_group_name
}

variable "resource_group_location" {
  type        = string
  description = "Resource group location"
  default     = module.init.resource_group_location
}

variable "storage_account_name" {
  type        = string
  description = "Storage account name"
  default     = module.init.storage_account_name
}

variable "storage_account_access_key" {
  type        = string
  description = "Storage account access key"
  default     = module.init.storage_account_access_key
}

variable "service_plan_id" {
  type        = string
  description = "Service plan id"
  default     = module.init.service_plan_id
}

variable "storage_container_name" {
  type        = string
  description = "Storage Container name"
  default     = module.init.storage_container_name
}

variable "project" {
  type        = string
  description = "Project name"
  default     = module.init.project
}




