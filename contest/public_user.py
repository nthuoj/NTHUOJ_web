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
from django.db import connection
from utils.log_info import get_logger
from datetime import datetime

logger = get_logger()


def get_public_contestant(contest):
    return Contestant.objects.filter(
        user__is_public=True, contest=contest)

def delete_public_contestants(contestants):
    for contestant in contestants:
        user = contestant.user
        contest = contestant.contest
        contestant.delete()
        logger.info('Contest: User %s leaves Contest %s!' %
                    (user.username, contest.id))


def attends_not_ended_contest(user):
    user_attends = Contestant.objects.filter(user=user)
    for contestant in user_attends:
        if(datetime.now() < contestant.contest.end_time):
            return True
    return False


def get_public_user(account_num, contest):
    cursor = connection.cursor()
    cursor.callproc('get_public_user', [account_num, contest])
    results = cursor.fetchall()
    available_public_user = len(results)
    logger.info('%d public users joined the Contest %d'
        % (available_public_user, contest))
    return available_public_user


def create_public_user(account_num, contest):
    cursor = connection.cursor()
    cursor.callproc('create_public_user', [account_num, contest,
        settings.PUBLIC_USER_PREFIX,
        settings.PUBLIC_USER_DEFAULT_PASSWORD])
    results = cursor.fetchall()
    new_public_user = len(results)
    logger.info('%d public users are created for the Contest %d'
        % (new_public_user, contest))
    return new_public_user


def is_public_user(user):
    return user.is_public


'''
if invalid return -1
'''


def check_account_num_valid(account_num):
    if not is_integer(account_num):
        logger.warning(
            'Contest: input word is not interger! Can not register public user!')
        return -1
    account_num = int(account_num)
    if account_num < 0:
        logger.warning(
            'Contest: input word is less than 0. Can not register public user!')
        return -1
    if account_num > settings.MAX_PUBLIC_USER:
        too_many_public_user_warning = 'Contest: register public user more than ' \
            + str(settings.MAX_PUBLIC_USER) + '! Set to ' + \
            str(settings.MAX_PUBLIC_USER) + '!'
        logger.warning(too_many_public_user_warning)
        account_num = settings.MAX_PUBLIC_USER
    return account_num


def is_integer(obj):
    try:
        int(obj)
        return True
    except ValueError:
        return False
