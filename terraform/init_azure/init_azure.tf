### INSTALL FIRST TIME CONFIGURATION ###

terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0.2"
    }
  }
  required_version = ">=1.3.6"
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "resource_group" {
  name     = "${var.project}_rg"
  location = var.location
}

resource "azurerm_storage_account" "storage_account" {
  name                     = "${var.project}acc"
  resource_group_name      = azurerm_resource_group.resource_group.name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_service_plan" "service_plan" {
  name                = "${var.project}_plan"
  location            = var.location
  resource_group_name = azurerm_resource_group.resource_group.name
  os_type             = "Linux"
  sku_name            = "Y1"
}

resource "azurerm_storage_container" "storage_container" {
  name                  = "${var.project}_cn"
  storage_account_name  = azurerm_storage_account.storage_account.name 
  
}

output "resource_group_name" {value = azurerm_resource_group.resource_group.name}
output "resource_group_location" {value = azurerm_resource_group.resource_group.location}
output "storage_account_name" {value = azurerm_storage_account.storage_account.name}
output "storage_account_access_key" {value = azurerm_storage_account.storage_account.primary_access_key}
output "service_plan_id" {value = azurerm_service_plan.service_plan.id}
output "storage_container_name" {value = azurerm_storage_container.storage_container.name}
output "project" {value = var.project}