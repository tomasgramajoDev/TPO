module "platform" {
  source = "../../modules/platform"

  project_name        = var.project_name
  environment         = "test"
  location            = var.location
  resource_group_name = "rg-${var.project_name}-tst"
  tags                = var.tags
}
