terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0.2"
    }
  }
  required_version = ">=1.3.6"

  backend "azurerm" {
    resource_group_name  = var.resource_group_name
    storage_account_name = var.storage_account_name
    container_name       = var.storage_container_name
    key                  = terraform.tfstate
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_application_insights" "insights" {
  name                = "${var.project}-insights"
  location            = var.resource_group_location
  resource_group_name = var.resource_group_name
  application_type    = "Web"
}


resource "azurerm_linux_function_app" "function_app" {
  name                       = "${var.project}-function-app"
  resource_group_name        = var.resource_group_name
  location                   = var.resource_group_name
  storage_account_name       = var.storage_account_name
  storage_account_access_key = var.storage_account_access_key
  service_plan_id            = var.service_plan_id

  app_settings = {}

  tags = {
    environment = var.environment
  }

  site_config {
    application_stack {
      python_version = "3.9" 
    }
    WEBSITE_RUN_FROM_PACKAGE = ""
    FUNCTIONS_WORKER_RUNTIME = "node"
    application_insights_key = azurerm_application_insight.insights.instrumentation_key
  }
}

resource "azurerm_linux_function_app_slot" "example" {
  name                 = "${azurerm_linux_function_app.function_app.name}-dev"
  function_app_id      = azurerm_linux_function_app.function_app.id
  storage_account_name = var.storage_account_name

  site_config {
    application_insights_key = azurerm_application_insight.insights.instrumentation_key
    WEBSITE_RUN_FROM_PACKAGE = ""
  }
}