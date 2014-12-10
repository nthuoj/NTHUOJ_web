# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contest_id', models.IntegerField(default=0)),
                ('contest_name', models.CharField(max_length=200)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('problem_id', models.IntegerField(default=0)),
                ('problem_name', models.CharField(max_length=200)),
                ('ppl_pass', models.IntegerField()),
                ('ppl_not_pass', models.IntegerField()),
                ('contest', models.ForeignKey(to='contest.Contest')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
