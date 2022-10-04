# Deploying to AWS

The Django Starter Project comes with a complete CircleCI configuration,
as well as some useful scripts that make deployment a breeze. The
project is designed to be deployed automatically via CircleCI.

## Setup CircleCI

Applications are **deployed automatically** by CircleCI when commits are
pushed to `develop` or `main`. Make sure CircleCI is setup on your
project by visiting the [CircleCI
dashboard](https://circleci.com/vcs-authorize/) for your project.

* Commits to the `develop`  branch are automatically deployed to the
    **Staging** environment.
* Commits to the `main`  branch are automatically deployed to the
    **Production** environment.

## Set CircleCI Environment Variables

In order for automatic deploys to work, your CircleCI must be setup with
the correct environment variables. 

### The easy way

We include a script that pulls the necessary environment variables from
your terraform state, and uploads them to CircleCI for you. In order to
run it, you will need to have already provisioned your terraform
infrastructure, [setup the project on
CircleCI](https://app.circleci.com/projects/project-dashboard/github/Shift3/),
and [created a CircleCI API
token](https://app.circleci.com/settings/user/tokens). Once your have
retrieved your CircleCI API token, simply run the following command,
replacing the values for `CIRCLECI_TOKEN` and `PROJECT_NAME` with your
own.

```bash
CIRCLECI_TOKEN=my-api-token PROJECT_NAME=my-project scripts/update-circleci.sh
```

Depending on your current **terraform workspace** the script will show
you what environment variables you will need, and will ask you if it's
ok to set them on CircleCI. 

After the script works, you can make a push to `develop` for staging, or
`main` for production, to start a deploy process and make sure
everything works.

### The manual way

The following environment variables are required to be set within the
CircleCI Project Settings. Descriptions (and example values) of the
environment variables follow:

* `PROJECT_NAME`
  - The name of your project. This variable will be used to tag your docker image file. A safe name would be to use the same name as your git repository. Cannot contain spaces.
  - `my-project`
* `STAGING_AWS_ACCESS_KEY_ID`
  - The AWS access key ID used to authenticate with AWS.
  - `AKIAIOSFODNN7EXAMPLE`
* `STAGING_AWS_SECRET_ACCESS_KEY`
  - The AWS secret key used to authenticate with AWS.
  - `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`
* `STAGING_AWS_DEFAULT_REGION`
  - The default region your infrastructure is deployed to.
  - `us-west-2`
* `STAGING_AWS_ECR_ACCOUNT_URL`
  - The ECR (Elastic Container Repository) account url. This will be used to store the docker images that are built for production and staging.
  - `012345678901.dkr.ecr.us-west-2.amazonaws.com`
* `STAGING_AWS_ECR_REPO_NAME`
  - The ECR repository name, this can be found in the AWS console.
  - `my-project-ecr-repo`
* `STAGING_EB_ENVIRONMENT_NAME`
  - The EB (Elastic Beanstalk) environment name, this can be found in the AWS console.
  - `my-project-api-webserver`
* `STAGING_EB_APPLICATION_NAME`
  - The EB application name, this can be found in the AWS console.
  - `my-project`
* `STAGING_AWS_ROLE_ARN`
  - When using [AWS AssumeRole](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html) (as bitwise does for AWS infastructure in our accounts). You must set this environment variable. When deploying to infrastructure outside of bitwise infrastructure, this variable is optional. The example value is the value you should use on bitwise infrastructure.
  - `arn:aws:iam::008036621198:role/SuperDevAssumeRole`

Once all of these are setup, commits to the `develop` branch should automatically deploy to your staging infrastructure. For more details on the deployment process, or if you need to customize it to fit your needs, check out the [`.cirleci/config.yml`](.circleci/config.yml) file.

## Deploying to Production

Production deploys from the `main` branch, and uses the same set of environment variables as staging just with `PRODUCTION` instead of `STAGING` in the names. The list of those variables follow:

* `PRODUCTION_AWS_ACCESS_KEY_ID`
* `PRODUCTION_AWS_SECRET_ACCESS_KEY`
* `PRODUCTION_AWS_DEFAULT_REGION`
* `PRODUCTION_AWS_ECR_ACCOUNT_URL`
* `PRODUCTION_AWS_ECR_REPO_NAME`
* `PRODUCTION_EB_ENVIRONMENT_NAME`
* `PRODUCTION_EB_APPLICATION_NAME`
* `PRODUCTION_AWS_ROLE_ARN` (optional)
