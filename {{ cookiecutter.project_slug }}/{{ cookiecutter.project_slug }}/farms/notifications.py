from templated_mail.mail import BaseEmailMessage

from {{cookiecutter.project_slug}}.farms.models import Farm
from {{cookiecutter.project_slug}}.notification_system.backends import (DatabaseBackend, EmailBackend, SMSBackend)
from {{cookiecutter.project_slug}}.notification_system.notifications import BaseNotification
from {{cookiecutter.project_slug}}.users.models import User


class FarmCreatedNotification(BaseNotification):
    backends = [DatabaseBackend, EmailBackend, SMSBackend]

    def as_database(self, user):
        farm = Farm.objects.get(pk=self.context["farm_id"])
        created_by = User.objects.get(pk=self.context["user_id"])

        return {
            "farm_name": farm.name,
            "user_name": created_by.full_name(),
            **self.context
        }

    def as_email(self, user) -> BaseEmailMessage:
        return BaseEmailMessage(
            subject="A new farm has been created",
            template_name="notifications/farm_created_notification_email.html",
            context={
                "user": user,
                "farm": Farm.objects.get(pk=self.context["farm_id"]),
                "created_by": User.objects.get(pk=self.context["user_id"]),
            },
        )

    def as_sms(self, user) -> str:
        created_by = User.objects.get(pk=self.context["user_id"])
        return f"Hello {user.full_name()}. A new farm has been created by {created_by.full_name()}"
