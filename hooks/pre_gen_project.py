project_slug = "{{ cookiecutter.project_slug }}"
if hasattr(project_slug, "isidentifier"):
    assert (
        project_slug.isidentifier()
    ), "'{}' project slug is not a valid Python identifier. Make sure that project slug is a fully_underscored_lowercased_name".format(
        project_slug
    )

assert (
    project_slug == project_slug.lower()
), "'{}' project slug should be all lowercase".format(project_slug)


client_name = "{{ cookiecutter.client_name }}"
assert "'" not in client_name, "'{}' client name cannot contain single quotes".format(
    client_name
)
