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
from problem.models import Problem, Submission, SubmissionDetail, Testcase
from vjudge.submit import submit_to_vjudge
from utils import log_info, user_info, config_info, file_info

logger = log_info.get_logger()


class CodeSubmitForm(forms.Form):
    SUBMIT_PATH = config_info.get_config('path', 'submission_code_path')
    LANGUAGE_CHOICE = tuple(config_info.get_config_items('compiler_option'))
    BACKEND_VERSION = config_info.get_config('system_version', 'backend')
    GCC_VERSION = config_info.get_config('system_version', 'gcc')
    GPP_VERSION = config_info.get_config('system_version', 'gpp')

    pid = forms.CharField(label='Problem ID')
    language = forms.ChoiceField(choices=LANGUAGE_CHOICE, initial=Submission.CPP,
                                 help_text="Backend: %s<br>gcc: %s<br>g++: %s"
                                 % (BACKEND_VERSION, GCC_VERSION, GPP_VERSION))
    code = forms.CharField(max_length=10000,
                           widget=forms.Textarea(attrs={'id': 'code_editor'}))

    def clean_pid(self):
        pid = self.cleaned_data['pid']
        if not unicode(pid).isnumeric():
            raise forms.ValidationError("Problem ID must be a number")
        try:
            problem = Problem.objects.get(id=pid)
            if not user_info.has_problem_auth(self.user, problem):
                raise forms.ValidationError("You don't have permission to submit that problem")
        except Problem.DoesNotExist:
            logger.warning('Pid %s doe not exist' % pid)
            raise forms.ValidationError('Problem of this pid does not exist')

        return pid

    def submit(self):
        pid = self.cleaned_data['pid']
        code = self.cleaned_data['code']
        language = self.cleaned_data['language']

        problem = Problem.objects.get(id=pid)
        problem.total_submission += 1
        problem.save()
        submission = Submission.objects.create(
            user=self.user,
            problem=problem,
            language=language)
        try:
            filename = '%s.%s' % (submission.id, file_info.get_extension(submission.language))
            f = open('%s%s' % (self.SUBMIT_PATH, filename), 'w')
            f.write(code.encode('utf-8'))
            f.close()
        except IOError:
            logger.warning('Sid %s fail to save code' % submission.id)

        if problem.judge_source == Problem.OTHER:
            submit_thread = Thread(target=submit_to_vjudge, args=(code, submission))
            submit_thread.start()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', User())
        super(CodeSubmitForm, self).__init__(*args, **kwargs)


class UserProfileForm(forms.ModelForm):
    """A form for updating user's profile. Includes all the required
    fields, plus a repeated password."""

    username = forms.CharField(label='Username',
                               widget=forms.TextInput(attrs={'readonly': True}))
    email = forms.EmailField(label='Email')
    theme = forms.ChoiceField(label='Theme', choices=User.THEME_CHOICE)
    password1 = forms.CharField(label='Password', required=False,
                                widget=forms.PasswordInput())
    password2 = forms.CharField(label='Password Confirmation', required=False,
                                widget=forms.PasswordInput())

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
    def __init__(self, *args, **kwargs):
        request_user = kwargs.pop('request_user', User())
        super(UserLevelForm, self).__init__(*args, **kwargs)
        self.fields['user_level'].label = 'User Level'
        # Admin can have all choices, which is the default
        if request_user.has_admin_auth():
            return
        # Judge can only promote a user to these levels
        if request_user.has_judge_auth():
            self.fields['user_level'].choices = ((User.SUB_JUDGE, 'Sub-judge'), (User.USER, 'User'))

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


class UserForgetPasswordForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()

    def clean_email(self):
        # Check that if username and email match or not
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        if username and email and User.objects.filter(username=username, email=email):
            return email
        raise forms.ValidationError("Username and Email don't match")



