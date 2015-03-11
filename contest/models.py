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
from users.models import User
from problem.models import Problem
from team.models import Team
from datetime import datetime
from datetime import timedelta
from django.utils import timezone

# Create your models here.

class Contest(models.Model):

    cname = models.CharField(max_length=50, default='')
    owner = models.ForeignKey(User, related_name='owner')
    coowner = models.ManyToManyField(User, related_name='coowner', blank=True)
    start_time = models.DateTimeField(default=datetime.now)
    end_time = models.DateTimeField(default=datetime.now)
    freeze_time = models.IntegerField(default=0)
    problem = models.ManyToManyField(Problem, blank=True)
    is_homework = models.BooleanField(default=False)
    open_register = models.BooleanField(default=True)
    creation_time = models.DateTimeField(default=datetime.now, auto_now_add=True)

    def time_diff(self):
        present = timezone.now()
        if self.start_time < present:
            delta = self.end_time  - present
        else:
            delta = self.start_time  - present

        deltatime = delta - timedelta(microseconds=delta.microseconds)
        return str(deltatime)

    def __unicode__(self):
        return self.cname


class Contestant(models.Model):

    contest = models.ForeignKey(Contest)
    user = models.ForeignKey(User)
    team = models.ForeignKey(Team, blank=True, null=True)

    class Meta:
        unique_together = (('contest', 'user'),)

    def __unicode__(self):
        return self.user.username + ' attend ' + self.contest.cname


class Clarification(models.Model):

    default_response = 'No Response. Please read the problem statement'

    contest = models.ForeignKey(Contest)
    problem = models.ForeignKey(Problem, blank=True, null=True)
    content = models.CharField(max_length=500, default='')
    reply = models.CharField(max_length=500, default=default_response)
    asker = models.ForeignKey(User, related_name='asker')
    replyer = models.ForeignKey(User, related_name='replyer', blank=True, null=True)
    ask_time = models.DateTimeField(default=datetime.now, auto_now=True)
    reply_time = models.DateTimeField(blank=True, null=True)
    reply_all = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.id)
