#!/bin/sh

set -e

./manage.py migrate --noinput
./manage.py collectstatic --noinput

# Creates an Admin user with a random password with the email specified
# in settings.SEEDED_USER_EMAIL
./manage.py createsu

# Run the server using gunicorn
newrelic-admin run-program gunicorn --bind 0.0.0.0:$PORT --access-logfile - {{ cookiecutter.project_slug }}.wsgi:application
