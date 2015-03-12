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
import time
import random
import datetime
from django.http import Http404
from django.utils import timezone
from contest.models import Contest
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext

# Create your views here.
def index(request, alert_info='none'):

    present = timezone.now()
    c_runnings = Contest.objects.filter(start_time__lt=present, end_time__gt=present)
    c_upcomings = Contest.objects.filter(start_time__gt=present)
    return render(request, 'index/index.html', 
                {'c_runnings':c_runnings, 'c_upcomings':c_upcomings,
                'alert_info':alert_info},
                context_instance=RequestContext(request, processors=[custom_proc]))


def custom_404(request):
    return render(request, 'index/404.html', status=404)

def custom_500(request):
    return render(request, 'index/500.html',{'error_message':'error'}, status=500)

def base(request):
    return render(request, 'index/base.html',{},
                context_instance=RequestContext(request, processors=[custom_proc]))

def get_time(request):
    t = time.time()
    tstr = datetime.datetime.fromtimestamp(t).strftime('%Y/%m/%d %H:%M:%S')
    return HttpResponse(tstr)

def custom_proc(request):

    t = time.time()
    tstr = datetime.datetime.fromtimestamp(t).strftime('%Y/%m/%d %H:%M:%S')
    people = 0
    people = random.randint(100,999)
    return {
        'tstr': tstr,
        'people': people,
        'info1': 123,
        'info2': 1234567
    }
