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
from users.models import User
from datetime import datetime
from contest.models import Contest
from team.models import TeamMember
from django.core.urlresolvers import reverse
from utils.user_info import validate_user

register = template.Library()


def show_submission(submission, user):
    '''Test if the user can see that submission

    Args:
        submission: a Submission object
        user: an User object
    Returns:
        a boolean of the judgement
    '''
    # admin can see all submissions
    if user.user_level == user.ADMIN:
        return True

    # no one can see admin's submissions
    if submission.user.user_level == user.ADMIN:
        return False

    # user's own submission must be seen
    if submission.user == user:
        return True

    # problem owner can see all submission of his problem
    if submission.problem.owner_id == user.username:
        return True

    # contest owner/coowner's submission can't be seen before the end of contest
    contests = Contest.objects.filter(
        is_homework=False,
        problem=submission.problem,
        creation_time__lte=submission.submit_time,
        end_time__gte=datetime.now())

    if contests:
        owners = []
        for contest in contests:
            owners.append(contest.owner)
            owners.extend(contest.coowner.all())
        if user in owners:
            # owner/coowner can see submission
            return True
        else:
            # not a owner/coowner
            # to see submission, submission.user must not be owners
            return submission.user not in owners

    # an invisible problem's submission can't be seen
    if not submission.problem.visible:
        return False
    # problem owner's submission can't be seen
    if submission.user.username == submission.problem.owner_id:
        return False
    return True


@register.filter()
def show_detail(submission, user):
    '''Test if the user can see that submission's
    details (code, error message, etc)

    Args:
        submission: the submission to show
        user: an User object
    Returns:
        a boolean of the judgement
    '''
    user = validate_user(user)

    # basic requirement: submission must be shown
    if show_submission(submission, user):
        # admin can see everyone's detail
        if user.user_level == user.ADMIN:
            return True
        # no one can see admin's detail
        if submission.user.user_level == user.ADMIN:
            return False

        contests = Contest.objects.filter(
            is_homework=False,
            start_time__lte=datetime.now(),
            end_time__gte=datetime.now())
        # during the contest, only owner/coowner with user level sub-judge/judge
        # can view the detail
        if contests:
            contests = contests.filter(problem=submission.problem)
            owners = []
            for contest in contests:
                owners.append(contest.owner)
                owners.extend(contest.coowner.all())
            if user in owners:
                return True
            else:
                return False
        # a user can view his own detail
        if submission.user == user:
            return True
        # a problem owner can view his problem's detail
        if submission.problem.owner_id == user.username:
            return True
        # a user can view his team member's detail
        if submission.team:
            team_member = TeamMember.objects.filter(team=submission.team, member=user)
            if team_member or submission.team.leader == user:
                return True
    # no condition is satisfied
    return False


@register.filter()
def submission_filter(submission_list, user):
    '''Return a list of submissions that the given user can see

    Args:
        submission_list: a list of submissions
        user: an User object
    Returns:
        a list of submissions
    '''
    user = validate_user(user)

    # an admin can see all submissions because he/she is god
    if user.user_level == user.ADMIN:
        return submission_list

    # filter for user level less than admin
    valid_submission_list = []
    for submission_group in submission_list:
        submission = submission_group['grouper']
        if show_submission(submission, user):
            valid_submission_list.append(submission_group)

    return valid_submission_list
