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
from users.models import User
from django.conf import settings
from utils.log_info import get_logger
from datetime import datetime

logger = get_logger()

def delete_public_contestants(contestants):
    for contestant in contestants:
        user = contestant.user
        contest = contestant.contest
        contestant.delete()
        logger.info('Contest: User %s leaves Contest %s!' % (user.username, contest.id))

def get_public_users():
    return User.objects.filter(username__startswith = settings.PUBLIC_USER_PREFIX)

def get_public_contestant(contest):
    return Contestant.objects.filter(
        user__username__startswith = settings.PUBLIC_USER_PREFIX, contest = contest)

def get_available_public_users():
    public_users = get_public_users()
    available_public_users = []
    for user in public_users:
        if not attends_not_ended_contest(user):
            deactivate_public_users([user])
            available_public_users.append(user)

    return available_public_users

def attends_not_ended_contest(user):
    user_attends = Contestant.objects.filter(user = user)
    for contestant in user_attends:
        if(datetime.now() < contestant.contest.end_time):
            return True
    return False

def create_public_users(need):
    public_users = get_public_users()
    we_have = len(public_users)
    new_users = []
    for index in range(we_have, we_have + need):
        username = settings.PUBLIC_USER_PREFIX + str(index)
        new_user = User.objects.create_user(
            username, settings.PUBLIC_USER_DEFAULT_PASSWORD)
        logger.info('user %s created' % str(new_user))
        new_users.append(new_user)
    return new_users

def activate_public_users(public_users):
    for public_user in public_users:
        public_user.is_active = True
        public_user.save()

def deactivate_public_users(public_users):
    for public_user in public_users:
        public_user.is_active = False
        public_user.save()

def is_public_user(user):
    return user.username.startswith(settings.PUBLIC_USER_PREFIX)


'''
if invalid return -1
'''
def check_account_num_valid(account_num):
    if not is_integer(account_num):
        logger.warning('Contest: input word is not interger! Can not register public user!')
        return -1
    account_num = int(account_num)
    if account_num < 0:
        logger.warning('Contest: input word is less than 0. Can not register public user!')
        return -1
    if account_num > settings.MAX_PUBLIC_USER:
        too_many_public_user_warning = 'Contest: register public user more than ' \
             + str(settings.MAX_PUBLIC_USER) + '! Set to ' + str(settings.MAX_PUBLIC_USER) + '!'
        logger.warning(too_many_public_user_warning)
        account_num = settings.MAX_PUBLIC_USER
    return account_num

def is_integer(obj):
    try:
        int(obj)
        return True
    except ValueError:
        return False
