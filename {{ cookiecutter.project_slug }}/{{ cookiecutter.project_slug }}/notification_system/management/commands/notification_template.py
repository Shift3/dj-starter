from {{ cookiecutter.project_slug }}.notification_system.backends import DatabaseBackend, EmailBackend, SMSBackend
from {{ cookiecutter.project_slug }}.notification_system.notifications import BaseNotification

{% raw %}
from templated_mail.mail import BaseEmailMessage

class {{ name }}Notification(BaseNotification):
    backends = [DatabaseBackend, EmailBackend, SMSBackend]

    def as_database(self, user):
        pass

    def as_email(self, user) -> BaseEmailMessage:
        pass

    def as_sms(self, user) -> str:
        pass
{% endraw %}
