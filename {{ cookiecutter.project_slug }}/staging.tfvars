# Your application name should match the name of your project. The value
# here will be used to create the name of each resource in your cloud
# provider. The normal format is something like
# <project-name>-<client/server>
#
# Character limit will depend on what workspace you are in as we append
# the workspace string. Limit = (workspaceName - 26)
application_name = "{{ cookiecutter.project_slug|replace('_', '-') }}"
s3_bucket_name = "{{ cookiecutter.project_slug|replace('_', '-') }}-staging"
aws_route53_subdomain = "{{ cookiecutter.project_slug|replace('_', '-') }}-staging"

# These tag values here will be applied to most resources Terraform
# creates. This allows us to audit our AWS account and to better track
# projects on the account. These tags are also required in the BWTC AWS
# account when creating resources like EC2. A more in-depth explaination
# of why these tags are required can be found here:
#
# https://docs.google.com/document/d/1_jvxKkL-1XY1ROQAOjZwQxL6lIu15v3tQ363NDOfYUE/edit#heading=h.aw008srhgnz0
default_tags = {
  "ClientName"      = "{{ cookiecutter.client_name }}"
  "Compliance"      = "None"
  "Developer"       = "Internal Tooling Team"
  "Environment"     = "Staging"
  "Organization"    = "Bitwise"
  "ProjectManager"  = "ProjectManager"
  "ProjectName"     = "{{ cookiecutter.project_name }}"
  "Purpose"         = "Web Server"
}

# Define the environment variables required for your live environment.
eb_env_variables = {
  APPLICATION_NAME       = "{{ cookiecutter.project_name }}"
  AWS_REGION             = "us-west-2"
  CLIENT_URL             = "{{ cookiecutter.staging_client_url }}"
  PORT                   = "8000"
  DJANGO_SECRET_KEY      = "{{ random_ascii_string(32) }}"
  DJANGO_SETTINGS_MODULE = "{{ cookiecutter.project_slug }}.settings.staging"
  SEEDED_USER_EMAIL      = "{{ cookiecutter.admin_email }}"
  NEW_RELIC_ENVIRONMENT  = "staging"
}
