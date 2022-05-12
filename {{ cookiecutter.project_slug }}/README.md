# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## Project Requirements

### Development Requirements
* [Docker](https://docs.docker.com/get-started/overview/) and [Docker Compose](https://docs.docker.com/compose/) for an easy to use and reproducible development environment.

### Deployment Requirements

* [Terraform](https://www.terraform.io/) for managing infrastructure and provisioning it.
* [AWS Cli](https://aws.amazon.com/cli/) for storing your AWS credentials for terraform to use.

## Quickstart

Start the dev server for local development:
```bash
docker-compose up
```

Enter the docker container (while the server is running), migrate, and create a user for yourself:
```bash
# Enters a shell in the docker container
docker-compose exec web bash

# And create a superuser for yourself.
$ ./manage.py createsuperuser
```

Optionally run the tests from within the docker container at anytime:
```bash
# From within docker container
$ pytest
```

> Make sure you store the credentials files `staging.tfvars` in a secure location (as it is not committed to the repository). Internally we use [Zoho Vault](https://www.zoho.com/vault) for secure credential storage.

## The Batteries

The starter project is **Batteries Included**, meaning it comes with lots of helpful feature preinstalled for you, to make your life as a developer easier. What follows is a list of what we include and where to find more information about them.

* [Django](https://www.djangoproject.com/) is the framework that we are building on top of. If you are unfamiliar with django, it has a great [tutorial](https://www.djangoproject.com/start/) to get you introduced to the basic concepts.
* [Django REST Framework](https://www.django-rest-framework.org/) (also known as DRF) specializes django to excel in serving a great API. It provides serialization, authentication, and a browseable API that you can use in development to aid your API development experience.
* [djoser](https://djoser.readthedocs.io/en/latest/introduction.html) provides a set of Django REST Framework endpoints that give us token authentication, registration, invitation, activation, forgot password, and other handy API endpoints for free.
* [django-filter](https://django-filter.readthedocs.io/) integrated with DRF which provides us powerful filtering capabilities that our API endpoints can take advantage of.
* [easy_thumbnails](https://github.com/SmileyChris/easy-thumbnails) which can automatically thumbnail user uploaded image files for optimized display on the frontend.
* [djangorestframework-camel-case](https://github.com/vbabiy/djangorestframework-camel-case) ensure that the REST api we provide uses camelcase, even though it's django conventions to use snake case. This package allows us to use snake case in django and still interact with camel case (which is standard on the frontend)
* [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/) which can be used in conjunction with the DRF Browsable API to get a deeper look at what SQL queries certain API endpoints are running, along with other helpful information in development.
* [Django Debug Toolbar - Mail Panel](https://github.com/scuml/django-mail-panel) for viewing emails "sent" in development while not actually sending emails while developing the software.
* [CircleCI Config](https://circleci.com/) for automatic testing and deployments to both staging and production

## Development Process

What follows is a short summary of what the day to day will look like working in this starter project. For more detailed information on the main components, the [Django documentation](https://docs.djangoproject.com/en/4.0/) and [Django REST Framework](https://www.django-rest-framework.org/) documentation will be a source of more in depth answers to questions.

### The Django REST Framework Browsable API

Django REST Framework provides a great browsable API that lets you easily utilize your API without a frontend, and without using something like Postman. You can authenticate with it to log in, and browse the API making any kind of API request your API allows.

![Logging in.](docs/01-browsable-api.png)
![The different components of the browsable API](docs/02-browsable-api.png)

The debug toolbar also integrates well with this browsable API. The most useful functions of the debug tools are being able to see SQL queries that request made, the raw request information, as well as being able to see any mail that was sent.

![Debug Toolbar](docs/03-browsable-api-debug-toolbar.png)

For more information about Django REST Framework, see the [DRF docs](https://www.django-rest-framework.org/)

### Models

A model is the single, definitive source of information about your data. Your models define what the structure of your database looks like. A typical model looks something like this:

```python
class MyCoolModel(TimeStampedModel, models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField()
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True, blank=True)
```

After you make changes to your models you need to tell Django to update your database to match your models.

For more details on Django models, see [the Django model docs](https://docs.djangoproject.com/en/4.0/topics/db/models/)

### Migrations

Django autogenerates migrations for you to match your database schema to what you have defined in your model files. The important commands are:

```bash
# From within your docker container

$ ./manage.py makemigrations # generate a migration based on your models
$ ./manage.py migrate # applies any un-applied migrations
```

For more details on how Django handles migrations, see [the Django migration docs](https://docs.djangoproject.com/en/4.0/topics/migrations/)

## Provisioning Infrastructure


### Quickstart

In order to start provisioning your infrastructure we need to initialize terraform. Before getting started, make sure you have AWS cli installed and the `shift3` profile configured.

```bash	
aws configure --profile shift3
```

Once we have the shift3 profile configured we need to initialize terraform. This is the first command that should be runl after writing a new Terraform configuration or cloning an existing one from version control. It is safe to run this command multiple times.


```bash
terraform init
```

Next we need to create a staging workspace. Workspaces allow you to manage multiple sets of infrastructure. Commonly we use staging and production. This project provides a staging setup out of the box, so lets set up our staging servers.

```bash
terraform workspace new staging
```

Now we can preview the infrastructure terraform will want to spin up by using the `plan` command.

```bash
terraform plan -var-file=$(terraform workspace show).tfvars
```

Finally, if the plan looks good, we can tell terraform to apply the plan and provision **actual infrastructure**

```bash
terraform apply -var-file=$(terraform workspace show).tfvars
```


### Updating staging or production infrastructure

First make sure you are on the correct workspace that you want to update.

```bash
# Check current workspaces
terraform workspace list

# If we need to change workspaces
terraform workspace select <desired-workspace>
```

Simply make your modifications and run `plan` and `apply` again.

```bash
# Preview the changes to be made.
terraform plan -var-file=$(terraform workspace show).tfvars

# Look good? Apply the changes to your infrastructure
terraform apply -var-file=$(terraform workspace show).tfvars
```


## Deploying your Application

Applications are **deployed automatically** by CircleCI when commits are pushed to `develop` or `main`. Make sure CircleCI is setup on your project.

* Commits to the `develop`  branch are automatically deployed to the **Staging** environment.
* Commits to the `main`  branch are automatically deployed to the **Production** environment.

### Settings up CircleCI Environment Variables

In order for automatic deploys to work, your CircleCI must be setup with the correct environment variables. 

#### The easy way

We include a script that pulls the necessary environment variables from your terraform state, and uploads them to CircleCI for you. In order to run it, you will need to have already provisioned your terraform infrastructure, [setup the project on CircleCI](https://app.circleci.com/projects/project-dashboard/github/Shift3/), and [created a CircleCI API token](https://app.circleci.com/settings/user/tokens).

```bash
CIRCLECI_TOKEN=my-api-token PROJECT_NAME=my-project scripts/update-circleci.sh
```

Depending on your current **terraform workspace** the script will show you what environment variables you will need, and will ask you if it's ok to set them on CircleCI. 

After the script works, you can make a push to `develop` for staging, or `main` for production, to start a deploy process and make sure everything works.

#### The manual way

The following environment variables are required to be set within the CircleCI Project Settings. Descriptions (and example values) of the environment variables follow:

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

### Deploying to Production

Production deploys from the `main` branch, and uses the same set of environment variables as staging just with `PRODUCTION` instead of `STAGING` in the names. The list of those variables follow:

* `PRODUCTION_AWS_ACCESS_KEY_ID`
* `PRODUCTION_AWS_SECRET_ACCESS_KEY`
* `PRODUCTION_AWS_DEFAULT_REGION`
* `PRODUCTION_AWS_ECR_ACCOUNT_URL`
* `PRODUCTION_AWS_ECR_REPO_NAME`
* `PRODUCTION_EB_ENVIRONMENT_NAME`
* `PRODUCTION_EB_APPLICATION_NAME`
* `PRODUCTION_AWS_ROLE_ARN` (optional)
