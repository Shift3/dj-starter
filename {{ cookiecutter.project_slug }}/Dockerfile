FROM python:3.10
ENV PYTHONUNBUFFERED 1

WORKDIR /code/

# Allows docker to cache installed dependencies between builds
COPY ./requirements requirements
RUN pip install -r requirements/dev.txt

# Install gettext in order to use Django's Translation system for internationalization support
RUN apt-get update && apt-get install gettext -y

# Adds our application code to the image
WORKDIR /code/app
COPY . /code/app

EXPOSE 8000
