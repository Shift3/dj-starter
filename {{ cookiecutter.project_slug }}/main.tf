terraform {
  backend "s3" {
    bucket  = "shift3-terraform-state"
    key     = "{{ cookiecutter.project_slug.replace('_', '-') }}/terraform.tfstate"
    region  = "us-west-2"
    profile = "shift3"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  profile = var.aws_profile
  region  = var.aws_region
  assume_role {
    role_arn = var.aws_assume_role_arn
  }
}

locals {
  workspace_name = "${terraform.workspace}"
  s3_bucket_name = format("%s-%s-bucket", var.application_name, local.workspace_name)
}

module "application" {
  source                        = "git@github.com:Shift3/terraform-modules.git//modules/eb-s3-postgres?ref=boilerplate-experimentation"
  s3_bucket_name                = local.s3_bucket_name
  application_name              = var.application_name
  aws_region                    = var.aws_region
  aws_route53_hosted_zone       = var.aws_route53_hosted_zone
  aws_route53_subdomain         = format("%s-%s", var.application_name, local.workspace_name)
  aws_assume_role_arn           = var.aws_assume_role_arn
  default_tags                  = var.default_tags
  eb_env_variables              = merge(var.eb_env_variables, { DEPLOYED_APPLICATION_NAME = var.application_name, S3_BUCKET = local.s3_bucket_name })
  environment                   = local.workspace_name
}
