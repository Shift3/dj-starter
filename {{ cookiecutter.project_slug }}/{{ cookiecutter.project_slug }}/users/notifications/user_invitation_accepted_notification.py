
from templated_mail.mail import BaseEmailMessage
from dj_starter_demo.notification_system.backends import DatabaseBackend, EmailBackend, SMSBackend
from dj_starter_demo.notification_system.notifications import BaseNotification


class UserInvitationAcceptedNotification(BaseNotification):
    backends = [DatabaseBackend]

    def as_database(self, user):
        invited_user = self.context["user"]

        return {
            "user_name": invited_user.full_name(),
            "user_id": str(invited_user.id)
        }

    def as_email(self, user) -> BaseEmailMessage:
        pass

    def as_sms(self, user) -> str:
        pass
