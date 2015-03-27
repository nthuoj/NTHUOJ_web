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
from contest.scoreboard import User as ScoreboardUser
from contest.scoreboard import ScoreboardProblem
from contest.scoreboard import UserProblem
from contest.scoreboard import Submission as ScoreboardSubmission

from problem.models import Problem
from problem.models import Testcase
from problem.models import Submission
from problem.models import SubmissionDetail

from utils.user_info import has_contest_ownership

from users.models import User

def get_contestant_list(contest):
    return Contestant.objects.filter(contest = contest)

def get_total_testcases(problem):
    testcases = Testcase.objects.filter(problem = problem)
    return testcases.count()

def get_contestant_problem_submission_list(contest,contestant,problem):
    return Submission.objects.filter(problem = problem, submit_time__lte = contest.end_time,
        submit_time__gte = contest.start_time,user = contestant.user).order_by('submit_time')

def get_passed_testcases(submission):
    passed_testcases = SubmissionDetail.objects.filter(sid = submission, verdict = SubmissionDetail.AC)
    return passed_testcases.count()

def get_penalty(obj,start_time):
    penalty = obj.get_penalty(start_time)
    if penalty == 0:
        return '--'
    else:
        return penalty

def get_scoreboard(contest):
    contestants = get_contestant_list(contest)
    
    scoreboard = Scoreboard(contest.start_time)
    for problem in contest.problem.all():
        total_testcases = get_total_testcases(problem);
        new_problem = ScoreboardProblem(problem.id,problem.pname,total_testcases)
        scoreboard.add_problem(new_problem)

    for contestant in contestants:
        new_contestant = ScoreboardUser(contestant.user.username)
        for problem in contest.problem.all():
            submissions = get_contestant_problem_submission_list(contest,contestant,problem)    
            total_testcases = get_total_testcases(problem)
            new_problem = UserProblem(problem.id,total_testcases)
            for submission in submissions:
                passed_testcases = get_passed_testcases(submission)
                new_submission = ScoreboardSubmission(submission.submit_time,passed_testcases)
                new_problem.add_submission(new_submission)
                if new_submission.is_solved(total_testcases):
                    break
            if new_problem.is_solved():
                scoreboard.get_problem(new_problem.id).add_pass_user()
            #setup problem attribute
            new_problem.penalty = get_penalty(new_problem,scoreboard.start_time)
            new_problem.submit_times = new_problem.submit_times()
            new_problem.solved = new_problem.is_solved()
            new_problem.testcases_solved = new_problem.get_testcases_solved()
            #to get single problem's total passed submission
            scoreboard_problem = scoreboard.get_problem(problem.id)
            scoreboard_problem.total_solved += new_problem.testcases_solved

            new_contestant.add_problem(new_problem)
        #setup contestant attribute
        new_contestant.solved = new_contestant.get_solved()
        new_contestant.penalty = get_penalty(new_contestant,scoreboard.start_time)
        new_contestant.testcases_solved = new_contestant.get_testcases_solved()
        scoreboard.add_user(new_contestant)

    return scoreboard

def get_clarifications(user,contest):
    if has_contest_ownership(user,contest):
        return Clarification.objects.filter(contest = contest)
    reply_all = Clarification.objects.filter(contest = contest, reply_all = True)
    if user.is_authenticated():
        user_ask = Clarification.objects.filter(contest = contest, asker = user)
        return reply_all | user_ask
    return reply_all

def is_contestant(user,contest):
    if user.is_authenticated():
        contestant = Contestant.objects.filter(contest = contest, user = user)
        if len(contestant) >= 1:
            return True
    return False

def can_ask(user,contest):
    user_is_contestant = is_contestant(user,contest)
    user_is_owner_coowner = has_contest_ownership(user,contest)
    return  user_is_contestant | user_is_owner_coowner

def can_reply(user,contest):
    return has_contest_ownership(user,contest)
