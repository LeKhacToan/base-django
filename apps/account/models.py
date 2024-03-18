from enum import Enum

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):

    def create_user(self, username, password=None, is_staff=False, is_active=True, **extra_fields):
        extra_fields.pop('email', None)
        user = self.model(username=username, is_active=is_active, is_staff=is_staff, **extra_fields)
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        return self.create_user(username, password, is_staff=True, is_superuser=True, **extra_fields)


class User(PermissionsMixin, AbstractBaseUser):
    class AuthGroup(Enum):
        UNKNOWN = -1
        NORMAL = 0
        ADMIN = 1

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now, editable=False)
    is_active = models.BooleanField(default=True)
    ad_username = models.CharField(max_length=255, unique=True)
    fullname = models.CharField(max_length=255)
    ghtk_user_id = models.CharField(max_length=255, null=True)
    auth_group_id = models.SmallIntegerField(default=AuthGroup.NORMAL.value)

    USERNAME_FIELD = 'username'

    objects = UserManager()

    class Meta:
        db_table = 'auth_user'


class AccountUserRole(models.Model):
    class Role(models.IntegerChoices):
        SUPER_USER = 0
        DEV = 1
        OTHER = 2
        ADMIN = 3

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.IntegerField(choices=Role.choices, default=Role.OTHER.value)

    class Meta:
        managed = False
        db_table = 'auth_user_role'
