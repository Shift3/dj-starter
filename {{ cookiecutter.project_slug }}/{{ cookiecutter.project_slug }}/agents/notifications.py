import re

from templated_mail.mail import BaseEmailMessage

from {{ cookiecutter.project_slug }}.agents.models import Agent
from {{ cookiecutter.project_slug }}.notification_system.notifications import BaseNotification
from {{ cookiecutter.project_slug }}.users.models import User


class AgentCreatedNotification(BaseNotification):
    def as_database(self, user):
        return self.context

    def as_email(self, user) -> BaseEmailMessage:
        return BaseEmailMessage(
            subject="A new agent has been created",
            template_name="notifications/agent_created_notification_email.html",
            context={
                "user": user,
                "agent": Agent.objects.get(pk=self.context["agent_id"]),
                "created_by": User.objects.get(pk=self.context["user_id"]),
            },
        )

    def as_sms(self, user):
        pass
