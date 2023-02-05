terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0.2"
    }
  }
  required_version = ">=1.3.6"

  backend "azurerm" {
    resource_group_name  = "DefaultResourceGroup-EUS"
    storage_account_name = "tfstatessa1"
    container_name       = "tfstatessac"
    key                  = "tfstatessac.tfstate"
  }

}

provider "azurerm" {
  features {}
}


resource "azurerm_resource_group" "resource_group" {
  name     = "${var.project}_rsg"
  location = var.location
}

resource "azurerm_storage_account" "storage_account" {
  name                     = "${var.project}acco"
  resource_group_name      = azurerm_resource_group.resource_group.name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_service_plan" "service_plan" {
  name                = "${var.project}_splan"
  location            = var.location
  resource_group_name = azurerm_resource_group.resource_group.name
  os_type             = "Linux"
  sku_name            = "Y1"
}


resource "azurerm_linux_function_app" "function_app" {
  name                       = "${var.project}-function-app"
  resource_group_name        = azurerm_resource_group.resource_group.name
  location                   = azurerm_resource_group.resource_group.location
  storage_account_name       = azurerm_storage_account.storage_account.name
  storage_account_access_key = azurerm_storage_account.storage_account.primary_access_key
  service_plan_id            = azurerm_service_plan.service_plan.id

  app_settings = {

  }


  site_config {
    application_stack {
      python_version = "3.9"
    }
   }
}