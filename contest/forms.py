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
import datetime
from django import forms
from django.views.generic.edit import UpdateView
from contest.models import Contest
from contest.models import Clarification
from contest.contest_info import get_freeze_time_datetime
from users.models import User
from datetimewidget.widgets import DateTimeWidget, DateWidget, TimeWidget
from problem.models import Problem
from django.db.models import Q

class ContestForm(forms.ModelForm):
    dateTimeOptions = {
            'format': 'yyyy-mm-dd hh:ii:00',
            'todayBtn': 'true',
            'minuteStep': 1,
    }
    start_time = forms.DateTimeField(widget=DateTimeWidget(options=dateTimeOptions, bootstrap_version=3))
    end_time = forms.DateTimeField(widget=DateTimeWidget(options=dateTimeOptions, bootstrap_version=3))
    def __init__(self, *args, **kwargs):
        super(ContestForm, self).__init__(*args, **kwargs)
        # access object through self.instance...
        initial = kwargs.get('initial',{})
        user = initial.get('user',User())
        owner = initial.get('owner',User())
        method = initial.get('method','')
        self.fields['coowner'].queryset = User.objects.exclude(
            Q(user_level=User.USER)|Q(pk = owner))
        if method == 'GET':
            contest_id = initial.get('id',0)
            # if user not is admin
            # get all problem when user is admin
            if not user.has_admin_auth():
                # edit contest
                if contest_id:
                    contest = Contest.objects.get(pk = contest_id)
                    contest_problems = contest.problem.all().distinct()
                    self.fields['problem'].queryset = Problem.objects.filter(
                            Q(visible = True)|Q(owner = user)).distinct() | contest_problems
                # create contest
                else:
                    self.fields['problem'].queryset = Problem.objects.filter(
                            Q(visible = True)|Q(owner = user))

        elif method == 'POST':
            self.fields['problem'].queryset = Problem.objects.all()
    class Meta:
        model = Contest
        fields = (
            'cname',
            'owner',
            'coowner',
            'start_time',
            'end_time',
            'freeze_time',
            'problem',
            'is_homework',
            'open_register',
        )
    def clean_freeze_time(self):
        start_time = self.cleaned_data.get("start_time")
        freeze_time = self.cleaned_data.get("freeze_time")
        end_time = self.cleaned_data.get("end_time")

        if type(end_time) is datetime.datetime:
            if end_time - datetime.timedelta(minutes = freeze_time) <= start_time:
                raise forms.ValidationError("Freeze time cannot longer than Contest duration.")
        return freeze_time

    def clean_end_time(self):
        start_time = self.cleaned_data.get("start_time")
        end_time = self.cleaned_data.get("end_time")
        if end_time <= start_time:
            raise forms.ValidationError("End time cannot be earlier than start time.")
        return end_time

class ClarificationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ClarificationForm, self).__init__(*args, **kwargs)
        #only problems contest contains will be shown in list
        initial = kwargs.get('initial',{})
        contest = initial.get('contest',{})
        if type(contest) is Contest:
            contest_id = contest.id
            the_contest = Contest.objects.get(id=contest_id)
            self.fields['problem'] = forms.ChoiceField(choices=[(problem.id,problem.pname)
                for problem in the_contest.problem.all()])

    class Meta:
        model = Clarification
        fields = (
            'contest',
            'problem',
            'content',
            'asker',
        )
        widgets = {
            'content': forms.Textarea(),
        }

class ReplyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReplyForm, self).__init__(*args, **kwargs)
        #only problems contest contains will be shown in list
        initial = kwargs.get('initial',{})
        contest = initial.get('contest',{})
        if type(contest) is Contest:
            clarifications = Clarification.objects.filter(contest = contest)
            self.fields['clarification'] = forms.ChoiceField(
                choices=[(clarification.id,clarification.content)
                for clarification in clarifications.all()])

    class Meta:
        model = Clarification
        fields = (
            'reply',
            'replier',
            'reply_time',
            'reply_all'
        )
        widgets = {
            'reply': forms.Textarea(),
        }
