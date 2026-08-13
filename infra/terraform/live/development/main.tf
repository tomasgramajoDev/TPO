module "platform" {
  source = "../../modules/platform"

  project_name        = var.project_name
  environment         = "development"
  location            = var.location
  resource_group_name = "rg-${var.project_name}-dev"
  tags                = var.tags
}
