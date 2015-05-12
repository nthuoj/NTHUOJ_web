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
from problem.models import Problem, Tag
from users.models import User
from django.db.models import Q
from ckeditor.widgets import CKEditorWidget

import autocomplete_light

# create autocomplete interface and register
class UserAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['^username']
    choices = User.objects.filter(Q(user_level=User.ADMIN) | \
                                  Q(user_level=User.JUDGE) | \
                                  Q(user_level=User.SUB_JUDGE))
    model = User
    attrs = {
        'placeholder': '',
        'data-autocomplete-minimum-characters': 1
    }

class TagAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['^tag_name']
    choices = Tag.objects.all()
    model = Tag
    attrs = {
        'placeholder': '',
        'data-autocomplete-minimum-characters': 1
    }
autocomplete_light.register(UserAutocomplete)
autocomplete_light.register(TagAutocomplete)

class ProblemForm(forms.ModelForm):
    other_judge_id = forms.IntegerField(required=False, min_value=0)
    partial_judge_code = forms.FileField(required=False)
    partial_judge_header = forms.FileField(required=False)
    special_judge_code = forms.FileField(required=False)
    class Meta:
        model = Problem
        fields = [
            'pname',
            'description',
            'input',
            'output',
            'owner',
            'visible',
            'judge_source',
            'judge_type',
            'judge_language',
            # 'error_tolerance',
            'other_judge_id',
            'partial_judge_code',
            'partial_judge_header',
            'special_judge_code',
        ]
        labels = {
            'pname': 'Problem Name',
        }
        widgets = {
            'description': CKEditorWidget(),
            'input': CKEditorWidget(),
            'output': CKEditorWidget(),
            'owner': autocomplete_light.TextWidget('UserAutocomplete')
        }

    def clean_judge_type(self):
        judge_source = self.cleaned_data['judge_source']
        judge_type = self.cleaned_data['judge_type']

        if judge_source != judge_type.split('_')[0]:
            raise forms.ValidationError("Invalid judge type")

        return judge_type

    def clean_other_judge_id(self):
        judge_source = self.cleaned_data['judge_source']
        judge_id = self.cleaned_data['other_judge_id']
        if judge_source == 'OTHER' and not judge_id:
            raise forms.ValidationError("Invalid Other Judge Id")

        return judge_id

    def clean_partial_judge_code(self):
        judge_type = self.cleaned_data['judge_type']
        code = self.cleaned_data['partial_judge_code']
        if judge_type == 'LOCAL_PARTIAL' and code == None:
            raise forms.ValidationError("Partial judge code empty")
        return code

    def clean_partial_judge_header(self):
        judge_type = self.cleaned_data['judge_type']
        header = self.cleaned_data['partial_judge_header']
        if judge_type == 'LOCAL_PARTIAL' and header == None:
            raise forms.ValidationError("Partial judge header empty")
        return header

    def clean_special_judge_code(self):
        judge_type = self.cleaned_data['judge_type']
        code = self.cleaned_data['special_judge_code']
        if judge_type == 'LOCAL_SPECIAL' and code == None:
            raise forms.ValidationError("Special judge code empty")
        return code


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['tag_name']
        labels = {'tag_name': 'Add Tag'}
        widgets = {
            'tag_name': autocomplete_light.TextWidget('TagAutocomplete',
                                        attrs={'class': 'form-control'})
        }

