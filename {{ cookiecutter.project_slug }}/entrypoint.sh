#!/bin/sh

set -e

./manage.py migrate --noinput
./manage.py collectstatic --noinput
newrelic-admin run-program gunicorn --bind 0.0.0.0:$PORT --access-logfile - {{ cookiecutter.project_slug }}.wsgi:application
