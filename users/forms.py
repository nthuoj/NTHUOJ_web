from django import forms
from django.conf import settings
from django.forms import ModelForm

from problem.models import Problem, Submission, SubmissionDetail, Testcase
from utils import log_info

logger = log_info.get_logger()

class CodeSubmitForm(forms.Form):
    LANGUAGE_CHOICE = (
        ('C', 'C: -O2 -lm -std=c99'),
        ('CPP', 'C++:  -O2 -lm -std=c++'),
        ('CPP11', 'C++11: -O2 -lm -std=c++11'),
    )

    pid = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'number'}))
    language = forms.ChoiceField(choices=LANGUAGE_CHOICE, initial='CPP',
        widget=forms.RadioSelect())
    code = forms.CharField(max_length=10000,
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'rows': 20,
                'id': 'code_editor'}))

    def clean_pid(self):
        pid = self.cleaned_data['pid']
        try:
            Problem.objects.get(id=pid)
        except Problem.DoesNotExist:
            logger.warning('Pid %s doe not exist' % pid)
            raise forms.ValidationError('Problem of this pid does not exist')

        return pid

    def submit(self, user):
        pid = self.cleaned_data['pid']
        code = self.cleaned_data['code']
        language = self.cleaned_data['language']

        problem = Problem.objects.get(id=pid)
        testcases = Testcase.objects.filter(problem=problem)
        submission = Submission.objects.create(
            user=user,
            problem=problem,
            language=language)
        try:
            f = open('%s%s.cpp' % (settings.SUBMIT_CODE_PATH, submission.id), 'w')
            f.write(code)
            f.close()
        except IOError:
            logger.warning('Sid %s fail to save code' % submission.id)

        for testcase in testcases:
            SubmissionDetail.objects.create(tid=testcase, sid=submission)
