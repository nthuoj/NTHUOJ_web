from django.forms import ModelForm
from django import forms

class CodeSubmitForm(forms.Form):
    LANGUAGE_CHOICE = (
        ('C', 'C: -O2 -lm -std=c99'),
        ('CPP', 'C++:  -O2 -lm -std=c++'),
        ('CPP11', 'C++11: -O2 -lm -std=c++11'),
    )

    pid = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    language = forms.ChoiceField(choices=LANGUAGE_CHOICE, initial='CPP',
        widget=forms.RadioSelect())
    code = forms.CharField(max_length=10000,
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'rows': 20,
                'id': 'code_editor'}))