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

from contest.scoreboard import Problem
from contest.scoreboard import User

register = template.Library()

# get field['key']
@register.filter
def get_value(field,key):
	return field.get(key,0)

register.filter('get_value', get_value)

# check if user has contest ownership
@register.filter
def has_auth(user,contest_id):
    contest = Contest.objects.get(id = contest_id)
    return user_info.has_c_ownership(user,contest)

register.filter("has_auth",has_auth)

#scoreboard
@register.filter
def solved(problem):
    if(problem.solved() == True):
        return 1
    else:
        return 0

register.filter("solved",solved)

@register.filter
def testcase_solved(problem):
    return problem.testcase_solved()

register.filter("testcase_solved",testcase_solved)


@register.filter
def get_problem(user,pname):
    return user.get_problem(pname)

register.filter("get_problem",get_problem)

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

@register.filter
def passrate(problem):
    return problem.passrate()

register.filter("passrate",passrate)

