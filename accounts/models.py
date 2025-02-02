from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db import models
from utils.models import TimestampsModel
from utils.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, TimestampsModel):
    """
    Custom "User" model for the application.
    """
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    country = models.CharField(_('country'), max_length=50, blank=True)
    phone_number = models.CharField(_('phone number'), max_length=15, blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
