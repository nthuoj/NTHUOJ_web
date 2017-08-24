# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Announce',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gname', models.CharField(default=b'', max_length=50)),
                ('description', models.TextField(blank=True)),
                ('creation_time', models.DateField(auto_now_add=True)),
                ('announce', models.ManyToManyField(to='group.Announce', blank=True)),
                ('coowner', models.ManyToManyField(related_name='group_coowner', to=settings.AUTH_USER_MODEL, blank=True)),
                ('member', models.ManyToManyField(related_name='member', to=settings.AUTH_USER_MODEL, blank=True)),
                ('owner', models.ForeignKey(related_name='group_owner', to=settings.AUTH_USER_MODEL)),
                ('trace_contest', models.ManyToManyField(to='contest.Contest', blank=True)),
            ],
        ),
    ]
