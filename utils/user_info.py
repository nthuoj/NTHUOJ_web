"""
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
"""
from datetime import datetime
from threading import Thread
import hashlib
import random

from django.core.urlresolvers import reverse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from contest.models import Contest
from contest.models import Contestant
from problem.models import Submission, SubmissionDetail
from users.models import User, UserProfile
from utils.log_info import get_logger
from utils.config_info import get_config
from django.conf import settings

EMAIL_HOST_USER = get_config('email', 'user')

logger = get_logger()

def has_contest_ownership(curr_user, curr_contest):
    curr_user = validate_user(curr_user)

    if curr_user == curr_contest.owner:
        return True

    contest_coowners = curr_contest.coowner.all()
    return curr_user in contest_coowners



def has_group_ownership(curr_user, curr_group):
    curr_user = validate_user(curr_user)

    if curr_user == curr_group.owner:
        return True

    group_coowners = curr_group.coowner.all()
    if group_coowners:
        for coowner in group_coowners:
            if curr_user == coowner:
                return True
    return False


def has_problem_ownership(curr_user, curr_problem):
    curr_user = validate_user(curr_user)

    return curr_user == curr_problem.owner


def has_problem_auth(user, problem):
    """Check if user has authority to see/submit that problem"""
    user = validate_user(user)

    if problem.visible:
        return True

    last_contest = problem.contest_set.all().order_by('-start_time')
    if last_contest and last_contest[0].start_time < datetime.now():
        problem.visible = True
        problem.save()
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
        creation_time__lte=datetime.now(),
        end_time__gte=datetime.now(),
        problem=problem)
    for contest in contests:
        if has_contest_ownership(user, contest):
            return True
    # None of the condition is satisfied
    return False


def validate_user(user):
    # an anonymous user is treated as a normal user
    if user.is_anonymous():
        user = User()  # create a temporary user instance with on attribute
    return user


def get_user_statistics(user):
    """Find the statistics of the given user"""
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
    activation_key = hashlib.sha1(salt + email).hexdigest()

    # Create and save user profile
    new_profile = UserProfile(user=user, activation_key=activation_key)
    new_profile.save()

    # Send email with activation key
    activation_link = request.META['HTTP_HOST'] + \
        reverse('users:confirm', kwargs={'activation_key': activation_key})
    email_subject = 'Account confirmation'
    email_body = render_to_string('index/activation_email.html',
                    {'username': username, 'activation_link': activation_link,
                    'active_time': new_profile.active_time})

    msg = EmailMultiAlternatives(email_subject, email_body, EMAIL_HOST_USER, [email])
    msg.attach_alternative(email_body, "text/html")

    try:
        Thread(target=msg.send, args=()).start()
    except:
        logger.warning("There is an error when sending email to %s's mailbox" % username)

def send_forget_password_email(request, user):
    username = user.username
    email = user.email
    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
    activation_key = hashlib.sha1(salt+email).hexdigest()
    # Create and save user profile
    UserProfile.objects.filter(user=user).delete()
    new_profile = UserProfile(user=user, activation_key=activation_key)
    new_profile.save()

    # Send email with activation key
    profile_link = request.META['HTTP_HOST'] + \
        reverse('users:forget_password_confirm', kwargs={'activation_key': activation_key})
    email_subject = 'Password Reset'
    email_body = render_to_string('index/forget_password_email.html',
                    {'username': username, 'profile_link': profile_link,
                    'active_time': new_profile.active_time})
    msg = EmailMultiAlternatives(email_subject, email_body, EMAIL_HOST_USER, [email])
    msg.attach_alternative(email_body, "text/html")

    try:
        Thread(target=msg.send, args=()).start()
    except:
        logger.warning("There is an error when sending email to %s's mailbox" % username)
