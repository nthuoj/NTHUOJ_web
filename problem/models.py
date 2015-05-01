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

from datetime import datetime
from django.db import models
from team.models import Team
from users.models import User

# Create your models here.

class Tag(models.Model):

    tag_name = models.CharField(max_length=20, default='')

    def __unicode__(self):
        return self.tag_name


class Problem(models.Model):
    LOCAL = 'LOCAL'
    OTHER = 'OTHER'
    JUDGE_SOURCE_CHOICE = (
        (LOCAL, 'Local Judge'),
        (OTHER, 'Use Other Judge'),
    )

    NORMAL = 'LOCAL_NORMAL'
    SPECIAL = 'LOCAL_SPECIAL'
    ERROR_TOLERANT = 'LOCAL_ERR_TOLERANT'
    PARTIAL = 'LOCAL_PARTIAL'
    UVA_JUDGE = 'OTHER_UVA'
    ICPC_JUDGE = 'OTHER_UVALive'
    POJ_JUDGE = 'OTHER_POJ'
    JUDGE_TYPE_CHOICE = (
        # Local Judge
        (NORMAL, 'Normal Judge'),
        (SPECIAL, 'Special Judge'),
        # (ERROR_TOLERANT, 'Error TOLERANT'),
        (PARTIAL, 'Partial Judge'),
        # Other Judge
        (UVA_JUDGE, 'Uva'),
        (ICPC_JUDGE, 'ACM ICPC Live Archive'),
        (POJ_JUDGE, 'POJ'),
    )

    C = 'C'
    CPP = 'CPP'
    CPP11 = 'CPP11'
    LANGUAGE_CHOICE = (
        (C, 'C'),
        (CPP, 'C++'),
        (CPP11, 'C++11'),
    )

    pname = models.CharField(max_length=50, default='')
    owner = models.ForeignKey(User)
    description = models.TextField(blank=True)
    input = models.TextField(blank=True)
    output = models.TextField(blank=True)
    sample_in = models.TextField(blank=True)
    sample_out = models.TextField(blank=True)
    visible = models.BooleanField(default=False)
    error_tolerance = models.DecimalField(decimal_places=15, max_digits=17, default=0)
    other_judge_id = models.IntegerField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True, null=True)
    judge_source = models.CharField(max_length=11, choices=JUDGE_SOURCE_CHOICE, default=LOCAL)
    judge_type = models.CharField(max_length=20, choices=JUDGE_TYPE_CHOICE, default=NORMAL)
    judge_language = models.CharField(max_length=11, choices=LANGUAGE_CHOICE, default=CPP)
    ac_count = models.IntegerField(default=0)
    total_submission = models.IntegerField(default=0)

    def __unicode__(self):
        return '%d - %s' % (self.id, self.pname)


class Testcase(models.Model):
    problem = models.ForeignKey(Problem)
    description = models.TextField(blank=True)
    time_limit = models.IntegerField(default=1)
    memory_limit = models.IntegerField(default=32)

    def __unicode__(self):
        return '%s: %s' % (self.problem.pname, self.description)


class Submission(models.Model):
    WAIT = 'WAIT'
    JUDGING = 'JUDGING'
    ACCEPTED = 'AC'
    NOT_ACCEPTED = 'NA'
    COMPILE_ERROR = 'CE'
    RESTRICTED_FUNCTION = 'RF'
    JUDGE_ERROR = 'JE'
    STATUS_CHOICE = (
        (WAIT, 'Being Judged'),
        (JUDGING, 'Judging'),
        (ACCEPTED, 'All Accepted'),
        (NOT_ACCEPTED, 'Not Accepted'),
        (COMPILE_ERROR, 'Compile Error'),
        (RESTRICTED_FUNCTION, 'Restricted Function'),
        (JUDGE_ERROR, 'Judge Error'),
    )

    C = 'C'
    CPP = 'CPP'
    CPP11 = 'CPP11'
    LANGUAGE_CHOICE = (
        (C, 'C'),
        (CPP, 'C++'),
        (CPP11, 'C++11'),
    )

    problem = models.ForeignKey(Problem)
    user = models.ForeignKey(User)
    team = models.ForeignKey(Team, blank=True, null=True)
    submit_time = models.DateTimeField(default=datetime.now)
    error_msg = models.TextField(blank=True)
    status = models.CharField(max_length=25, choices=STATUS_CHOICE, default=WAIT)
    language = models.CharField(max_length=5, choices=LANGUAGE_CHOICE, default=C)
    other_judge_sid = models.IntegerField(blank=True, null=True)
    def __unicode__(self):
        return str(self.id)


class SubmissionDetail(models.Model):
    AC = 'AC'
    WA = 'WA'
    TLE = 'TLE'
    MLE = 'MLE'
    RE = 'RE'
    PE = 'PE'
    VERDICT_CHOICE = (
        (AC, 'Accepted'),
        (WA, 'Wrong Answer'),
        (TLE, 'Time Limit Exceeded'),
        (MLE, 'Memory Limit Exceeded'),
        (RE, 'Runtime Error'),
        (PE, 'Presentation Error'),
    )

    tid = models.ForeignKey(Testcase)
    sid = models.ForeignKey(Submission)
    cpu = models.FloatField(default=0)
    memory = models.IntegerField(default=0)
    verdict = models.CharField(max_length=3, choices=VERDICT_CHOICE, default='')

    class Meta:
        unique_together = (('tid', 'sid'),)

    def __unicode__(self):
        return 'sid %d, tid %d' % (self.sid.id, self.tid.id)

