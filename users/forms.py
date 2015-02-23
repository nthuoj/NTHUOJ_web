
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
from django import forms

from users.models import User

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

