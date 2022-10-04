# Cookiecutter Bitwise Django Starter Project

Powered by [Cookiecutter](https://github.com/cookiecutter/cookiecutter), this project is a a production ready, batteries included, starter project based on [Django](https://www.djangoproject.com/), that gives you a head-start on client projects. Designed for use at Bitwise Tech Consulting.

We include an API explorer, authentication, authorization, pagination, change tracking, comprehensive filters, and more features that make development a breeze.

For a live demo, you can check out the frontend [staging site](https://boilerplate-client-react.shift3sandbox.com).

[![asciicast](https://asciinema.org/a/BxSb6BFQPei4Q9sRkTSNfYbwP.svg)](https://asciinema.org/a/BxSb6BFQPei4Q9sRkTSNfYbwP)

## Prerequisites

* [Python](https://www.python.org/) for installing cookiecutter and generating out the project.

## Quickstart

It's easy to generate out your own project. Simply install cookiecutter.
```bash
pip install --user cookiecutter
```

And run the cookiecutter generator
```bash
cookiecutter gh:Shift3/dj-starter
```

The generator will prompt you for a few details about your project, once done, it will create a django project for you in a directory named whatever you choose as the `project_slug`. After generation, view the `README.md` for instructions on how to develop and deploy the project.

Be sure to get this pushed up to a `Shift3` repository by creating a repository on our github org and following the instructions.

## The Batteries

The starter project is **Batteries Included**, meaning it comes with lots of helpful feature preinstalled for you, to make your life as a developer easier. What follows is a list of what we include and where to find more information about them.

* [Django](https://www.djangoproject.com/) is the framework that we are building on top of. If you are unfamiliar with django, it has a great [tutorial](https://www.djangoproject.com/start/) to get you introduced to the basic concepts.
* [Django REST Framework](https://www.django-rest-framework.org/) (also known as DRF) specializes django to excel in serving a great API. It provides, serialization, authentication, and a browseable API that you can use in development to aid your API development experience.
* [djoser](https://djoser.readthedocs.io/en/latest/introduction.html) provides a set of Django REST Framework endpoints that give us token authentication, registration, invitation, activation, forgot password, and other handy API endpoints for free.
* [django-filter](https://django-filter.readthedocs.io/) integrated with DRF which provides us powerful filtering capabilities that our API endpoints can take advantage of.
* [easy_thumbnails](https://github.com/SmileyChris/easy-thumbnails) which can automatically thumbnail user uploaded image files for optimized display on the frontend.
* [djangorestframework-camel-case](https://github.com/vbabiy/djangorestframework-camel-case) ensure that the REST api we provide uses camelcase, even though it's django conventions to use snake case. This package allows us to use snake case in django and still interact with camel case (which is standard on the frontend)
* [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/) which can be used in conjunction with the DRF Browsable API to get a deeper look at what SQL queries certain API endpoints are running, along with other helpful information in development.
* [Mailhog](https://github.com/mailhog/MailHog) for viewing emails "sent" in development while not actually sending emails while developing the software.
* [CircleCI Config](https://circleci.com/) for automatic testing and deployments to both staging and production

## Optional Features

During generation, you will be able to select optional features to be
included. Currently we have a single optional feature:

### Notifications (In-App, Email, and Text)

Enable this feature during generation if you want to be able to send
notifications to users of the web application. Enabling this feature
allows you to define notification types and send them easily.

Notifications are sent via
[SSE](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events),
which is a somewhat newer technology that allows you to push events
directly to consuming clients.

We include an example notification.

```python
class AgentCreatedNotification(BaseNotification):
    backends = [DatabaseBackend, EmailBackend, SMSBackend]

    def as_database(self, user):
        agent = Agent.objects.get(pk=self.context["agent_id"])
        created_by = User.objects.get(pk=self.context["user_id"])

        return {
            "agent_name": agent.name,
            "user_name": created_by.full_name(),
            **self.context
        }

    def as_email(self, user):
        return BaseEmailMessage(
            subject="A new agent has been created",
            template_name="notifications/agent_created_notification_email.html",
            context={
                "user": user,
                "agent": Agent.objects.get(pk=self.context["agent_id"]),
                "created_by": User.objects.get(pk=self.context["user_id"]),
            },
        )

    def as_sms(self, user):
        created_by = User.objects.get(pk=self.context["user_id"])
        return "Hello {}. A new agent has been created by {}" % (
            user.full_name(), created_by.full_name()
        )
```

which is sent like so:

```python
Notification.send(
    AgentCreatedNotification({
        "agent_id": instance.id,
        "user_id": "example"
    }),
    User.objects.filter(role=User.ADMIN) # list of users to send the notifications to
)
```
