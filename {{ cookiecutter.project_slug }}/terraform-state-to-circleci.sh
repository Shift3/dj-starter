#!/bin/sh

# How do we want to handle these env vars?
# PROJECT_NAME                          my-project
# STAGING_AWS_ACCESS_KEY_ID             AKIAIOSFODNN7EXAMPLE
# STAGING_AWS_SECRET_ACCESS_KEY         wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
# STAGING_AWS_DEFAULT_REGION            us-west-2

set -e

prefix=''

tf_workspace=$(terraform workspace show)
case $tf_workspace in
	staging)
		prefix='STAGING_'
		;;
	production)
		prefix='PRODUCTION_'
		;;
	*)
		;;
esac


json=$(terraform show -json)
ecr_repo_name=$(printf "%s" "$json" | jq -r '.. | select(.type? == "aws_ecr_repository") | .values.name')
ecr_repo_url=$(printf "%s" "$json" | jq -r '.. | select(.type? == "aws_ecr_repository") | .values.repository_url' | cut -d '/' -f 1)
eb_app=$(printf "%s" "$json" | jq -r '.. | select(.type? == "aws_elastic_beanstalk_application") | .values.name')
eb_env=$(printf "%s" "$json" | jq -r '.. | select(.type? == "aws_elastic_beanstalk_environment") | .values.name')

echo "In terraform workspace          $tf_workspace"
echo
echo "${prefix}EB_APPLICATION_NAME    $eb_app"
echo "${prefix}EB_ENVIRONMENT_NAME    $eb_env"
echo "${prefix}AWS_ECR_REPO_NAME      $ecr_repo_name"
echo "${prefix}AWS_ECR_ACCOUNT_URL    $ecr_repo_url"

# TODO: set environment variables to circleci after confirmation.
