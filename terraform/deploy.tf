terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0.2"
    }
  }
  required_version = ">=1.3.6"

  backend "azurerm" {
    resource_group_name  = "tamopstfstates"
    storage_account_name = "tfstatedevops"
    container_name       = "terraformgithubexample"
    key                  = "terraformgithubexample.tfstate"
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "resource_group" {
  name     = "${var.project}_${var.environment}_rg"
  location = var.location
}

resource "azurerm_storage_account" "storage_account" {
  name                     = "${var.project}${var.environment}acc"
  resource_group_name      = azurerm_resource_group.resource_group.name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}


resource "azurerm_service_plan" "service_plan" {
  name                = "${var.project}_${var.environment}_plan"
  location            = var.location
  resource_group_name = azurerm_resource_group.resource_group.name
  os_type             = "Linux"
  sku_name            = "Y1"
}


resource "azurerm_linux_function_app" "function_app" {
  name                       = "${var.project}-${var.environment}-function-app"
  resource_group_name        = azurerm_resource_group.resource_group.name
  location                   = azurerm_resource_group.resource_group.location
  storage_account_name       = azurerm_storage_account.storage_account.name
  storage_account_access_key = azurerm_storage_account.storage_account.primary_access_key
  service_plan_id            = azurerm_service_plan.service_plan.id

  app_settings = {}

  tags = {
    environment = var.environment
  }

  site_config {
    application_stack {
      python_version = "3.9"
      WEBSITE_RUN_FROM_PACKAGE = ""
      FUNCTIONS_WORKER_RUNTIME = "node" 
    }
  }
}

/*
module "api-1" {
  source = "../api-1"
  resource_group_name = azurerm_resource_group.resource_group.name
  resource_group_location = azurerm_resource_group.resource_group.location
  storage_account_name= azurerm_storage_account.storage_account.name
  storage_account_access_key= azurerm_storage_account.storage_account.primary_access_key
  service_plan_id= azurerm_service_plan.service_plan.id
  environment = var.environment
}
*/