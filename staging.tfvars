# Your application name should match the name of your project. The value here will be used to create the name of each resource in your cloud provider. The normal format is something like <project-name>-<client/server>
# Character limit will depend on what workspace you are in as we append the workspace string. Limit = (workspaceName - 26)
application_name = "dj-starter"
s3_bucket_name = "dj-starter-staging"
aws_route53_subdomain = "dj-starter-staging"

# These tag values here will be applied to most resources Terraform creates. This allows us to audit our AWS account and to better track projects on the account. These tags are also required in the BWTC AWS account when creating resources like EC2. A more in-depth explaination of why these tags are required can be found here:
# https://docs.google.com/document/d/1_jvxKkL-1XY1ROQAOjZwQxL6lIu15v3tQ363NDOfYUE/edit#heading=h.aw008srhgnz0
default_tags = {
  "ClientName"      = "Internal"
  "Compliance"      = "None"
  "Developer"       = "Boilerplate Team"
  "Environment"     = "Staging"
  "Organization"    = "Bitwise"
  "ProjectManager"  = "Internal"
  "ProjectName"     = "Django Boilerplate"
  "Purpose"         = "Web Server"
}

# This should match your .env file but represent the vaules your application would need for a live environment.
eb_env_variables = {
  APPLICATION_NAME     = "Bitwise Starter Project"
  AWS_REGION           = "us-west-2"
  CLIENT_URL           = "https://react-dj-staging.shift3sandbox.com"
  PORT                 = "8000"
  DJANGO_SECRET_KEY    = "!w_s8q_+q4a7%-ae(_shx!3%q*6c6pfv6#$0(hmvelwv$9e6_"
  DJANGO_SETTINGS_MODULE = "boilerplate.settings.production"

}
