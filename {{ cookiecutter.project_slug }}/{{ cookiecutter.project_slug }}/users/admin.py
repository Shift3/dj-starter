from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from simple_history.admin import SimpleHistoryAdmin


@admin.register(User)
class UserAdminRegister(SimpleHistoryAdmin):
    ordering = ("email",)
