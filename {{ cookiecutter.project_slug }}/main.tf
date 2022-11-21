terraform {
  backend "s3" {
    bucket  = "shift3-terraform-state"
    key     = "{{ cookiecutter.project_slug.replace('_', '-') }}/terraform.tfstate"
    region  = "us-west-2"
    profile = "BWTC-Developer"
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
}

locals {
  slug           = "${var.application_name}-${terraform.workspace}"
  workspace_name = "${terraform.workspace}"
  s3_bucket_name = format("%s-%s-bucket", var.application_name, local.workspace_name)
}

module "application" {
  source                        = "git@github.com:Shift3/terraform-modules.git//modules/eb-s3-postgres"
  s3_bucket_name                = local.s3_bucket_name
  application_name              = var.application_name
  aws_region                    = var.aws_region
  aws_route53_hosted_zone       = var.aws_route53_hosted_zone
  aws_route53_subdomain         = format("%s-%s", var.application_name, local.workspace_name)
  aws_assume_role_arn           = var.aws_assume_role_arn
  default_tags                  = var.default_tags
  eb_env_variables              = merge(
    var.eb_env_variables,
    {
      DEPLOYED_APPLICATION_NAME = var.application_name, 
      S3_BUCKET = local.s3_bucket_name,
      REDIS_HOST = aws_elasticache_cluster.main.cache_nodes.0.address,
      REDIS_PORT = aws_elasticache_cluster.main.cache_nodes.0.port
    }
  )
  environment                   = local.workspace_name
}

resource "aws_security_group" "allow_redis_communication" {
  name                   = "${local.slug}-redis-sg"
  description            = "Allows private connection to Elasticache (Redis)"
  egress                 = [{
    cidr_blocks      = [
      "0.0.0.0/0",
    ]
    description      = ""
    from_port        = 0
    ipv6_cidr_blocks = []
    prefix_list_ids  = []
    protocol         = "-1"
    security_groups  = []
    self             = false
    to_port          = 0
  }]
  ingress              = [
    {
      cidr_blocks      = [
        "0.0.0.0/0"
      ]
      description      = "Allows connection to redis"
      from_port        = 6379
      ipv6_cidr_blocks = []
      prefix_list_ids  = []
      protocol         = "tcp"
      security_groups  = []
      self             = false
      to_port          = 6379
    },
  ]
  revoke_rules_on_delete = false
  vpc_id = module.application.vpc_id
}

resource "aws_elasticache_subnet_group" "default" {
  name       = "${local.slug}-cache-subnet"
  subnet_ids = module.application.subnet_ids
}

resource "aws_elasticache_cluster" "main" {
  cluster_id           = "${local.slug}-cluster-redis"
  engine               = "redis"
  node_type            = "cache.t3.micro"
  num_cache_nodes      = 1
  port                 = 6379
  subnet_group_name    = "${aws_elasticache_subnet_group.default.name}"
  security_group_ids   = [aws_security_group.allow_redis_communication.id]
}
