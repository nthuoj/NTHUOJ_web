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
    contestant = Contestant(contest = contest, user = user)
    contestant.save()
    logger.info('Contest: User %s attends Contest %s!' % (user.username, contest.id))

# add many contestants
def add_contestants(users, contest):
    for user in users:
         add_contestant(user, contest)

# add many contestants and activate them
def add_contestants_and_activate(users, contest):
     add_contestants(users, contest)
     public_user.activate_public_users(users)

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

#tbd
def public_user_register_contest(account_num, contest):
    # can not register started contest
    if has_started(contest):
        return False

    account_num = public_user.check_account_num_valid(account_num)
    # if invalid
    if account_num == -1:
        return False
    public_contestants = public_user.get_public_contestant(contest)
    need = account_num - len(public_contestants)
    # public contestant attend more than needed, kick some out
    if need < 0:
        public_user.delete_public_contestants(\
            public_contestants[account_num:len(public_contestants)])
        return account_num
    #public contestant is not enough
    available_users = public_user.get_available_public_users()
    lack = need - len(available_users)
    # available public user is enough
    if lack <=0:
        add_contestants_and_activate(available_users[0:need], contest)
    # available public user not enough, then create some
    else:
        new_users = public_user.create_public_users(lack)
        add_contestants_and_activate(new_users, contest)
        add_contestants_and_activate(available_users, contest)
    return account_num
