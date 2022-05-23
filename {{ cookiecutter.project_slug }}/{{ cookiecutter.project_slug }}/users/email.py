from django.contrib.auth.tokens import default_token_generator
from djoser.email import ActivationEmail as DjoserActivationEmail
from djoser.email import PasswordResetEmail as DjoserPasswordResetEmail
from djoser import utils
from django.conf import settings
from templated_mail.mail import BaseEmailMessage


class ChangeEmailRequestEmail(BaseEmailMessage):
    template_name = "email/change_email_request.html"

    def get_context_data(self):
        context = super().get_context_data()

        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.DJOSER["CHANGE_EMAIL_REQUEST_URL"].format(**context)
        context["frontend_url"] = settings.CLIENT_URL
        return context


class ActivationEmail(DjoserActivationEmail):
    template_name = "email/custom_activation.html"

    def get_context_data(self):
        context = super().get_context_data()
        context["frontend_url"] = settings.CLIENT_URL
        return context


class PasswordResetEmail(DjoserPasswordResetEmail):
    template_name = "email/custom_password_reset.html"

    def get_context_data(self):
        context = super().get_context_data()
        context["frontend_url"] = settings.CLIENT_URL
        return context
