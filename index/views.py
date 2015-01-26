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
import time
import datetime
import random
# Create your views here.
def index(request):
    t = time.time()
    tstr = datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')
    vol = 0
    vol = random.randint(1,10)
    contest_num = 0
    contest_num = random.randint(2,4)
    contest = ['DS', 'senior', 'junior', 'ABC']
    ctime = ['seconds', 'minutes', 'hours', 'days']
    people = 0
    people = random.randint(100,999)
    return render(request, 'index/index.html', 
                { 'tstr':tstr, 'info1':123, 'info2':1234567,
                'people':people, 'vol': vol, 'contest_num':contest_num, 
                'contest':contest, 'ctime':ctime})

def base(request):
    t = time.time()
    tstr = datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')
    people = 0
    people = random.randint(100,999)
    return render(request, 'index/base.html', 
                            { 'tstr':tstr, 'info1':123, 'info2':1234567, 
                            'people':people})

def broken(request):
    people = 0
    people = random.randint(100,999)
    return render(request, 'index/brokenpage.html', 
                            {'error_message':'error message', 'people':people, 
                            'info1':123, 'info2':1234567})

def get_time(request):
    t = time.time()
    tstr = datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')
    return HttpResponse(tstr)

def submit(request):
    people = 0
    people = random.randint(100,999)
    return render(request, 'index/submit.html', 
                            {'people':people, 'info1':123, 'info2':1234567})

def status(request):
    people = 0
    people = random.randint(100,999)
    return render(request, 'index/status.html', 
                            {'people':people, 'info1':123, 'info2':1234567})

def group_list(request):
    people = 0
    people = random.randint(100,999)
    return render(request, 'index/group_list.html', 
                            {'people':people, 'info1':123, 'info2':1234567})

def team_list(request):
    people = 0
    people = random.randint(100,999)
    return render(request, 'index/team_list.html', 
                            {'people':people, 'info1':123, 'info2':1234567})
