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

from contest import contest_info
from contest.scoreboard import Scoreboard
from contest.scoreboard import ScoreboardProblem
from contest.scoreboard import UserProblem
from contest.scoreboard import User

from users.models import User


register = template.Library()

# check if user has contest ownership
@register.filter
def has_auth(user,contest_id):
    contest = Contest.objects.get(id = contest_id)
    return user_info.has_contest_ownership(user,contest)

register.filter("has_auth",has_auth)

@register.filter
def can_ask(user,contest):
    return contest_info.can_ask(user,contest)
register.filter("can_ask",can_ask)

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

@register.filter
def total_contestant(scoreboard):
    return len(scoreboard.users)
register.filter("total_contestant",total_contestant)
