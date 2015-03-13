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
IMPLIED, INCLUDING BUT NOsT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
from contest.models import Contest
from datetime import datetime
from django.core.urlresolvers import reverse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.db import models
from emailInfo import EMAIL_HOST_USER
from group.models import Group
from problem.models import Problem, Submission, SubmissionDetail
from threading import Thread
from users.models import User, UserProfile
from utils.log_info import get_logger
import hashlib
import random

logger = get_logger()


#contest ownership
def has_contest_ownership(curr_user, curr_contest):
    user_is_valid(curr_user) #check user
    #check contset
    try:
        Contest.objects.get(id=curr_contest.id)
    except Contest.DoesNotExist:
        logger.warning('Contest id %ld does not exsit!' % curr_contest.id)

    is_owner = (curr_user.username == curr_contest.owner.username)
    if curr_contest.coowner.all().count() != 0:
        for coowner in curr_contest.coowner.all():
            if curr_user == coowner:
                is_owner = True
    return is_owner


#group ownership
def has_group_ownership(curr_user, curr_group):
    user_is_valid(curr_user) #check user
    #check group
    try:
        Group.objects.get(id=curr_group.id)
    except Group.DoesNotExist:
        logger.warning('Group id %ld does not exsit!' % curr_group.id)

    is_owner = (curr_user.username == curr_group.owner.username)
    if curr_group.coowner.all().count() != 0:
        for coowner in curr_group.coowner.all():
            if curr_user == coowner:
                is_owner = True
    return is_owner


#problem ownership
def has_problem_ownership(curr_user, curr_problem):
    user_is_valid(curr_user) #check user
    #check problem
    try:
        Problem.objects.get(id=curr_problem.id)
    except Problem.DoesNotExist:
        logger.warning('Problem id %ld does not exsit!' % curr_problem.id)

    is_owner = (curr_user.username == curr_problem.owner.username)
    return is_owner


def has_problem_auth(user, problem):
    '''Check if user has authority to see/submit that problem'''
    user = validate_user(user)

    if problem.visible:
        return True
    # check the invisible problem
    # To see/submit an invisible problem, user must
    # 1. has admin auth
    if user.has_admin_auth():
        return True
    # 2. be the problem owner
    if has_problem_ownership(user, problem):
        return True
    # 3. be a contest owner/coowner
    contests = Contest.objects.filter(
        start_time__lte=datetime.now(),
        end_time__gte=datetime.now(),
        problem=problem)
    for contest in contests:
        if has_contest_ownership(user, contest):
            return True
    # None of the condition is satisfied
    return False


def user_is_valid(curr_user):
    try:
        User.objects.get(username=curr_user.username)
    except User.DoesNotExist:
        logger.warning('User username %s does not exsit!' % curr_user.username)

def validate_user(user):
    # an anonymous user is treated as a normal user
    if user.is_anonymous():
        user = User()  # create a temporary user instance with on attribute
    return user


def get_user_statistics(user):
    '''Find the statistics of the given user'''
    # fetch some status labels in Submissions
    # here, we only concern about COMPILE_ERROR, RESTRICTED_FUNCTION,
    # and JUDGE_ERROR since ACCEPTED, NOT_ACCEPTED, etc will appear in
    # SubmissionDetail.VERDICT_CHOICE
    status_labels = [
        Submission.COMPILE_ERROR,
        Submission.RESTRICTED_FUNCTION,
        Submission.JUDGE_ERROR
        ]
    # find all verdict in SubmissionDetail.VERDICT_CHOICE
    verdict_labels = [x[0] for x in SubmissionDetail.VERDICT_CHOICE]
    statistics = []

    # fetch Submission of the given user
    submissions = Submission.objects.filter(user=user)
    for label in status_labels:
        statistics += [{
            'label': label,
            'value': submissions.filter(status=label).count()
        }]

    # fetch Submission of the given user
    submissions_id = map(lambda submission: submission.id, submissions)
    submission_details = SubmissionDetail.objects.filter(sid__in=submissions_id)
    for label in verdict_labels:
        statistics += [{
            'label': label,
            'value': submission_details.filter(verdict=label).count()
        }]

    return statistics


def send_activation_email(request, user):
    username = user.username
    email = user.email
    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
    activation_key = hashlib.sha1(salt+email).hexdigest()

    # Create and save user profile
    new_profile = UserProfile(user=user, activation_key=activation_key)
    new_profile.save()

    # Send email with activation key
    activation_link = request.META['HTTP_HOST'] + \
        reverse('users:confirm', kwargs={'activation_key': activation_key})
    email_subject = 'Account confirmation'
    email_body = render_to_string('index/activation_email.html',
                    {'username': username, 'activation_link': activation_link})
    msg = EmailMultiAlternatives(email_subject, email_body, EMAIL_HOST_USER, [email])
    msg.attach_alternative(email_body, "text/html")

    try:
        Thread(target=msg.send, args=()).start()
    except:
         logger.warning('There is an error when sending email to %s\' mailbox' % username)
