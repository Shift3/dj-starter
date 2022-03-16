variable "application_name" {
  description = "Name of application that will appear in the AWS console. This is normally something like the projectname-server.An example may be ifg-server. Where ifg is the name of the project, and the server is the designation for the backend, ifg-api is also common."
}

variable "aws_assume_role_arn" {
  description = "AWS role in our devops sandbox account. This should only be changed when deploying to a non BWTC AWS account."
  default = "arn:aws:iam::008036621198:role/SuperDevAssumeRole"
}

variable "s3_bucket_name" {
  description = "Name of the S3 bucket used for public uploads."
}

variable "aws_profile" {
  description = "The AWS profile used to provision resources"
  default     = "shift3"
}

variable "aws_region" {
  description = "Specified region where your AWS resources will live. In general we use us-west-2 because it is a west coast region but cheaper than us-west-1 (California). This should not change unless your projects client is based somewhere else in the world."
  default = "us-west-2"
}

variable "aws_route53_subdomain" {
  description = "The subdomain to use, if not provided we use the application_name by default. A value of 'cool_custom_subdomain' would give you a full domain of cool_custom_subdomain.shift3sandbox.com"
  default = ""
}

variable "aws_route53_hosted_zone" {
  description = "Hosted Zone that will be used, this usually represents a domain name. This should not change until you are deploying the application to production."
  default = "shift3sandbox.com."
}

variable "default_tags" {
  description = "The values here will be passed to the cloud resources as tag meta data. This helps our team audit the resources in our cloud account."
  default     = {
    "ClientName"      = "" # Should be the name of your client (onboarding this will be BWTC)
    "Compliance"      = "" # None if your application does not have client like HIPPA or PCI
    "Developer"       = ""
    "Environment"     = "Staging" # Staging | Production | Dev
    "Organization"    = "" # The organization responsible for creation and maintenance
    "ProjectManager"  = "" # The PM on the project
    "ProjectName"     = ""
    "Purpose"         = "Web Server"
  }
}

variable "eb_env_variables" {
  description = "This variable will be an environment copy of your .env file. It should contain all the environment variables needed for your application to work"
  default     = {
    APPLICATION_NAME = "Bitwise Starter Project"
    AWS_REGION       = "us-west-2"
    CLIENT_URL       = ""
    ERROR_LOGS       = "/opt/node/app/server-logs"
    PORT             = "8000"
  }
}
