#!/bin/sh

set -e

if [ -z "$(command -v jq)" ]; then
	echo 'jq must be installed. If you are on mac, you can install it with:'
	echo 'brew install jq'
	exit 1
fi

if [ -z "$(command -v terraform)" ]; then
	echo 'terraform must be installed. If you are on mac, you can install it with:'
	echo 'brew install terraform'
	exit 1
fi

if [ -z "$CIRCLECI_TOKEN" ] || [ -z "$PROJECT_NAME" ]; then
	echo 'Usage: CIRCLECI_TOKEN=your-personal-cirlceci-api-token PROJECT_NAME=your-project-name ./update_cirleci.sh'
	echo
	echo 'To get a CircleCI API token, visit https://app.circleci.com/settings/user/tokens and create a new token.'
	echo 'Your project name should also match that project name in CircleCI'
	exit 1
fi

update_circleci_variable() {
	env_name=$1
	env_value=$2

	data="{\"name\":\"$env_name\",\"value\":\"$env_value\"}"
	curl -s -o /dev/null --show-error --fail --request POST \
	  --url "https://circleci.com/api/v2/project/gh/Shift3/$PROJECT_NAME/envvar" \
	  --header "Circle-Token: $CIRCLECI_TOKEN" \
	  --header 'content-type: application/json' \
	  --data "$data"
}


prefix=''
tf_workspace=$(terraform workspace show)
case $tf_workspace in
	staging)
		prefix='STAGING_'
		;;
	prod)
		prefix='PRODUCTION_'
		;;
	*)
		;;
esac


json=$(terraform show -json)
ecr_repo_name=$(printf "%s" "$json" | \
	jq -r '.. | select(.type? == "aws_ecr_repository") | .values.name')
ecr_repo_url=$(printf "%s" "$json" | \
	jq -r '.. | select(.type? == "aws_ecr_repository") | .values.repository_url' | cut -d '/' -f 1)
eb_app=$(printf "%s" "$json" | \
	jq -r '.. | select(.type? == "aws_elastic_beanstalk_application") | .values.name')
eb_env=$(printf "%s" "$json" | \
	jq -r '.. | select(.type? == "aws_elastic_beanstalk_environment") | .values.name')


echo "In terraform workspace:"
echo "$tf_workspace"
echo

echo 'CircleCI also needs a AWS key pair to deploy with.'
printf "Enter value for %sAWS_ACCESS_KEY_ID (enter to skip): " $prefix
read -r aws_access_key
printf "Enter value for %sAWS_SECRET_ACCESS_KEY (enter to skip): " $prefix
read -r aws_secret_key


env_vars=$(cat <<- EOF
PROJECT_NAME  $PROJECT_NAME
${prefix}AWS_DEFAULT_REGION  us-west-2
${prefix}EB_APPLICATION_NAME  $eb_app
${prefix}EB_ENVIRONMENT_NAME  $eb_env
${prefix}AWS_ECR_REPO_NAME  $ecr_repo_name
${prefix}AWS_ECR_ACCOUNT_URL  $ecr_repo_url
${prefix}AWS_ROLE_ARN  arn:aws:iam::008036621198:role/SuperDevAssumeRole
EOF
)

if [ -n "$aws_access_key" ]; then
	env_vars=$(cat <<-EOF
$env_vars
${prefix}AWS_ACCESS_KEY_ID  $aws_access_key
EOF
)
fi

if [ -n "$aws_secret_key" ]; then
	env_vars=$(cat <<-EOF
$env_vars
${prefix}AWS_SECRET_ACCESS_KEY  $aws_secret_key
EOF
)
fi


echo "Want to set the following environment variables:"
printf "%s\n" "$env_vars" | column -t
echo
printf "Would you like to update CircleCI project '%s' with these settings? [y/n] " "$PROJECT_NAME"
read -r answer


case $answer in
	y)
		echo 'Updating CircleCI...'
		update_circleci_variable "PROJECT_NAME" "$PROJECT_NAME"
		update_circleci_variable "${prefix}AWS_DEFAULT_REGION" "us-west-2"
		update_circleci_variable "${prefix}EB_APPLICATION_NAME" "$eb_app"
		update_circleci_variable "${prefix}EB_ENVIRONMENT_NAME" "$eb_env"
		update_circleci_variable "${prefix}AWS_ECR_REPO_NAME" "$ecr_repo_name"
		update_circleci_variable "${prefix}AWS_ECR_ACCOUNT_URL" "$ecr_repo_url"
		update_circleci_variable "${prefix}AWS_ROLE_ARN" "arn:aws:iam::008036621198:role/SuperDevAssumeRole"
		if [ -n "$aws_access_key" ]; then
			update_circleci_variable "${prefix}AWS_ACCESS_KEY_ID" "$aws_access_key"
		fi
		if [ -n "$aws_secret_key" ]; then
			update_circleci_variable "${prefix}AWS_SECRET_ACCESS_KEY" "$aws_secret_key"
		fi

		echo 'Done!'
		;;
	n)
		echo 'No changes have been made'
		exit
		;;
	*)
		echo 'No changes have been made'
		exit
		;;
esac

