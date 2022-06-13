import pytest
from {{ cookiecutter.project_slug }}.users.models import User
from rest_framework.test import APITestCase
from .factories import UserFactory
from django.core import mail


@pytest.mark.django_db
class UserTests(APITestCase):
    def test_registration(self):
        self.client.post(
            "/users/",
            {
                "email": "some@email.com",
                "firstName": "Bob",
                "lastName": "McBob",
            },
        )

        assert User.objects.count() == 1

    def test_sending_change_email_request(self):
        user = UserFactory()
        self.client.force_authenticate(user)

        response = self.client.post(
            "/users/change_email_request/",
            {
                "email": "some@otheremail.com",
            },
        )

        assert len(mail.outbox) > 0
        assert response.status_code == 200

    def test_invitation(self):
        user = UserFactory(role=User.ADMIN)
        self.client.force_authenticate(user)

        response = self.client.post(
            "/users/invitation/",
            {
                "email": "new@user.com",
                "first_name": "Bob",
                "last_name": "Bobbicus",
                "role": User.USER,
            },
        )

        assert len(mail.outbox) > 0
        assert response.status_code == 204

    def test_invitation_for_already_exiting_email(self):
        user = UserFactory(role=User.ADMIN)
        self.client.force_authenticate(user)

        response = self.client.post(
            "/users/invitation/",
            {
                "email": user.email,
                "first_name": "Bob",
                "last_name": "Bobbicus",
                "role": User.USER,
            },
        )

        assert len(mail.outbox) == 0
        assert "email" in response.json()
        assert response.status_code == 400
