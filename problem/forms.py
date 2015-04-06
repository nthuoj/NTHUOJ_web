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
from problem.models import Problem
from users.models import User
from django.db.models import Q

import autocomplete_light

# create autocomplete interface and register
class UserAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['^username']
    choices = User.objects.filter(Q(user_level=User.ADMIN) | Q(user_level=User.JUDGE) | Q(user_level=User.SUB_JUDGE))
    model = User
    attrs = {
        'placeholder': '',
        'data-autocomplete-minimum-characters': 1
    }
autocomplete_light.register(UserAutocomplete)

class ProblemForm(forms.ModelForm):
    other_judge_id = forms.IntegerField(required=False, min_value=0)
    partial_judge_code = forms.FileField(required=False)
    special_judge_code = forms.FileField(required=False)
    class Meta:
        model = Problem
        fields = [
            'pname',
            'owner',
            'visible',
            'judge_language',
            'judge_source',
            'judge_type',
            'error_torrence',
            'other_judge_id',
            'partial_judge_code',
            'special_judge_code',
        ]
        labels = {
            'pname': 'Problem Name'
        }
        widgets = {
            'owner': autocomplete_light.TextWidget('UserAutocomplete')
        }

