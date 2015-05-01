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
from django.db.models import Q
from contest.models import Contest 
from contest.models import Contestant
from utils.user_info import validate_user

def get_contests(user):
    user = validate_user(user)
    if user.has_admin_auth():
        #admin show all
        contests_info = Contest.objects.order_by('-start_time')
    elif user.has_subjudge_auth():
        contests_info = get_owned_or_started_contests(user)
    else:
        contests_info = get_started_contests()

    return contests_info.distinct()

def get_owned_or_started_contests(user):
    owned_contests = get_owned_contests(user)
    started_contests = get_started_contests()
    return owned_contests | started_contests

#both owned and coowned
def get_owned_contests(user):
    request = Q(owner = user)|Q(coowner = user)
    owned_contests = Contest.objects.order_by('-start_time').filter(request)
    return owned_contests

def get_started_contests():
    now = datetime.now()
    return Contest.objects.order_by('-start_time').filter(start_time__lte = now)

def add_contestants(contest):
    contestants = Contestant.objects.filter(contest = contest)
    contest.contestants = []
    for contestant in contestants:
        contest.contestants.append(contestant.user.username)
    return contest
