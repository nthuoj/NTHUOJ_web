# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('team_name', models.CharField(default=b'', unique=True, max_length=15)),
                ('description', models.TextField(blank=True)),
                ('note', models.TextField(blank=True)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('leader', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=b'', max_length=7, choices=[(b'VALID', b'Valid'), (b'INVITED', b'Invited'), (b'APPLY', b'Apply')])),
                ('member', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('team', models.ForeignKey(to='team.Team')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='teammember',
            unique_together=set([('team', 'member')]),
        ),
    ]
