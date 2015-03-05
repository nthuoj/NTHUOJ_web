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
from django import template
from utils import user_info
from contest.models import Contest

from contest.scoreboard import Scoreboard
from contest.scoreboard import Scoreboard_Problem
from contest.scoreboard import Problem
from contest.scoreboard import User

from users.models import User


register = template.Library()

# check if user has contest ownership
@register.filter
def has_auth(user,contest_id):
    contest = Contest.objects.get(id = contest_id)
    return user_info.has_c_ownership(user,contest)

register.filter("has_auth",has_auth)

#check if user is judge or admin
@register.filter
def has_judge_auth(user):
    if user.is_authenticated():
        return user.has_judge_auth()
    else:
        return False
register.filter("has_judge_auth",has_judge_auth)

#scoreboard
@register.filter
def users_sorted_by_penalty(scoreboard):
    scoreboard.sort_users_by_penalty()
    return scoreboard.users
register.filter("users_sorted_by_penalty",users_sorted_by_penalty)

@register.filter
def users_sorted_by_solved_testcases(scoreboard):
    scoreboard.sort_users_by_solved_testcases()
    return scoreboard.users
register.filter("users_sorted_by_solved_testcases",users_sorted_by_solved_testcases)

def total_contestant(scoreboard):
    return scoreboard.users.__len__()
register.filter("total_contestant",total_contestant)

@register.filter
def get_problem(scoreboard,id):
    return scoreboard.get_problem(id)

register.filter("get_problem",get_problem)

@register.filter
def total_testcase(scoreboard_problem):
    return scoreboard_problem.total_testcase

register.filter("total_testcase",total_testcase)

@register.filter
def is_solved(problem):
    if problem.is_solved():
        return 1
    return 0
register.filter("is_solved",is_solved)

@register.filter
def testcases_solved(problem):
    return problem.testcases_solved()

register.filter("testcases_solved",testcases_solved)

@register.filter
def submit_times(problem):
    return problem.submit_times()

register.filter("submit_times",submit_times)

@register.filter
def problem_solved(user):
    return user.solved()

register.filter("problem_solved",problem_solved)

@register.filter
def penalty(user,start_time):
    return user.penalty(start_time)

register.filter("penalty",penalty)
