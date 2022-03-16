terraform {
  backend "s3" {
    bucket  = "shift3-terraform-state"
    key     = "<project-name>/<environment>/terraform.tfstate"
    region  = "us-west-2"
    profile = "shift3"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "2.58"
    }
  }
}

provider "aws" {
  profile = var.aws_profile
  region  = var.aws_region
  # assume_role {
  #   role_arn = var.aws_assume_role_arn
  # }
}

locals {
  api_domain_name    = var.aws_route53_subdomain == "" ?  "${var.application_name}.${var.aws_route53_hosted_zone}" : "${var.aws_route53_subdomain}.${var.aws_route53_hosted_zone}"
  workspace_name     = "${terraform.workspace}"
  app_name           = "${var.application_name}-${terraform.workspace}"
  database_connection_variables = {
    DB_NAME          = replace("${var.application_name}_${terraform.workspace}_db", "/\\s+|\\-+/", "_")
    DB_PASSWORD      = sha1(uuid())
    DB_PORT          = "5432"
    DB_USER          = replace("${var.application_name}_admin", "/\\s+|\\-+/", "_")
  }
}

resource "aws_default_vpc" "default" {}

data "aws_subnet_ids" "default" {
  vpc_id = aws_default_vpc.default.id
}

module "boilerplate_ecr" {
  source = "git@github.com:Shift3/terraform-modules.git//modules/aws/ecr"

  name   = local.app_name
}

module "eb_acm" {
  source      = "git@github.com:Shift3/terraform-modules.git//modules/aws/acm"

  domain_name = local.api_domain_name
  hosted_zone = var.aws_route53_hosted_zone
}

resource "aws_security_group" "allow_db_communication" {
  name        = "${local.app_name}-db-sg"
  description = "Allows private connection to DB instance"
  tags        = merge({ "Name" = "${local.app_name}-db-sg" }, var.default_tags)
  vpc_id      = aws_default_vpc.default.id

  ingress {
    description = "Allows connection to postgres"
    protocol    = "tcp"
    from_port   = 5432
    to_port     = 5432
    self        = true
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

module "rds_instance" {
  source = "git@github.com:Shift3/terraform-modules.git//modules/aws/rds"

  allocated_storage             = "20"
  apply_immediately             = true
  backup_window                 = "09:30-10:00"
  backup_retention_period       = "14"
  database_connection_variables = local.database_connection_variables
  deletion_protection           = true
  engine                        = "postgres"
  final_snapshot_identifier     = "${var.application_name}-final-${uuid()}"
  identifier                    = "${local.app_name}-db"
  instance_class                = "db.t3.micro"
  maintenance_window            = "Sun:06:00-Sun:09:00"
  max_allocated_storage         = "50"
  multi_az                      = false
  parameter_group_name          = "default.postgres13"
  port                          = 5432
  publicly_accessible           = false
  security_group_ids            = [aws_security_group.allow_db_communication.id]
  skip_final_snapshot           = false
  storage_encrypted             = true
  tags                          = var.default_tags
}

module "tf_eb" {
  source = "git@github.com:Shift3/terraform-modules.git//modules/aws/elastic-beanstalk"

  acm_certificate_arn                   = module.eb_acm.cert_arn
  allowed_subnets                       = data.aws_subnet_ids.default.ids
  application_name                      = local.app_name
  ec2_security_groups                   = [aws_security_group.allow_db_communication.id]
  eb_service_role                       = "arn:aws:iam::008036621198:role/aws-elasticbeanstalk-service-role"
  iam_instance_profile                  = "aws-elasticbeanstalk-ec2-role"
  max_size                              = "4"
  solution_stack                        = ""
  tags                                  = var.default_tags
  vpc_id                                = aws_default_vpc.default.id

  environment_variables                 = merge(
    {
      "DATABASE_URL" = "postgres://${local.database_connection_variables.DB_USER}:${local.database_connection_variables.DB_PASSWORD}@${split(":", module.rds_instance.host_name)[0]}:${local.database_connection_variables.DB_PORT}/${local.database_connection_variables.DB_NAME}",
      "S3_BUCKET" = var.s3_bucket_name,
      "EMAIL_DOMAIN" = trimsuffix(local.api_domain_name, "."),
    },
    var.eb_env_variables
  )
}

module "eb_route53_record" {
  source            = "git@github.com:Shift3/terraform-modules.git//modules/aws/route53"

  alias_dns_name    = module.tf_eb.dns_cname
  domain_name       = local.api_domain_name
  hosted_zone       = var.aws_route53_hosted_zone
  resource_zone_id  = module.tf_eb.hosted_zone_id
}

module "ses_through_domain_name" {
  source      = "git@github.com:Shift3/terraform-modules.git//modules/aws/ses"

  domain_name = local.api_domain_name
  hosted_zone = var.aws_route53_hosted_zone
}

module "s3" {
  source            = "git@github.com:Shift3/terraform-modules.git//modules/aws/s3-bucket?ref=boilerplate-experimentation"
  bucket_name       = var.s3_bucket_name
  bucket_acl        = "public-read"
  enable_versioning = false
  bucket_tags       = var.default_tags
  bucket_policy     = <<EOF
{
    "Version": "2008-10-17",
    "Statement": [
    {
        "Sid": "PublicReadForGetBucketObjects",
        "Effect": "Allow",
        "Principal": {
            "AWS": "*"
         },
         "Action": "s3:GetObject",
         "Resource": "arn:aws:s3:::${var.s3_bucket_name}/*"
    }]
}
EOF
}
