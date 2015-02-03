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
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
import time
import datetime
from django.utils import timezone
import random
from contest.models import Contest
from problem.models import Problem

# Create your views here.
def index(request):
    present = timezone.now()
    contests = Contest.objects.all()
    start_times = map(lambda contest: contest.start_time, contests)
    end_times = map(lambda contest: contest.end_time, contests)

    notFisnished = endcontest_filter(end_times, present)
    isRunning = isRunning_filter(start_times, end_times, present)
    isUpcoming = isUpcoming_filter(notFisnished, isRunning)

    cRunnings = Contest.objects.filter(end_time__in=isRunning)
    cUpcomings = Contest.objects.filter(end_time__in=isUpcoming)

    return render(request, 'index/index.html', 
                {'cRunnings':cRunnings, 'cUpcomings':cUpcomings}, 
                context_instance = RequestContext(request, processors = [custom_proc]))

def base(request):
    return render(request, 'index/base.html',{},
                context_instance = RequestContext(request, processors = [custom_proc]))

def broken(request):
    return render(request, 'index/brokenpage.html',
                {'error_message':'error message'},
                context_instance = RequestContext(request, processors = [custom_proc]))

def get_time(request):
    t = time.time()
    tstr = datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')
    return HttpResponse(tstr)

def status(request):
    return render(request, 'index/status.html',{},
                context_instance = RequestContext(request, processors = [custom_proc]))
def group_list(request):
    return render(request, 'index/group_list.html',{},
                context_instance = RequestContext(request, processors = [custom_proc]))

def custom_proc(request):
    volumes = []
    problems = Problem.objects.all()
    ids = map(lambda problem: problem.id, problems)
    volume_number = ids[-1] // 1000
    for i in range(1,volume_number + 2):
        volumes.append(i)

    t = time.time()
    tstr = datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')
    people = 0
    people = random.randint(100,999)
    return {
        'volumes': volumes,
        'tstr': tstr,
        'people': people,
        'info1': 123,
        'info2': 1234567
    }

def endcontest_filter(endlists, present):
    notFishied = []
    for i in endlists:
        if i > present:
            notFishied.append(i)
    return notFishied

def isRunning_filter(startlists, endlists, present):
    isRunning = []
    for i, j in enumerate(startlists):
        if j < present and endlists[i] > present:
            isRunning.append(endlists[i])
    return isRunning

def isUpcoming_filter(notFisnished, isRunning):
    isUpcoming = []
    for i in notFisnished:
        if i not in isRunning:
            isUpcoming.append(i)
    return isUpcoming
