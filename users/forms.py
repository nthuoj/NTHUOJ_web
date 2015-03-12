from django import forms
from django.conf import settings
from django.forms import ModelForm

from users.models import User
from problem.models import Problem, Submission, SubmissionDetail, Testcase
from utils import log_info, user_info, config_info

logger = log_info.get_logger()

class CodeSubmitForm(forms.Form):
    SUBMIT_PATH = config_info.get_config('path', 'submission_code_path')
    LANGUAGE_CHOICE = tuple(config_info.get_config_items('compiler_option'))

    pid = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    language = forms.ChoiceField(choices=LANGUAGE_CHOICE, initial='CPP',
        widget=forms.RadioSelect())
    code = forms.CharField(max_length=10000,
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'rows': 20,
                'id': 'code_editor'}))

    def clean_pid(self):
        pid = self.cleaned_data['pid']
        try:
            problem = Problem.objects.get(id=pid)
            if not user_info.has_problem_auth(self.user, problem):
                raise forms.ValidationError('You don\'t have permission to submit that problem')
        except Problem.DoesNotExist:
            logger.warning('Pid %s doe not exist' % pid)
            raise forms.ValidationError('Problem of this pid does not exist')

        return pid

    def submit(self):
        pid = self.cleaned_data['pid']
        code = self.cleaned_data['code']
        language = self.cleaned_data['language']

        problem = Problem.objects.get(id=pid)
        testcases = Testcase.objects.filter(problem=problem)
        submission = Submission.objects.create(
            user=self.user,
            problem=problem,
            language=language)
        try:
            f = open('%s%s.cpp' % (self.SUBMIT_PATH, submission.id), 'w')
            f.write(code)
            f.close()
        except IOError:
            logger.warning('Sid %s fail to save code' % submission.id)

        for testcase in testcases:
            SubmissionDetail.objects.create(tid=testcase, sid=submission)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', User())
        super(CodeSubmitForm, self).__init__(*args, **kwargs)

class UserProfileForm(forms.ModelForm):
    """A form for updating user's profile. Includes all the required
    fields, plus a repeated password."""

    username = forms.CharField(label='Username',
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': True}))
    email = forms.EmailField(label='Email',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    theme = forms.ChoiceField(label='Theme',
        choices=User.THEME_CHOICE,
        widget=forms.Select(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Password Confirmation', required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'theme', 'password1', 'password2')

    def clean_username(self):
        # username is primary key, should not be changed
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.username
        else:
            return self.cleaned_data['username']

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        if (not password1) != (not password2):
            raise forms.ValidationError("Passwords can't be empty")
        return password2

    def save(self):
        if self.cleaned_data["password1"]:
            self.instance.set_password(self.cleaned_data["password1"])
        self.instance.save()
        return self.instance


class UserLevelForm(forms.ModelForm):
    """A form for updating user's userlevel."""
    user_level = forms.ChoiceField(label='Userlevel',
        choices=User.USER_LEVEL_CHOICE,
        widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('user_level',)

    def is_valid(self, user):
        # run the parent validation first
        valid = super(UserLevelForm, self).is_valid()
        # we're done now if not valid
        if not valid:
            return valid
        # admin can change user to all levels
        if user.has_admin_auth():
            return True
        # judge can change user to sub-judge, user
        user_level = self.cleaned_data['user_level']
        if user.has_judge_auth() and \
            (user_level == User.SUB_JUDGE or user_level == User.USER):
            return True
        return False
