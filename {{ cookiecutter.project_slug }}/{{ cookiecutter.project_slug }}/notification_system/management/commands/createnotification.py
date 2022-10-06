import os
from django.core.management.base import BaseCommand
from django.template import Context, Engine
from djangorestframework_camel_case.util import camel_to_underscore

DIR = os.path.dirname(__file__)

class Command(BaseCommand):
    TEMPLATE_PATH = os.path.join(DIR, "notification_template.py")
    help = ""

    def add_arguments(self, parser):
        parser.add_argument("name")
        parser.add_argument("folder")

    def handle(self, *args, **options):
        name = options.pop("name")
        folder = options.pop("folder")

        notifications_folder = os.path.join(folder, "notifications")
        try:
            os.mkdir(notifications_folder)
        except OSError:
            pass

        context = Context(
            {
                "name": name
            },
            autoescape=False,
        )

        with open(self.TEMPLATE_PATH) as template:
            renderer = Engine().from_string(template.read())
            content = renderer.render(context)
            cameled_name = name[0].lower() + name[1:]
            filename = f"{camel_to_underscore(cameled_name)}_notification.py"
            dest = os.path.join(notifications_folder, filename)
            with open(dest, "w", encoding="utf-8") as new_file:
                new_file.write(content)
                print(f"CREATED: {dest}")
