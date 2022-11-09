#!/bin/sh

set -e

./manage.py migrate --noinput
./manage.py collectstatic --noinput

# Creates an Admin user with a random password with the email specified
# in settings.SEEDED_USER_EMAIL
./manage.py createsu

# Compiles the translation files (.po) and generates their .mo counterparts
./manage.py compilemessages

# Run server and any workers
honcho start -f Procfile.prod
