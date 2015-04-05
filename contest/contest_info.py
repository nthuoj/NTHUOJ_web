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

logger = get_logger()

def get_contestant_list(contest):
    return Contestant.objects.filter(contest = contest)

def get_total_testcases(problem):
    testcases = Testcase.objects.filter(problem = problem)
    return testcases.count()

def get_contestant_problem_submission_list(contest, contestant, problem):
    return Submission.objects.filter(problem = problem, submit_time__lte = contest.end_time,
        submit_time__gte = contest.start_time,user = contestant.user).order_by('submit_time')

def get_passed_testcases(submission):
    passed_testcases = SubmissionDetail.objects.filter(sid = submission, verdict = SubmissionDetail.AC)
    return passed_testcases.count()

def get_penalty(obj, start_time):
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

def get_clarifications(user, contest):
    if has_contest_ownership(user,contest):
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
'''
1. contest is not ended
2. contest is open_register
3. user is not owner or coowner
4. user has not attended
5. user is logined
6. user is not admin
'''
NOT_LOGGED_IN = "not_logged_in"
ENDED = "ended"
NOT_OPEN_REGISTER = "not_open_register"
OWN_CONTEST = "own_contest"
HAS_ATTENDED = "has_attended"
IS_ADMIN = "is_admin"
OK = "OK"
def can_register_return_status(user, contest):
    if not user.is_authenticated():
        return NOT_LOGGED_IN

    ended = is_ended(contest)
    if ended:
        return ENDED

    open_register = contest.open_register
    if not open_register:
        return NOT_OPEN_REGISTER

    has_ownership = has_contest_ownership(user,contest)
    if has_ownership:
        return OWN_CONTEST

    has_attended = Contestant.objects.filter(contest = contest,user = user).exists()
    if has_attended:
        return HAS_ATTENDED
    
    if user.has_admin_auth():
        return IS_ADMIN

    return OK

def can_register(user, contest):
    if can_register_return_status(user, contest) is OK:
        return True
    return False

def can_register_log(user, contest):
    status = can_register_return_status(user, contest)
    if status is OK:
        return True
    elif status is NOT_LOGGED_IN:
        logger.info('Contest: User does not logged in. Can not register.')
    elif status is ENDED:
        logger.info('Contest: Contest %s has ended! Can not register.' % (contest.id))
    elif status is NOT_OPEN_REGISTER:
        logger.info('Contest: Registration for Contest %s is closed. Can not register.' % contest.id)
    elif status is OWN_CONTEST:
        logger.info('Contest: User %s has Contest %s ownership. Can not register.' % (user.username, contest.id))
    elif status is HAS_ATTENDED:
        logger.info('Contest: User %s has already attended Contest %s!' % (user.username, contest.id))
    elif status is IS_ADMIN:
        logger.info('Contest: User %s is admin. Can not register contest %s!' % (user.username, contest.id))

    return False

def get_contest_or_404(contest_id):
    try:
        contest = Contest.objects.get(id = contest_id)
        return contest
    except Contest.DoesNotExist:
        logger.warning('Contest: Can not register contest %s! Contest not found!' % contest_id)
        raise Http404('Can not register contest %s! Contest not found!' % contest_id)

def is_ended(contest):
    return (datetime.now() > contest.end_time)
