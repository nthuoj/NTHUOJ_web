# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import users.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('username', models.CharField(default=b'', max_length=15, unique=True, serialize=False, primary_key=True)),
                ('email', models.CharField(default=b'', max_length=100)),
                ('register_date', models.DateField(auto_now_add=True)),
                ('user_level', models.CharField(default=b'USER', max_length=9, choices=[(b'ADMIN', b'Admin'), (b'JUDGE', b'Judge'), (b'SUB_JUDGE', b'Sub-judge'), (b'USER', b'User')])),
                ('theme', models.CharField(default=b'cerulean', max_length=10, choices=[(b'paper', b'Paper'), (b'cosmo', b'Cosmo'), (b'darkly', b'Darkly'), (b'lumen', b'Lumen'), (b'readable', b'Readable'), (b'simplex', b'Simplex'), (b'spacelab', b'Spacelab'), (b'united', b'United'), (b'cerulean', b'Cerulean'), (b'cyborg', b'Cyborg'), (b'flatly', b'Flatly'), (b'journal', b'Journal'), (b'sandstone', b'Sandstone'), (b'slate', b'Slate'), (b'superhero', b'Superhero'), (b'yeti', b'Yeti')])),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('is_public', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.TextField(null=True)),
                ('read', models.BooleanField(default=False)),
                ('receiver', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activation_key', models.CharField(max_length=40, blank=True)),
                ('active_time', models.DateTimeField(default=users.models.get_default_active_time)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'User profiles',
            },
        ),
    ]
