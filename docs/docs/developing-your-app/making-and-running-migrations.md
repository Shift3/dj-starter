# Making and Running Migrations

## Migrations

Django autogenerates migrations for you to match your database schema to
what you have defined in your model files. The important commands are:

```bash
# From within your docker container

$ ./manage.py makemigrations # generate a migration based on your models
$ ./manage.py migrate # applies any un-applied migrations
```

For more details on how Django handles migrations, see [the Django
migration
docs](https://docs.djangoproject.com/en/4.0/topics/migrations/)

