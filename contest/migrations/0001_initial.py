# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations, connections
import datetime
from django.conf import settings
import django.core.validators
from utils.config_info import get_config
from utils.sql_helper import get_sql_from_file

db_user = get_config('client', 'user')
if db_user == None:
    db_user = connections['default'].settings_dict['USER']

scoreboard_store_procedure_install_sql = get_sql_from_file(
    'get_scoreboard_penalty.sql',
    formatting_tuple=(db_user),
)
scoreboard_store_procedure_uninstall_sql = get_sql_from_file(
    'drop_get_scoreboard_penalty.sql')

def install_scoreboard_store_procedure(apps, schema_editor):
    schema_editor.execute(scoreboard_store_procedure_install_sql)

def uninstall_scoreboard_store_procedure(apps, schema_editor):
    schema_editor.execute(scoreboard_store_procedure_uninstall_sql)


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('team', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clarification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(default=b'', max_length=500)),
                ('reply', models.CharField(default=b'No Response. Please read the problem statement', max_length=500)),
                ('ask_time', models.DateTimeField(auto_now_add=True)),
                ('reply_time', models.DateTimeField(null=True, blank=True)),
                ('reply_all', models.BooleanField(default=False)),
                ('asker', models.ForeignKey(related_name='asker', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cname', models.CharField(default=b'', max_length=50)),
                ('start_time', models.DateTimeField(default=datetime.datetime.now)),
                ('end_time', models.DateTimeField(default=datetime.datetime.now)),
                ('freeze_time', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('is_homework', models.BooleanField(default=False)),
                ('open_register', models.BooleanField(default=True)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('coowner', models.ManyToManyField(related_name='coowner', to=settings.AUTH_USER_MODEL, blank=True)),
                ('owner', models.ForeignKey(related_name='owner', to=settings.AUTH_USER_MODEL)),
                ('problem', models.ManyToManyField(to='problem.Problem', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contestant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contest', models.ForeignKey(to='contest.Contest')),
                ('team', models.ForeignKey(blank=True, to='team.Team', null=True)),
                ('user', models.ForeignKey(related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='clarification',
            name='contest',
            field=models.ForeignKey(to='contest.Contest'),
        ),
        migrations.AddField(
            model_name='clarification',
            name='problem',
            field=models.ForeignKey(blank=True, to='problem.Problem', null=True),
        ),
        migrations.AddField(
            model_name='clarification',
            name='replier',
            field=models.ForeignKey(related_name='replier', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='contestant',
            unique_together=set([('contest', 'user')]),
        ),
        migrations.RunPython(
            install_scoreboard_store_procedure,
            uninstall_scoreboard_store_procedure
        ),
    ]
