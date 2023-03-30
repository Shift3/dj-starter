# Provisioning Infrastructure

The DJ Starter Project is designed to easily be deployed to AWS. We
provide files that easily allow you to spin up the AWS infrastructure
necessary to deploy the application.

## Prerequisites

The following tools must be installed to be able to provision AWS
infrastructure. Please note that if you used our
[laptop](https://github.com/shift3/laptop) script to setup your
computer, you likely have these tools installed already.

* [Terraform](https://www.terraform.io/) for managing infrastructure and
	provisioning it.
* [AWS Cli](https://aws.amazon.com/cli/) for storing your AWS
	credentials for terraform to use.

## Quick Start

In order to start provisioning your infrastructure we need to initialize
terraform. Before getting started, make sure you have AWS cli installed
and the `shift3` profile configured.

```bash	
$ aws configure sso --profile shift3

SSO session name (Recommended): shift3
SSO start URL [None]: https://bitwiseindustries.awsapps.com/start
SSO region [None]: us-west-2
SSO registration scopes [sso:account:access]: (press Enter)
```
To test this out: 

To use this profile, specify the profile name using --profile, as shown:

`aws s3 ls --profile shift3`

Once we have the shift3 profile configured we need to initialize
terraform. This is the first command that should be runl after writing a
new Terraform configuration or cloning an existing one from version
control. It is safe to run this command multiple times.


```bash
terraform init
```

Next we need to create a staging workspace. Workspaces allow you to
manage multiple sets of infrastructure. Commonly we use staging and
prod. This project provides a staging setup out of the box, so lets set
up our staging servers.

```bash
terraform workspace new staging
```

Now we can preview the infrastructure terraform will want to spin up by
using the `plan` command.

```bash
terraform plan -var-file=$(terraform workspace show).tfvars
```

Finally, if the plan looks good, we can tell terraform to apply the plan
and provision **actual infrastructure**

```bash
terraform apply -var-file=$(terraform workspace show).tfvars
```

## Updating Staging or Prod Infrastructure

First make sure you are on the correct workspace that you want to
update.

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
