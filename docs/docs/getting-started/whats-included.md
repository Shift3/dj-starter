---
sidebar_position: 2
---

# What's Included?

The starter project is **Batteries Included**, meaning it comes with
lots of helpful feature preinstalled for you, to make your life as a
developer easier. What follows is a list of what we include and where to
find more information about them.

* [Django](https://www.djangoproject.com/) is the framework that we are
	building on top of. If you are unfamiliar with django, it has a
	great [tutorial](https://www.djangoproject.com/start/) to get you
	introduced to the basic concepts.
* [Django REST Framework](https://www.django-rest-framework.org/) (also
	known as DRF) specializes django to excel in serving a great API. It
	provides, serialization, authentication, and a browseable API that
	you can use in development to aid your API development experience.
* [djoser](https://djoser.readthedocs.io/en/latest/introduction.html)
	provides a set of Django REST Framework endpoints that give us token
	authentication, registration, invitation, activation, forgot
	password, and other handy API endpoints for free.
* [django-filter](https://django-filter.readthedocs.io/) integrated with
	DRF which provides us powerful filtering capabilities that our API
	endpoints can take advantage of.
* [easy_thumbnails](https://github.com/SmileyChris/easy-thumbnails)
	which can automatically thumbnail user uploaded image files for
	optimized display on the frontend.
* [djangorestframework-camel-case](https://github.com/vbabiy/djangorestframework-camel-case)
	ensure that the REST api we provide uses camelcase, even though it's
	django conventions to use snake case. This package allows us to use
	snake case in django and still interact with camel case (which is
	standard on the frontend)
* [Django Debug
	Toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/)
	which can be used in conjunction with the DRF Browsable API to get a
	deeper look at what SQL queries certain API endpoints are running,
	along with other helpful information in development.
* [Django Debug Toolbar - Mail
	Panel](https://github.com/scuml/django-mail-panel) for viewing
	emails "sent" in development while not actually sending emails while
	developing the software.
* [CircleCI Config](https://circleci.com/) for automatic testing and
	deployments to both staging and production

