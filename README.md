# Cookiecutter Bitwise Django Starter Project

Powered by [Cookiecutter](https://github.com/cookiecutter/cookiecutter), this project is a a production ready, batteries included, starter project based on [Django](https://www.djangoproject.com/), that gives you a head-start on client projects. Designed for use at Bitwise Tech Consulting.

We include an API explorer, authentication, authorization, pagination, change tracking, comprehensive filters, and more features that make development a breeze.

For a live demo, you can check out the [staging site](https://react-dj-staging.shift3sandbox.com).

## Prerequisites

### Development Requirements
* [Python](https://www.python.org/) for installing cookiecutter and generating out the project.
* [Docker](https://docs.docker.com/get-started/overview/) and [Docker Compose](https://docs.docker.com/compose/) for an easy to use and reproducible development environment.

### Deployment Requirements
* [Terraform](https://www.terraform.io/) for managing AWS infrastructure and provisioning it.

## Quickstart

It's easy to generate out your own project. Simply install cookiecutter.
```bash
pip install --user cookiecutter
```

And run the cookiecutter generator
```bash
cookiecutter gh:Shift3/dj-starter
```

The generator will prompt you for a few details about your project, once done, it will create a django project for you in a directory named whatever you choose as the `project_slug`

### Quickstart on the Generated Project

Make sure you are in the generated project directory and start the dev server for local development:
```bash
docker-compose up
```

Enter the docker container (while the server is running), migrate, and create a user for yourself:
```bash
# Enters a shell in the docker container
docker-compose run exec web bash

# And create a superuser for yourself.
$ ./manage.py createsuperuser
```

Optinally run the tests from within the docker container at anytime:
```bash
# From within docker container
$ pytest
```

## The Batteries

The starter project is **Batteries Included**, meaning it comes with lots of helpful feature preinstalled for you, to make your life as a developer easier. What follows is a list of what we include and where to find more information about them.

* [Django](https://www.djangoproject.com/) is the framework that we are building on top of. If you are unfamiliar with django, it has a great [tutorial](https://www.djangoproject.com/start/) to get you introduced to the basic concepts.
* [Django REST Framework](https://www.django-rest-framework.org/) (also known as DRF) specializes django to excel in serving a great API. It provides, serialization, authentication, and a browseable API that you can use in development to aid your API development experience.
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

## Provisioning the AWS Infrastructure

### Setting Up Your Remote State

Terraform will keep a copy of the infrastructure it creates in a state file. This file is basically a snapshot of what has been generated by your `.tf` files. In order to keep everyone on the project in sync, this boilerplate comes with remote state built in. The state file itself will be stored in an S3 bucket, so that any changes made can be referenced by everyone on the project. Before doing **ANYTHING** else with Terraform you will need to setup the folder your state will be stored in.

In the root directory, look for the `main.tf` file. Near the top, there should be a block that looks something like this:

```
terraform {
  backend "s3" {
    bucket  = "shift3-terraform-state"
    key     = "<project-name>/<environment>/terraform.tfstate"
    region  = "us-west-2"
    profile = "shift3"
  }
}
```

This block sets up the remote state for your project!

Replace `<project-name>` with the name of your project, and `<environment>` with the environment for your deployment (staging | production). Once this is done, you can then move forward with setting up your projects variables to begin deployment!

### What are workspaces?

Workspaces are the new way we manage infrastructure instead of using directories. A workspace contains everything
Terraform needs to manage a given collection of infrastructure. You can read more about it [here](https://www.terraform.io/docs/language/state/workspaces.html)

### Setting up Staging and Production workspace

Run `terraform init` to initialize the remote state for terraform.

Before we do anything, lets make sure we only have one workspace (`default`)

Run `terraform workspace list` and `default` should be starred.

Now that we made sure that there is only one workspace. Lets create the Staging and Production workspace\
Run `terraform workspace new staging` and press enter\
Run `terraform workspace new production` and press enter

Now if you run `terraform workspace list` you'll see that the last workspace you created (`production`) will be starred. The star means that is your *current* workspace.

### Switching between workspaces
Example: 3 environments, default, staging and production.

1. Know what workspace you are currently in by doing: `terraform workspace list` the `*` is your current workspace
```
* default
  staging
  production
```
2. Switch workspaces by doing `terraform workspace select (environment name)`

### Provisioning the staging or production infrastructure
When the staging/production environment needs to be provisioned, lets make sure that we are in the correct workspace by doing `terraform workspace list` and the star is next to `staging` or `production`.

```
  default
* staging
  production
```

Now that we have confirmed our workspace, lets fill in! Currently, we have an `example.tfvars` that shows what values are needed to be filled in. Because we have two environments, we will need to create a `staging.tfvars` and `production.tfvars` at the root directory. Depending on what environment you are currently in (staging/production) will dictate what `.tfvars` file will be used when provisioning. For example if working in `staging environment`, fill out `staging.tfvars`, if `production environment`, fill out `production.tfvars`.

Once the variables are filled out. Lets create the infrastructure!

### Provisioning the staging or production infrastructure
To apply the infrastructure, let make sure again we are in the correct
workspace `terraform workspace list` and `staging` or `production`
should be starred (depending on what environment we are deploying)<br/>

To apply:
1. `terraform plan -var-file $(terraform workspace show).tfvars`
2. `terraform apply -var-file $(terraform workspace show).tfvars`

The output of running terraform plan (if everything is correct) is the following. Note that what to `add`, `change`, `destroy` changes as you change the infrastructure.
```
Plan:  to add,  to change,  to destroy.
```
The output of running terraform apply is

```
  Do you want to perform these actions in workspace "(workspace env)"?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.
```

### How can we update staging or production after they are provisioned?

Just as always, make sure you are in the correct workspace before you do any updates/changes.

Then you can run `terraform plan -var-file $(terraform workspace show).tfvars` and `terraform apply $(terraform workspace show).tfvars` to see and apply the changes to the already provisioned infrastructure.


## Deploying your Application

Applications are **deployed automatically** by CircleCI when commits are pushed to `develop` or `main`. Make sure CircleCI is setup on your project.

* Commits to the `develop`  branch are automatically deployed to the **Staging** environment.
* Commits to the `main`  branch are automatically deployed to the **Production** environment.

### Settings up CircleCI Environment Variables

In order for automatic deploys to work, your CircleCI must be setup with the correct environment variables. The following environment variables are required to be set within the CircleCI Project Settings. Descriptions (and example values) of the environment variables follow:

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
