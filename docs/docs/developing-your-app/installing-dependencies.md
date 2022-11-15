# Installing Dependencies

## Intro

For dependency management we simply use `pip` from within the docker
container.

There is a `requirements/` directory that contains dependency lists for
`dev, test, staging, prod` as well as a `base` dependency list that is
included by all the environments.

## Adding a Dependency

To add a new dependency to the project, first install it with pip.

```bash
pip install some_new_dependency
```

And then to get the version that you need to put in the requirements
files, run:

```bash
pip freeze | grep some_new_dependency

# should output something like this:
# some_new_dependency==1.2.3
```

Then simply place that line into the relevent requirements file.
* `requirements/base.txt` for dependencies that installed in all
	environments.
* `requirements/dev.txt` for development only dependencies.
* `requirements/{staging,prod}.txt` for staging/prod only dependencies.
* `requirements/test.txt` for testing only dependencies.
