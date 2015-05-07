"""
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
"""
from django import forms
from threading import Thread

from users.models import User
from contest.models import Contest
from problem.models import Problem, Submission
from utils import log_info

logger = log_info.get_logger()


class StatusFilter(forms.Form):
    username = forms.CharField(required=False)
    pid = forms.CharField(label='Problem ID', required=False)
    cid = forms.CharField(label='Contest ID', required=False)
    status = forms.ChoiceField(choices=(('', '---'),) + Submission.STATUS_CHOICE, required=False)

    def clean_username(self):
        username = self.cleaned_data['username']
        if username:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                logger.warning('User %s doe not exist' % username)
                raise forms.ValidationError('User %s does not exist' % username)

        return username


    def clean_pid(self):
        pid = self.cleaned_data['pid']

        if pid:
            try:
                if not unicode(pid).isnumeric():
                    raise forms.ValidationError("Problem ID must be a number")
                problem = Problem.objects.get(id=pid)
            except Problem.DoesNotExist:
                logger.warning('Pid %s doe not exist' % pid)
                raise forms.ValidationError('Problem of this ID does not exist')

        return pid


    def clean_cid(self):
        cid = self.cleaned_data['cid']
        if cid:
            try:
                if not unicode(cid).isnumeric():
                    raise forms.ValidationError("Contest ID must be a number")
                contest = Contest.objects.get(id=cid)
            except Contest.DoesNotExist:
                logger.warning('Cid %s doe not exist' % cid)
                raise forms.ValidationError('Contest of this ID does not exist')

        return cid

