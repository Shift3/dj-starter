import pytest
from ..models import User
from .factories import UserFactory


@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user(email="test@test.com", password="password")

    assert user.is_active == False
    assert user.activated_at == None
    assert user.role == User.USER


@pytest.mark.django_db
def test_create_superuser():
    user = User.objects.create_superuser(email="test@test.com", password="password")

    assert user.is_active
    assert user.activated_at is not None
    assert user.role == User.ADMIN
    assert user.is_superuser


@pytest.mark.django_db
def test_user_activate():
    user = UserFactory()

    user.activate()

    assert user.is_active == True
    assert user.activated_at is not None
    assert user.disabled_at is None

@pytest.mark.django_db
def test_user_deactivate():
    user = UserFactory()

    user.activate()
    user.deactivate()

    assert user.is_active is False
    assert user.disabled_at is not None
