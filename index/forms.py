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
from index.models import Announcement
from datetimewidget.widgets import DateTimeWidget, DateWidget, TimeWidget

class AnnouncementCreationForm(forms.ModelForm):
    dateTimeOptions = {
            'format': 'yyyy-mm-dd hh:ii:00',
            'todayBtn': 'true',
            'minuteStep': 30,
    }
    content = forms.CharField(widget=forms.Textarea)
    start_time = forms.DateTimeField(widget=DateTimeWidget(options=dateTimeOptions, bootstrap_version=3))
    end_time = forms.DateTimeField(widget=DateTimeWidget(options=dateTimeOptions, bootstrap_version=3))
    class Meta:
        model = Announcement
        fields = ('content', 'start_time', 'end_time')

    def clean_end_time(self):
        start_time = self.cleaned_data.get("start_time")
        end_time = self.cleaned_data.get("end_time")
        if end_time <= start_time:
            raise forms.ValidationError("End time cannot be earlier than start time.")
        return end_time
