module "global" {
  source = "../tf"
}

resource "azurerm_function_app" "ms_api_get_tickers" {
  name                     = basename(path.module)
  resource_group_name      = module.global.resource_group_name
  location                 = module.global.resource_group_location
  storage_account_name     = module.global.storage_account_name
  storage_account_access_key= module.global.storage_account_access_key
  app_service_plan_id      = module.global.service_plan_id

  app_settings = {
    "FUNCTIONS_WORKER_RUNTIME" = "python"
  }

   tags = {
    environment = "dev"
  }

}

