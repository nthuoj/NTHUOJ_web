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

from contest.contest_info import get_contest_or_404
from contest.contest_info import can_register

from group.models import Group

from utils.log_info import get_logger

logger = get_logger()

def register(contest, user):
    contestant = Contestant(contest = contest,user = user)
    contestant.save()
    logger.info('Contest: User %s attends Contest %s!' % (user.username, contest.id))
    return True

def register_user(contest_id, user):
    contest = get_contest_or_404(contest_id)
    if can_register(contest, user):
        return register(contest,user)
    return False

def register_group(contest_id, group_id):
    contest = get_contest_or_404(contest_id)
    try:
        group = Group.objects.get(id = group_id)
    except Group.DoesNotExist:
        logger.warning('Contest: Group %s can not register contest %s! Group not found!' % (group_id, contest_id))
        raise Http404(' Group %s can not register contest %s! Group not found!' % (group_id, contest_id))

    if not contest.open_register:
        logger.info('Contest: Registration for Contest %s is closed, can not register.' % contest_id)
        return False
    for member in group.member.all():
        if can_register(contest, member):
            register(contest, member)
    return True
    