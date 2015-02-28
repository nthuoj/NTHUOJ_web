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

from contest.scoreboard import Scoreboard
from contest.scoreboard import User
from contest.scoreboard import Scoreboard_Problem
from contest.scoreboard import Problem as User_Problem
from contest.scoreboard import Submission as Scoreboard_Submission

from problem.models import Problem
from problem.models import Testcase
from problem.models import Submission
from problem.models import SubmissionDetail

def get_contestant_list(contest):
    return Contestant.objects.filter(contest = contest)

def get_total_testcases(problem):
    testcases = Testcase.objects.filter(problem = problem)
    return testcases.__len__()

def get_contestant_problem_submission_list(contest,contestant,problem):
    return Submission.objects.filter(problem = problem, submit_time__lte = contest.end_time,
                                     submit_time__gte = contest.start_time, user = contestant.user) 

def get_passed_testcases(submission):
    passed_testcases = SubmissionDetail.objects.filter(sid = submission, virdect = SubmissionDetail.AC)
    return passed_testcases.__len__()

def get_scoreboard(contest):
    contestant_list = get_contestant_list(contest)
    
    scoreboard = Scoreboard(contest.start_time)
    for problem in contest.problem.all():
        testcases_quantity = get_total_testcases(problem);
        new_problem = Scoreboard_Problem(problem.id,problem.pname,testcases_quantity)
        scoreboard.add_problem(new_problem)

    for contestant in contestant_list:
        new_contestant = User(contestant.user.username)
        for problem in contest.problem.all():
            submissions = get_contestant_problem_submission_list(contest,contestant,problem)    
            new_problem = User_Problem(problem.id)
            total_testcases = get_total_testcases(problem)
            for submission in submissions:
                passed_testcases = get_passed_testcases(submission)
                new_submission = Scoreboard_Submission(submission.submit_time,passed_testcases,total_testcases)
                new_problem.add_submission(new_submission)
            if new_problem.is_solved():
                scoreboard.get_problem(new_problem.id).add_pass_user()
            new_contestant.add_problem(new_problem)
        scoreboard.add_user(new_contestant)

    return scoreboard
