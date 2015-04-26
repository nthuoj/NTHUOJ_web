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
from datetime import datetime
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

from users.models import User

from utils.user_info import has_contest_ownership
from utils.user_info import validate_user
from utils.log_info import get_logger
from utils import user_info

from django.http import Http404

import csv
from django.http import HttpResponse
from datetime import datetime

logger = get_logger()

def get_contestant_list(contest):
    return Contestant.objects.filter(contest = contest)

def get_total_testcases(problem):
    testcases = Testcase.objects.filter(problem = problem)
    return testcases.count()

def get_contestant_problem_submission_list(contest, contestant, problem):
    return Submission.objects.filter(problem = problem, submit_time__lte = contest.end_time,
        submit_time__gte = contest.start_time, user = contestant.user).order_by('submit_time')

def get_passed_testcases(submission):
    passed_testcases = SubmissionDetail.objects.filter(sid = submission, verdict = SubmissionDetail.AC)
    return passed_testcases.count()

def get_penalty(obj, start_time):
    penalty = obj.get_penalty(start_time)
    if penalty == 0:
        return '--'
    else:
        return penalty

def get_submit_times(problem):
    submit_times = problem.submit_times()
    if submit_times == 0:
        return '--'
    else:
        return submit_times

def get_scoreboard(contest):
    contestants = get_contestant_list(contest)
    
    scoreboard = Scoreboard(contest.start_time)
    for problem in contest.problem.all():
        total_testcases = get_total_testcases(problem);
        new_problem = ScoreboardProblem(problem.id,problem.pname,total_testcases)
        new_problem.no_submission = True
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
                    new_problem.AC_time = new_submission.submit_time - contest.start_time
                    new_problem.AC_time = int(new_problem.AC_time.total_seconds()/60)
                    break
            if new_problem.is_solved():
                scoreboard.get_problem(new_problem.id).add_pass_user()
            else:
                new_problem.AC_time = '--'
            if len(submissions):
                scoreboard.get_problem(new_problem.id).no_submission = False

            #setup problem attribute
            new_problem.penalty = get_penalty(new_problem,scoreboard.start_time)
            new_problem.submit_times = get_submit_times(new_problem)
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

    for problem in scoreboard.problems:
        if len(scoreboard.users):
            problem.pass_rate = float(problem.pass_user) / len(scoreboard.users) * 100
            problem.not_pass_rate = 100 - problem.pass_rate
        else:
            problem.pass_rate = 0
            problem.not_pass_rate = 100
            problem.no_submission = True

    return scoreboard

def get_scoreboard_csv(contest_id, scoreboard_type):
    contest = get_contest_or_404(contest_id)
    scoreboard = get_scoreboard(contest)
    
    response = HttpResponse(content_type='text/csv')
    filename = str(contest.cname) + '-scoreboard-' + str(scoreboard_type)
    response['Content-Disposition'] = 'attachment; filename=' + filename

    #init
    writer = csv.writer(response)
    if scoreboard_type == "penalty":
        write_scoreboard_csv_penalty(writer, contest, scoreboard)
    elif scoreboard_type == "testcases":
        write_scoreboard_csv_testcases(writer, contest, scoreboard)

    return response

def write_scoreboard_csv_penalty(writer, contest, scoreboard):
    #penalty scoreboard csv
    scoreboard.sort_users_by_penalty()
    #title
    title = ['Rank', 'User']
    for problem in scoreboard.problems:
        title.append(problem.id)
    title.append('Total')
    writer.writerow(title)
    #user data
    for counter, user in enumerate(scoreboard.users):
        user_row = [counter+1, user.username]
        for problem in user.problems:
            submit_times = problem.submit_times
            AC_time = problem.AC_time
            user_row.append(str(submit_times) + '/' + str(AC_time))
        total_penalty = user.get_penalty(contest.start_time)
        user_row.append(total_penalty)
        writer.writerow(user_row)

    footer = ['Passed', '']  
    for problem in scoreboard.problems:
        footer.append(problem.pass_user)
    writer.writerow(footer)

def write_scoreboard_csv_testcases(writer, contest, scoreboard):
    #testcases scoreboard csv
    scoreboard.sort_users_by_solved_testcases()
    #title
    title = ['Rank', 'User']
    for problem in scoreboard.problems:
        title.append(problem.id)
    title.append('Total')
    writer.writerow(title)
    #user data
    for counter, user in enumerate(scoreboard.users):
        user_row = [counter+1, user.username]
        for problem in user.problems:
            passed_testcases = problem.get_testcases_solved()
            total_testcases = problem.total_testcases
            user_row.append(str(passed_testcases) + '/' + str(total_testcases))
        user_total_testcases = user.get_testcases_solved()
        user_row.append(user_total_testcases)
        writer.writerow(user_row)

    footer = ['Passed Testcases', '']  
    for problem in scoreboard.problems:
        footer.append(problem.total_solved)
    writer.writerow(footer)

def get_clarifications(user, contest):

    if has_contest_ownership(user,contest) or user.has_admin_auth():
        return Clarification.objects.filter(contest = contest)
    reply_all = Clarification.objects.filter(contest = contest, reply_all = True)
    if user.is_authenticated():
        user_ask = Clarification.objects.filter(contest = contest, asker = user)
        return reply_all | user_ask
    return reply_all

def is_contestant(user, contest):
    user = validate_user(user)
    contestant = Contestant.objects.filter(contest = contest, user = user)
    return (len(contestant)>=1)

#check if user can create new clarification in contest
'''
admin and owner and coowner and contestant can create clarification
'''
def can_ask(user, contest):
    user = validate_user(user)
    user_is_contestant = is_contestant(user,contest)
    user_is_owner_coowner = has_contest_ownership(user,contest)
    user_is_admin = user.has_admin_auth()
    return  user_is_contestant | user_is_owner_coowner | user_is_admin

#check if user can reply clarification
'''
admin and owner and coowner can reply clarification
'''
def can_reply(user, contest):
    user = validate_user(user)
    return user.has_admin_auth() or has_contest_ownership(user,contest)

#check if user can edit contest
'''
admin and owner and coowner can edit
'''
def can_edit_contest(user, contest):
    user = validate_user(user)
    return user.has_admin_auth() or has_contest_ownership(user, contest)

#check if user can create contest
'''
admin or judge can create contest
'''
def can_create_contest(user):
    user = validate_user(user)
    return user.has_judge_auth()

#check if user can delete contest
'''
admin or owner can delete contest
'''
def can_delete_contest(user, contest):
    user = validate_user(user)
    return user.has_admin_auth() or (user == contest.owner)

def contest_registrable(contest):
    if has_started(contest):
        return False    
    open_register = contest.open_register
    if not open_register:
        return False
    return True

def user_can_register_contest(user, contest):
    if not user.is_authenticated():
        return False
    if user.has_admin_auth():
        return False
    has_ownership = has_contest_ownership(user,contest)
    if has_ownership:
        return False
    is_contestant = Contestant.objects.filter(contest = contest, user = user).exists()
    if is_contestant:
        return False
    return True

'''
return boolean
'''
def can_register(user, contest):
    return (contest_registrable(contest) and user_can_register_contest(user, contest))

def get_contest_or_404(contest_id):
    try:
        contest = Contest.objects.get(id = contest_id)
        return contest
    except Contest.DoesNotExist:
        logger.warning('Contest: Can not register contest %s! Contest not found!' % contest_id)
        raise Http404('Can not register contest %s! Contest not found!' % contest_id)

def has_started(contest):
    return (datetime.now() > contest.start_time)
