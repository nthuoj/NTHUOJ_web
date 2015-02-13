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
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render,get_object_or_404
from datetime import datetime
from index.views import custom_proc
from django.template import RequestContext
from django.forms.models import model_to_dict

from contest.models import Contest
from contest.models import Contestant
from contest.models import Clarification

from contest.forms import ContestForm

from problem.models import Problem
from problem.models import Testcase
from problem.models import Submission
from problem.models import SubmissionDetail

from utils.log_info import get_logger
from utils import user_info


logger = get_logger()

def archive(request):
    #to store contest basic info and contestants
    contest_list = []
    #store contest basic info only
    contest_info_list = Contest.objects.order_by('-start_time')
    for contest in contest_info_list:
        contestants = Contestant.objects.filter(contest = contest)
        contest_list.append({'contest':contest,'contestants':contestants})

    user = request.user

    return render(request, 'contest/contestArchive.html',
        {'contest_list':contest_list,'user':user},
        context_instance = RequestContext(request, processors = [custom_proc]))

def contest(request,contest_id):

    serverTime = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    try:
        contest = Contest.objects.get(id = contest_id)
    except Contest.DoesNotExist: 
        logger.warning('Contest: Can not find contest %s!' % contest_id)
        raise Http404('Contest does not exist')
    
    clarification_list = Clarification.objects.filter(contest = contest)
    contestant_list = Contestant.objects.filter(contest = contest)
    
    ### get penalty scoreboard ###

    #store contestants' submission dictionary
    submission_list = []
    #temporary store single contestant submission
    contestant_submission_list = []
    for contestant in contestant_list:
        for problem in contest.problem.all():
            submission = Submission.objects.filter(problem = problem , submit_time__lte = contest.end_time,
                submit_time__gte = contest.start_time , user = contestant.user)
            contestant_submission_list.append(submission)
        
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
    #store single problem penalty
    penalty = {}

    #get single contestant
    for contestant_submission_list in submission_list:
        times = {}
        status = {}
        #count penalty
        total_penalty = 0
        #count solved
        solved = 0
        contestant = []
        #get single contestant's submissions
        for submissions in contestant_submission_list['contestant_submission_list']:
            #get single contestant's single submission
            for submission in submissions:
                #count single problem submission times
                times[submission.problem.id] = times.get(submission.problem.id,0) + 1  
                if submission.status == Submission.ACCEPTED:
                    #status[problem name] = 1 if problem is solved
                    status[submission.problem.id] = 1
                    #get single problem penalty
                    penalty[submission.problem.id] = penalty.get(submission.problem.id,0) + (submission.submit_time - contest.start_time).total_seconds()/60
                else:
                    # 20 is penalty if wrong submission
                    penalty[submission.problem.id] = penalty.get(submission.problem.id,0) + 20
                contestant = submission.user
            #calculate penalty and solved
            solved = 0
            for problem in contest.problem.all():
                if status.get(problem.id,0) == 1:
                    solved += 1
                    total_penalty += penalty[problem.id]


            contestant_scoreboard = {'status':status,'times':times,'penalty':total_penalty,'solved':solved}
        scoreboard.append({'contestant':contestant,'contestant_scoreboard':contestant_scoreboard})
        contestant_scoreboard = []

    #ppl_pass instead of pass to avoid using python reserved word
    ppl_pass = {}

    not_pass = {}

    ### get pass rate ###
    for problem in contest.problem.all():
        for contestant_data in scoreboard:
            status = contestant_data['contestant_scoreboard']['status']
            if status.get(problem.id,0) == 1:
                ppl_pass[problem.id] = ppl_pass.get(problem.id,0) + 1
            else:
                not_pass[problem.id] = not_pass.get(problem.id,0) + 1

    problem_pass_rate = {'pass':ppl_pass,'not_pass':not_pass}
    
    ### get testcase scoreboard ###
    testcase_scoreboard = {}
    # store single contestant testcase-based score
    contestant_testcase_scoreboard = {}
    # store single problem passed testcase number
    testcase_status = {}
    # store single problem total testcase number
    testcase_number = {}
    if submission_list.__len__() != 0:
        # single contestant's all submission
        for contestant_submission_list in submission_list:
            testcase_status = {}
            testcase_number = {}
            testcase_contestant_name = ""
            # each problem's submissions
            for submissions in contestant_submission_list['contestant_submission_list']:
                #each submission
                for submission in submissions:
                    submission_detail = SubmissionDetail.objects.filter(sid = submission)
                    accepted_count = 0
                    for testcase in submission_detail.all():
                        if testcase.virdect == SubmissionDetail.AC:
                            accepted_count += 1
                    if accepted_count >= testcase_status.get(submission.problem.id,0):
                        testcase_status[submission.problem.id] = accepted_count
                    testcase_number[submission.problem.id] = Testcase.objects.filter(problem = submission.problem).__len__()
                    testcase_contestant_name = submission.user.username
            contestant_testcase_scoreboard = {'status':testcase_status,'number':testcase_number}
            testcase_scoreboard[testcase_contestant_name] = {'contestant_scoreboard':contestant_testcase_scoreboard}
            contestant_testcase_scoreboard = []

    return render(request, 'contest/contest.html',{'contest':contest,'clarification_list':clarification_list,
        'contestant_list':contestant_list,'contestant_number':contestant_list.__len__(),
        'scoreboard':scoreboard,'testcase_scoreboard':testcase_scoreboard,
        'server_time':serverTime,'problem_pass_rate':problem_pass_rate},
        context_instance = RequestContext(request, processors = [custom_proc]))

def new(request):
    if request.user.has_judge_auth():
        if request.method == 'GET':
            form = ContestForm()
            return render(request,'contest/editContest.html',{'form':form})
        if request.method == 'POST':
            form = ContestForm(request.POST)
            if form.is_valid():
                new_contest = form.save()
                logger.info('Contest: Create a new contest %s!' % new_contest.id)
                return HttpResponseRedirect('/contest/')
    else:
        raise PermissionDenied
    

def edit(request,contest_id):
    try:
        contest = Contest.objects.get(id = contest_id)
    except Contest.DoesNotExist:
        logger.warning('Contest: Can not edit contest %s! Contest not found!' % contest_id)
        raise Http404("Contest does not exist, can not edit.")

    if user_info.has_c_ownership(request.user,contest):
        if request.method == 'GET':        
            contest_dic = model_to_dict(contest)
            form = ContestForm(initial = contest_dic)
            return render(request,'contest/editContest.html',{'form':form})
        if request.method == 'POST':
            form = ContestForm(request.POST, instance = contest)
            if form.is_valid():
                modified_contest = form.save()
                logger.info('Contest: Modified contest %s!' % modified_contest.id)
                return HttpResponseRedirect('/contest/')
    else:
        raise PermissionDenied

def delete(request,contest_id):
    try:
        contest = Contest.objects.get(id = contest_id)
    except Contest.DoesNotExist:
        logger.warning('Contest: Can not delete contest %s! Contest not found!' % contest_id)
        raise Http404("Contest does not exist, can not delete.")
    
    # only contest owner can delete
    if request.user == contest.owner:
        deleted_contest_id = contest.id
        contest.delete()
        logger.info('Contest: Delete contest %s!' % deleted_contest_id)
        return HttpResponseRedirect('/contest/')
    else:
        raise PermissionDenied

def register(request,contest_id):
    #check contest's existance
    try:
        contest = Contest.objects.get(id = contest_id)
    except Contest.DoesNotExist:
        logger.warning('Contest: Can not register contest %s! Contest not found!' % contest_id)
        raise Http404("Contest does not exist, can not register.")
    #check contestant existance
    try:
        #if user has attended
        contestant = Contestant.objects.get(contest = contest,user = request.user)
        logger.info('Contest: User %s has already attended Contest %s!' % (request.user.username,contest.id))
    except Contestant.DoesNotExist:
        contestant = Contestant(contest = contest,user = request.user)
        contestant.save()
        logger.info('Contest: User %s attends Contest %s!' % (request.user.username,contest.id))
    return HttpResponseRedirect('/contest/')
    
