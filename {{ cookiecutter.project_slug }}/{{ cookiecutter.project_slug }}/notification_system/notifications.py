from abc import ABC, abstractmethod
from templated_mail.mail import BaseEmailMessage


class BaseNotification(ABC):
    def __init__(self, context={}):
        self.context = context

    @abstractmethod
    def as_database(self, user):
        pass

    @abstractmethod
    def as_email(self, user) -> BaseEmailMessage:
        pass

    @abstractmethod
    def as_sms(self, user):
        pass
