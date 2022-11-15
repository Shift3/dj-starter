import os
import shutil

def remove_notification_files():
    shutil.rmtree(
        os.path.join(
            "{{ cookiecutter.project_slug }}", "notification_system"
        )
    )

    os.remove(
        os.path.join(
            "{{ cookiecutter.project_slug }}",
            "agents",
            "notifications.py"
        )
    )

def main():
    if "{{ cookiecutter.include_notifications }}" == "no":
        remove_notification_files()

    green = "\033[32m"
    reset = "\033[0m"

    full_path = os.path.dirname(os.path.abspath("{{ cookiecutter.project_slug }}"))
    print(green)
    print("SUCCESS!")
    print("Project directory created at {}".format(full_path))
    print()
    print("To get started:")
    print()
    print("# Change directory to the newly created project directory")
    print("cd {{ cookiecutter.project_slug }}")
    print("# Then start docker")
    print("docker-compose up")
    print()
    print("Make sure to check out your new projects README.md for more")
    print("information on development and deployment")
    print(reset)


if __name__ == "__main__":
    main()
