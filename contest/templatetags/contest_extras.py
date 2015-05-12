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
from datetime import datetime
from utils import user_info
from contest.models import Contest

from contest import contest_info
from contest.scoreboard import Scoreboard
from contest.scoreboard import ScoreboardProblem
from contest.scoreboard import UserProblem
from contest.scoreboard import User
from contest.public_user import is_public_user

from users.models import User
from utils import user_info

register = template.Library()

# check if user has contest ownership
@register.filter
def has_auth(user, contest_id):
    contest = Contest.objects.get(id = contest_id)
    user = user_info.validate_user(user)
    return user_info.has_contest_ownership(user, contest) | user.has_admin_auth()

register.filter("has_auth", has_auth)

#clarification
@register.filter
def can_create_contest(user):
    return contest_info.can_create_contest(user)
register.filter("can_create_contest", can_create_contest)

@register.filter
def can_edit_contest(user, contest):
    return contest_info.can_edit_contest(user,contest)
register.filter("can_edit_contest", can_edit_contest)

@register.filter
def can_delete_contest(user, contest):
    return contest_info.can_delete_contest(user,contest)
register.filter("can_delete_contest", can_delete_contest)

@register.filter
def can_ask(user, contest):
    return contest_info.can_ask(user,contest)
register.filter("can_ask", can_ask)

@register.filter
def can_reply(user, contest):
    return contest_info.can_reply(user,contest)
register.filter("can_reply", can_reply)

#check if user is coowner
@register.filter
def is_coowner(user, contest):
    return contest_info.is_coowner(user, contest)
register.filter("is_coowner", is_coowner)

#check if contest is freezed
@register.filter
def is_freezed(contest):
    return contest_info.is_freezed(contest)
register.filter("is_freezed", is_freezed)

#check if user is judge or admin
@register.filter
def has_judge_auth(user):
    if user.is_authenticated():
        return user.has_judge_auth()
    else:
        return False
register.filter("has_judge_auth", has_judge_auth)

#scoreboard
@register.filter
def users_sorted_by_penalty(scoreboard):
    scoreboard.sort_users_by_penalty()
    return scoreboard.users
register.filter("users_sorted_by_penalty", users_sorted_by_penalty)

@register.filter
def users_sorted_by_solved_testcases(scoreboard):
    scoreboard.sort_users_by_solved_testcases()
    return scoreboard.users
register.filter("users_sorted_by_solved_testcases", users_sorted_by_solved_testcases)

@register.filter
def total_contestant(scoreboard):
    return len(scoreboard.users)
register.filter("total_contestant", total_contestant)

@register.filter
def can_register(user, contest):
    return contest_info.can_register(user, contest)
register.filter("can_register", can_register)

@register.filter
def has_attended(user, contest):
    return contest_info.has_attended(user, contest)
register.filter("has_attended", has_attended)

'''
Contest should not be end.
And user should own contest(to register group)
or user can register
'''
@register.filter
def show_register_btn(user, contest):
    if not user.is_authenticated():
        return False
    has_not_started = not contest_info.has_started(contest)
    own_contest = user_info.has_contest_ownership(user, contest)
    is_not_public_user = not is_public_user(user)
    user_is_admin = user.has_admin_auth()
    return has_not_started and (own_contest or is_not_public_user or user_is_admin)
register.filter("show_register_btn", show_register_btn)
