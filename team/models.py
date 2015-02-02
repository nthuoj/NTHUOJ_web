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
from users.models import User

# Create your models here.

class Team(models.Model):

    team_name = models.CharField(max_length=15, default='', unique=True)
    leader = models.ForeignKey(User)
    description = models.TextField(blank=True)
    note = models.TextField(blank=True)
    creation_time = models.DateTimeField(default=date.today, auto_now_add=True)

    def __unicode__(self):
        return self.team_name

class TeamMember(models.Model):

    team = models.ForeignKey(Team)
    member = models.ForeignKey(User)

    VALID = 'VALID'
    INVITED = 'INVITED'
    APPLY = 'APPLY'
    MEMBER_STATUS_CHOICE = (
        (VALID, 'Valid'), (INVITED, 'Invited'), (APPLY, 'Apply'),
    )
    status = models.CharField(max_length=7, choices=MEMBER_STATUS_CHOICE, default='')
    
    class Meta:
        unique_together = (('team', 'member'),)
    
    def __unicode__(self):
        return self.member.username + ' in ' + self.team.team_name

