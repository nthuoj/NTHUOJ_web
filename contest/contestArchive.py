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
from contest.contestObject import Contest
from contest.models import Contest as ContestModels
from contest.models import Contestant

def get_contests():
    contests_info = ContestModels.objects.order_by('-start_time')
    contests = []
    for contest in contests_info:
        new_contest = get_contest(contest)
        contests.append(new_contest)
    return contests

def get_contest(contest):
    new_contest = Contest(contest.id,contest.cname,contest.owner) 
    new_contest.set_time(contest.start_time,contest.end_time)
    new_contest.set_freeze_time(contest.freeze_time)
    new_contest.set_homework(contest.is_homework)
    new_contest.set_open_register(contest.open_register)
    for problem in contest.problem.all():
        new_contest.add_problem(problem.pname)
    for coowner in contest.coowner.all():
        new_contest.add_coowner(coowner.username)
    contestants = Contestant.objects.filter(contest = contest)
    for contestant in contestants:
        new_contest.add_contestant(contestant.user.username)
    return new_contest