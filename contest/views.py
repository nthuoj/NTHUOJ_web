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

from django.http import HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from datetime import datetime
from index.views import custom_proc
from django.template import RequestContext
from django.forms.models import model_to_dict

from contest.models import Contest
from contest.models import Contestant
from contest.models import Clarification

from contest.forms import ContestForm

from problem.models import Submission
from problem.models import Problem

def archive(request):
    #to store contest basic info and contestants
    contest_list = []
    #store contest basic info only
    contest_info_list = Contest.objects.order_by('-start_time')
    for contest in contest_info_list:
        contestants = Contestant.objects.filter(contest = contest)
        contest_list.append({'contest':contest,'contestants':contestants})

    return render(request, 'contest/contestArchive.html',
        {'contest_list':contest_list,'admin':1},
        context_instance = RequestContext(request, processors = [custom_proc]))

def contest(request,contest_id):

    serverTime = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    contest = get_object_or_404(Contest,id = contest_id)
    clarification_list = Clarification.objects.filter(contest = contest)
    contestant_list = Contestant.objects.filter(contest = contest)
    
    ### get panalty scoreboard ###

    #store contestants' submission dictionary
    submission_list = []
    #temporary store single contestant submission
    contestant_submission_list = []
    for contestant in contestant_list:
        for problem in contest.problem.all():
            submission = Submission.objects.filter(problem = problem , submit_time__lte = contest.end_time,
                submit_time__gte = contest.start_time , user = contestant.user)
            contestant_submission_list.append({'submission':submission})
        
        submission_list.append({'contestant_submission_list':contestant_submission_list})
        contestant_submission_list = []
    
    #store all contestants' data
    scoreboard = []
    #store single contestant score
    contestant_scoreboard = []
    #store single problem status (pass or not)
    status = {}
    #store single problem submit times
    times = {}

    #get single contestant
    for contestant_submission_list in submission_list:
        times = {}
        status = {}
        #count panalty
        panalty = 0

        #get single contestant's submissions
        for submissions in contestant_submission_list['contestant_submission_list']:
            #get single contestant's single submission
            for submission in submissions['submission']:
                times[submission.problem.pname.encode('utf8')] = times.get(submission.problem.pname.encode('utf8'),0) + 1
                if submission.status == Submission.ACCEPTED:
                    status[submission.problem.id] = 1

            contestant_scoreboard.append({'status':status,'times':times})
        scoreboard.append({'contestant_scoreboard':contestant_scoreboard})
        contestant_scoreboard = []


    return render(request, 'contest/contest.html',{'contest':contest,'clarification_list':clarification_list,
        'contestant_list':contestant_list,'scoreboard':scoreboard,'server_time':serverTime},
        context_instance = RequestContext(request, processors = [custom_proc]))

def new(request):
    if request.method == 'GET':
        form = ContestForm()
        return render(request,'contest/editContest.html',{'form':form})
    if request.method == 'POST':
        form = ContestForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/contest/')
    

def edit(request,contest_id):
    contest = get_object_or_404(Contest,id = contest_id)
    if request.method == 'GET':        
        contest_dic = model_to_dict(contest)
        form = ContestForm(initial = contest_dic)
        return render(request,'contest/editContest.html',{'form':form})
    if request.method == 'POST':
        form = ContestForm(request.POST, instance = contest )
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/contest/')

def delete(request,contest_id):
    contest = get_object_or_404(Contest,id = contest_id)
    contest.delete()
    return HttpResponseRedirect('/contest/')
