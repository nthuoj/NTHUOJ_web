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
from contest.contest_info import user_can_register_contest
from contest.contest_info import has_started
from contest import public_user
from group.models import Group
from users.models import User

from utils.log_info import get_logger

logger = get_logger()

# add one contestant


def add_contestant(user, contest):
    contestant = Contestant(contest=contest, user=user)
    contestant.save()
    logger.info('Contest: User %s attends Contest %s!' %
                (user.username, contest.id))

# add many contestants


def add_contestants(users, contest):
    for user in users:
        add_contestant(user, contest)


def user_register_contest(user, contest):
    if can_register(user, contest):
        add_contestant(user, contest)
        return True
    return False


def group_register_contest(group, contest):
    if has_started(contest):
        return False
    for user in group.member.all():
        if user_can_register_contest(user, contest):
            add_contestant(user, contest)
    return True


def public_user_register_contest(account_num, contest):
    # can not register started contest
    if has_started(contest):
        return False
    # check whether account_num is valid
    account_num = public_user.check_account_num_valid(account_num)
    if account_num == -1:
        return False
    # get public user
    res = account_num - public_user.get_public_user(account_num, contest)
    # create public user
    if res > 0:
        public_user.create_public_user(res, contest)
    return account_num
