"""
The MIT License (MIT)

Copyright (c) 2014 NTHUOJ team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from datetime import date, datetime, timedelta

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

from utils.config_info import get_config_items ,get_config


# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        """
        Creates and saves a User with the given username and password.
        """
        user = self.model(
            username=username,
            password=password
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        """
        Creates and saves a Superser with the given username and password.
        """
        user = self.create_user(username=username, password=password)
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    ADMIN = 'ADMIN'
    JUDGE = 'JUDGE'
    SUB_JUDGE = 'SUB_JUDGE'
    USER = 'USER'
    USER_LEVEL_CHOICE = (
        (ADMIN, 'Admin'),
        (JUDGE, 'Judge'),
        (SUB_JUDGE, 'Sub-judge'),
        (USER, 'User'),
    )
    THEME_CHOICE = tuple(get_config_items('web_theme'))
    DEFAULT_THEME = get_config('theme_settings', 'default')


    username = models.CharField(max_length=15, default='', unique=True, primary_key=True)
    email = models.CharField(max_length=100, default='')
    register_date = models.DateField(default=date.today, auto_now_add=True)
    user_level = models.CharField(max_length=9, choices=USER_LEVEL_CHOICE, default=USER)
    theme = models.CharField(max_length=10, choices=THEME_CHOICE, default=DEFAULT_THEME)

    USERNAME_FIELD = 'username'
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()

    def has_admin_auth(self):
        has_auth = (self.user_level == self.ADMIN)
        return has_auth

    def has_judge_auth(self):
        has_auth = ((self.user_level == self.ADMIN) or (self.user_level == self.JUDGE))
        return has_auth

    def has_subjudge_auth(self):
        has_auth = ((self.user_level == self.ADMIN) or ( self.user_level == self.JUDGE) \
                    or (self.user_level == self.SUB_JUDGE))
        return has_auth

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        # Simplest possible answer: Yes, always (To be constructed later)
        return True

    def has_module_perms(self, app_label):
        # Simplest possible answer: Yes, always (To be constructed later)
        return True

    def __unicode__(self):
        return self.username

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin


class Notification(models.Model):
    receiver = models.ForeignKey(User)
    message = models.TextField(null=True)
    read = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.id)


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40, blank=True)
    # default active time is 15 minutes
    active_time = models.DateTimeField(default=lambda: datetime.now() + timedelta(minutes=15))

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name_plural=u'User profiles'
