'''
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
'''

from django.db import models
from datetime import date

# Create your models here.

class User(models.Model):
    
    username = models.CharField(max_length=15, primary_key=True, default='')
    password = models.CharField(max_length=20, blank=True)
    email = models.CharField(max_length=100, default='')
    register_date = models.DateField(default=date.today, auto_now_add=True)
    active = models.BooleanField(default=False)

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
    user_level = models.CharField(max_length=9, choices=USER_LEVEL_CHOICE, default=USER)

    PAPER = 'PAPER'
    READABLE = 'READABLE'
    COSMO = 'COSMO'
    DEFAULT = 'DEFAULT'
    LUMEN = 'LUMEN'
    THEME_CHOICE = (
        (PAPER, 'Paper'),
        (READABLE, 'Readable'),
        (COSMO, 'Cosmo'),
        (DEFAULT, 'Default'),
        (LUMEN, 'Lumen'),
    )
    theme = models.CharField(max_length=8, choices=THEME_CHOICE, default=PAPER)

    def __unicode__(self):
        return self.username

class Notification(models.Model):
    reciver = models.ForeignKey(User)
    message = models.TextField(null=True)
    read = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.id)

