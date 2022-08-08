---
sidebar_position: 1
---

# Getting Up and Running

The Bitwise DJ Starter project is powered by
[Cookiecutter](https://github.com/cookiecutter/cookiecutter), and is a a
production ready, batteries included, starter project based on
[Django](https://www.djangoproject.com/), that gives you a head-start on
client projects. Designed for use at Bitwise Tech Consulting.

We include an API explorer, authentication, authorization, pagination,
change tracking, comprehensive filters, and more features that make
development a breeze.

For a live demo, you can check out the frontend [staging
site](https://boilerplate-client-react.shift3sandbox.com).

## Project Requirements

[Docker](https://docs.docker.com/get-started/overview/) is used for running
the server after you have generated your project. If you are using our [laptop
setup script](https://github.com/shift3/laptop) then this should already be
installed for you.

## Quick Start

It's easy to generate out your own project. Simply install cookiecutter.
```bash
pip install --user cookiecutter
```

And run the cookiecutter generator
```bash
cookiecutter gh:Shift3/dj-starter
```

The generator will prompt you for a few details about your project, once done, it will create a django project for you in a directory named whatever you choose as the `project_slug`.

### After Generation

From within the generated project directory. You can start developing
your application.


Start the dev server for local development:

```bash
docker-compose up
```

You can now visit [http://localhost:8000/](http://localhost:8000) to view the
browsable api.

Enter the docker container (while the server is running), migrate, and create a
user for yourself:

```bash
# Enters a shell in the docker container
docker compose exec web bash

# And create a superuser for yourself.
$ ./manage.py createsuperuser
```


