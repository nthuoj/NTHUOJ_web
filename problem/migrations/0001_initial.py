# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('team', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pname', models.CharField(default=b'', max_length=50)),
                ('description', models.TextField(blank=True)),
                ('input', models.TextField(blank=True)),
                ('output', models.TextField(blank=True)),
                ('sample_in', models.TextField(blank=True)),
                ('sample_out', models.TextField(blank=True)),
                ('visible', models.BooleanField(default=False)),
                ('error_tolerance', models.DecimalField(default=0, max_digits=17, decimal_places=15)),
                ('other_judge_id', models.IntegerField(null=True, blank=True)),
                ('judge_source', models.CharField(default=b'LOCAL', max_length=11, choices=[(b'LOCAL', b'Local Judge'), (b'OTHER', b'Use Other Judge')])),
                ('judge_type', models.CharField(default=b'LOCAL_NORMAL', max_length=20, choices=[(b'LOCAL_NORMAL', b'Normal Judge'), (b'LOCAL_SPECIAL', b'Special Judge'), (b'LOCAL_PARTIAL', b'Partial Judge'), (b'OTHER_UVA', b'Uva'), (b'OTHER_UVALive', b'ACM ICPC Live Archive'), (b'OTHER_POJ', b'POJ')])),
                ('judge_language', models.CharField(default=b'CPP', max_length=11, choices=[(b'C', b'C'), (b'CPP', b'C++'), (b'CPP11', b'C++11')])),
                ('ac_count', models.IntegerField(default=0)),
                ('total_submission', models.IntegerField(default=0)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('submit_time', models.DateTimeField(default=datetime.datetime.now)),
                ('error_msg', models.TextField(blank=True)),
                ('status', models.CharField(default=b'WAIT', max_length=25, choices=[(b'WAIT', b'Being Judged'), (b'JUDGING', b'Judging'), (b'AC', b'All Accepted'), (b'NA', b'Not Accepted'), (b'CE', b'Compile Error'), (b'RF', b'Restricted Function'), (b'JE', b'Judge Error')])),
                ('language', models.CharField(default=b'C', max_length=5, choices=[(b'C', b'C'), (b'CPP', b'C++'), (b'CPP11', b'C++11')])),
                ('other_judge_sid', models.IntegerField(null=True, blank=True)),
                ('problem', models.ForeignKey(to='problem.Problem')),
                ('team', models.ForeignKey(blank=True, to='team.Team', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SubmissionDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cpu', models.FloatField(default=0)),
                ('memory', models.IntegerField(default=0)),
                ('verdict', models.CharField(default=b'', max_length=3, choices=[(b'AC', b'Accepted'), (b'WA', b'Wrong Answer'), (b'TLE', b'Time Limit Exceeded'), (b'MLE', b'Memory Limit Exceeded'), (b'RE', b'Runtime Error'), (b'PE', b'Presentation Error')])),
                ('sid', models.ForeignKey(to='problem.Submission')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag_name', models.CharField(default=b'', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Testcase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(blank=True)),
                ('time_limit', models.IntegerField(default=1)),
                ('memory_limit', models.IntegerField(default=32)),
                ('problem', models.ForeignKey(to='problem.Problem')),
            ],
        ),
        migrations.AddField(
            model_name='submissiondetail',
            name='tid',
            field=models.ForeignKey(to='problem.Testcase'),
        ),
        migrations.AddField(
            model_name='problem',
            name='tags',
            field=models.ManyToManyField(to='problem.Tag', blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='submissiondetail',
            unique_together=set([('tid', 'sid')]),
        ),
    ]
