variable "function_directory" {
  type = string
  default = "api_1"
}
variable "function_name" {
  type = string
  default= "api_1"
}

locals {
  resource_group_name = azurerm_resource_group.resource_group.name
  storage_account_key = azurerm_storage_account.storage_account.primary_access_key
  storage_account_name = azurerm_storage_account.storage_account.name
  // azurerm_storage_account.example.name
}

resource "null_resource" "filter_python_files" {
 provisioner "local-exec" {
  command = "for file in $(ls ${var.function_directory}); do if [ -f ${var.function_directory}/${file} ] && [ $${file: -3} == '.py' ]; then az storage blob upload --account-name ${local.storage_account_name} --account-key ${local.storage_account_key} --type block --source ${local.function_directory}/${file} --container-name site --name ${file}; fi; done"
  }
}
