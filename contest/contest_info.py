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
from contest.models import Contest
from contest.models import Contestant
from contest.models import Clarification

from problem.models import Problem
from problem.models import Testcase
from problem.models import Submission
from problem.models import SubmissionDetail

def get_contestant_list(contest):
    return Contestant.objects.filter(contest = contest)

def get_contest_submission_list(contest):
    
    contestant_list = get_contestant_list(contest)
    
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
    return submission_list

def get_penalty_scoreboard(contest):
    
    contestant_list = get_contestant_list(contest)
    submission_list = get_contest_submission_list(contest)
    
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

    wrong_submission_panelty = 20

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
                    penalty[submission.problem.id] = penalty.get(submission.problem.id,0) + wrong_submission_panelty 
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
    return scoreboard

def get_testcase_scoreboard(contest):
    
    submission_list = get_contest_submission_list(contest)
    
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
    return testcase_scoreboard

def get_contest_problem_passrate(contest):
    scoreboard = get_penalty_scoreboard(contest)
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
    return problem_pass_rate
