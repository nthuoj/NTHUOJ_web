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

from django import template

from contest.models import Contest, Contestant
from contest.contest_info import get_running_contests, get_contestant
from problem.models import SubmissionDetail
from team.models import TeamMember
from utils.user_info import validate_user, has_contest_ownership, \
    has_problem_ownership


register = template.Library()


def show_contest_submission(submission, user, contests):
    for contest in contests:
        if not has_contest_ownership(user, contest):
            continue
        if submission.user == contest.owner or \
                submission.user in contest.coowner.all():
            return True
        contestants = get_contestant(contest)
        if submission.user in contestants:
            return True
    return False


@register.filter()
def show_detail(submission, user):
    """Test if the user can see that submission's
    details (code, error message, etc)

    Args:
        submission: the submission to show
        user: an User object
    Returns:
        a boolean of the judgement
    """
    user = validate_user(user)

    # admin can see everyone's detail
    if user.has_admin_auth():
        return True
    # no one can see admin's detail
    if submission.user.has_admin_auth():
        return False
    # during the contest, only owner/coowner can view contestants' detail
    contests = get_running_contests()
    if contests:
        contests = contests.filter(
            problem=submission.problem,
            creation_time__lte=submission.submit_time
        )
        return show_contest_submission(submission, user, contests)
    # a user can view his own detail
    if submission.user == user:
        return True
    # a problem owner can view his problem's detail in normal mode
    if submission.problem.owner_id == user.username:
        return True
    # contest owner/coowner can still view code after the contest in normal
    # mode
    contests = Contest.objects.filter(
        problem=submission.problem,
        end_time__gte=submission.submit_time,
        creation_time__lte=submission.submit_time)
    if show_contest_submission(submission, user, contests):
        return True
    # a user can view his team member's detail
    if submission.team:
        team_member = TeamMember.objects.filter(
            team=submission.team, member=user)
        if team_member or submission.team.leader == user:
            return True
    # no condition is satisfied
    return False


@register.filter()
def can_rejudge(submission, user):
    """Test if the user can rejudge that submission

    Args:
        submission: the submission to show
        user: an User object
    Returns:
        a boolean of the judgement
    """
    user = validate_user(user)
    # There are 2 kinds of people can rejudge submission:
    # 1. Admin Almighty
    if user.has_admin_auth():
        return True

    # 2. Problem owner
    if has_problem_ownership(user, submission.problem):
        return True

    # 3. Contest owner / coowner
    contests = Contest.objects.filter(
        problem=submission.problem,
        end_time__gte=submission.submit_time,
        creation_time__lte=submission.submit_time)
    for contest in contests:
        if has_contest_ownership(user, contest):
            return True

    return False


@register.simple_tag()
def show_passed_testcase(submission):
    details = submission['list']
    if details:
        return '(%d/%d)' % \
            (details.filter(verdict=SubmissionDetail.AC).count(),
             details.count())
    return ''
