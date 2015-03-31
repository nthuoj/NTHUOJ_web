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
from users.models import User

from utils.log_info import get_logger
from utils.user_info import get_public_users
from utils.user_info import attends_not_ended_contest
from utils.user_info import create_anonymous

logger = get_logger()

def register(contest, user):
    contestant = Contestant(contest = contest,user = user)
    contestant.save()
    logger.info('Contest: User %s attends Contest %s!' % (user.username, contest.id))
    return True

def register_user(contest, user):
    if can_register(contest, user):
        return register(contest,user)
    return False

def register_group(contest, group):
    if not contest.open_register:
        logger.info('Contest: Registration for Contest %s is closed, can not register.' % contest.id)
        return False
    for member in group.member.all():
        if can_register(contest, member):
            register(contest, member)
    return True

def register_anonymous(contest, anonymous):
    if not is_integer(anonymous):
        logger.warning('Contest: input word is not interger! Can not register anonymous!')
        return False
    anonymous = int(anonymous)  
    if anonymous < 0:
        logger.info('Contest: input word is less than 0. Can not register anonymous!')
        return False
    if anonymous > 200:
        logger.info('Contest: register anonymous more than 200! Set to 200!')
        anonymous = 200
        
    public_users = get_public_users()
    available = 0
    available_anonymous = []
    for user in public_users:
        if attends_not_ended_contest(user):
            user.is_active = True
        else:
            user.is_active = False
            available_anonymous.append(user)
            available += 1

    #if attend more than request, then kick some out
    all_contestant = Contestant.objects.filter(contest = contest).order_by('-user')
    attended_anonymous = []
    for contestant in all_contestant:
        if contestant.user.username.startswith('OJ'):
            attended_anonymous.append(contestant.user)

    attended = len(attended_anonymous)
    if anonymous == attended:
        return True

    if (anonymous < attended):
        for index,user in enumerate(attended_anonymous):
            if index == (attended-anonymous):
                return True
            username = user.username
            contestant = Contestant.objects.get(user = user)
            contestant.delete()
            logger.info('Contest: User %s leave Contest %s!' % (username, contest.id))
            
    still_need = anonymous - attended
    #available is more than request
    if(available >= still_need):
        for user in available_anonymous:
            if (still_need > 0):
                if can_register(contest, user):
                    register(contest, user)
                    user.is_active = True
                    still_need -= 1
            else:
                break
    #free anonymous user not enough
    else:
        need_to_create = still_need - available
        user_created = create_anonymous(need_to_create)
        for user in available_anonymous:
            if can_register(contest, user):
                register(contest, user)
                user.is_active = True
        for user in user_created:
            if can_register(contest, user):
                register(contest, user)
                user.is_active = True
                user.save()
    for user in public_users:
        user.save()

    return True
    
def is_integer(obj):
    try:
        int(obj)
        return True
    except ValueError:
        return False
