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
from contest.models import Contest
from datetime import date


class Announce(models.Model):

    title = models.CharField(max_length=100, default='')
    content = models.TextField(blank=True)

    def __unicode__(self):
        return self.title


class Group(models.Model):

    gname = models.CharField(max_length=50, default='')
    owner = models.ForeignKey(User, related_name='group_owner')
    coowner = models.ManyToManyField(User, related_name='group_coowner', blank=True)
    member = models.ManyToManyField(User, related_name='member', blank=True)
    description = models.TextField(blank=True)
    announce = models.ManyToManyField(Announce, blank=True)
    trace_contest = models.ManyToManyField(Contest, blank=True)
    creation_time = models.DateField(default=date.today, auto_now_add=True)

    def __unicode__(self):
        return '%d - %s' % (self.id, self.gname)
