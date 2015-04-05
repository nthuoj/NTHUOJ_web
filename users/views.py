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
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from users.admin import UserCreationForm, AuthenticationForm
from users.forms import CodeSubmitForm
from users.forms import UserProfileForm, UserLevelForm, UserForgetPasswordForm
from users.models import User, UserProfile, Notification
from users.templatetags.profile_filters import can_change_userlevel
from utils.log_info import get_logger
from utils.user_info import get_user_statistics, send_activation_email, send_forget_password_email
from utils.render_helper import render_index
from axes.decorators import *
import json

# Create your views here.

logger = get_logger()

def list(request):
    users = User.objects.all()
    paginator = Paginator(users, 25)  # Show 25 users per page
    page = request.GET.get('page')

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        users = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        users = paginator.page(paginator.num_pages)

    return render_index(
        request,
        'users/userList.html',
        {'users': users})


def profile(request, username):
    try:
        profile_user = User.objects.get(username=username)
        piechart_data = get_user_statistics(profile_user)

        render_data = {}
        render_data['profile_user'] = profile_user
        render_data['piechart_data'] = json.dumps(piechart_data)
        if request.user == profile_user:
            render_data['profile_form'] = UserProfileForm(instance=profile_user)
        if can_change_userlevel(request.user, profile_user):
            render_data['userlevel_form'] = UserLevelForm(instance=profile_user)

        if request.method == 'POST' and 'profile_form' in request.POST:
            profile_form = UserProfileForm(request.POST, instance=profile_user)
            render_data['profile_form'] = profile_form
            if profile_form.is_valid() and request.user == profile_user:
                logger.info('User %s update profile' % username)
                profile_form.save()
                request.user = profile_user
                render_data['profile_message'] = 'Update successfully'

        if request.method == 'POST' and 'userlevel_form' in request.POST:
            userlevel_form = UserLevelForm(request.POST)
            if can_change_userlevel(request.user, profile_user):
                if userlevel_form.is_valid(request.user):
                    user_level = userlevel_form.cleaned_data['user_level']
                    logger.info('User %s update %s\'s user_level to %s' %
                        (request.user, username, user_level))
                    profile_user.user_level = user_level
                    profile_user.save()
                    render_data['userlevel_message'] = 'Update successfully'
                else:
                    user_level = userlevel_form.cleaned_data['user_level']
                    render_data['userlevel_message'] = 'You can\'t switch user %s to %s' % \
                        (profile_user, user_level)

        return render_index(
            request,
            'users/profile.html',
            render_data)

    except User.DoesNotExist:
        logger.warning('User %s does not exist' % username)
        return render(
            request,
            'index/500.html',
            {'error_message': 'User %s does not exist' % username})


def user_create(request):
    args = {}
    args.update(csrf(request))
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        args['user_form'] = user_form
        if user_form.is_valid():
            user = user_form.save()
            send_activation_email(request, user)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            logger.info('user %s created' % str(user))
            return redirect(reverse('index:alert', kwargs={'alert_info': 'mailbox'}))
        else:
            return render_index(
                request, 'users/auth.html',
                {'form': user_form, 'title': 'Sign Up'})
    return render_index(
        request,
        'users/auth.html',
        {'form': UserCreationForm(), 'title': 'Sign Up'})


def user_logout(request):
    logger.info('user %s logged out' % str(request.user))
    logout(request)
    return redirect(reverse('index:index'))


def user_login(request):
    if request.user.is_authenticated():
        return redirect(reverse('index:index'))
    if request.method == 'POST':
        user_form = AuthenticationForm(data=request.POST)
        if user_form.is_valid():
            user = authenticate(
                username=user_form.cleaned_data['username'],
                password=user_form.cleaned_data['password'])
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            ip = get_ip(request)
            logger.info('user %s @ %s logged in' % (str(user), ip))
            one_hour = 60 * 60
            request.session.set_expiry(one_hour)
            logger.info('user %s set session timeout one hour' % str(user))
            login(request, user)
            return redirect(reverse('index:index'))
        else:
            user_form.add_error(None,
                "You will be blocked for 6 minutes if you have over 3 wrong tries.")
            return render_index(
                request,
                'users/auth.html',
                {'form': user_form, 'title': 'Login'})
    return render_index(
        request,
        'users/auth.html',
        {'form': AuthenticationForm(), 'title': 'Login'})


def user_forget_password(request):
    if request.user.is_authenticated():
        return redirect(reverse('index:index'))

    message = ''
    if request.method == 'POST':
        user_form = UserForgetPasswordForm(data=request.POST)
        if user_form.is_valid():
            user = User.objects.get(username=user_form.cleaned_data['username'])
            send_forget_password_email(request, user)
            message = 'Conform email has sent to you.'
        else:
            return render_index(
                request,
                'users/auth.html',
                {'form': user_form, 'title': 'Forget Password'})

    return render_index(
        request,
        'users/auth.html',
        {'form': UserForgetPasswordForm(), 'title': 'Forget Password', 'message': message})


def forget_password_confirm(request, activation_key):
    '''check if user is already logged in and if he
    is redirect him to some other url, e.g. home
    '''
    if request.user.is_authenticated():
        HttpResponseRedirect(reverse('index:index'))

    '''check if there is UserProfile which matches
    the activation key (if not then display 404)
    '''
    user_profile = get_object_or_404(UserProfile, activation_key=activation_key, active_time__gte=datetime.datetime.now())
    user = user_profile.user
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    # Let user login, so as to modify password
    login(request, user)
    logger.info('User %s is ready to reset his/her password' % user.username)
    user_profile.delete()
    return redirect(reverse('users:profile', kwargs={'username': user.username}))


def user_block_wrong_tries(request):
    """Block login for over 3 wrong tries."""
    attempts = AccessAttempt.objects.filter(ip_address=get_ip(request))
    for attempt in attempts:
        if attempt.failures_since_start >= FAILURE_LIMIT:
            unblock_time = attempt.attempt_time + COOLOFF_TIME
            return render_index(request, 'users/blockWrongTries.html',
                {'unblock_time': unblock_time})
    # No block attempt
    return redirect(reverse('index:index'))


@login_required()
def submit(request, pid=None):
    if request.method=='POST':
        codesibmitform = CodeSubmitForm(request.POST, user=request.user)
        if codesibmitform.is_valid():
            codesibmitform.submit()
            return redirect(reverse('status:status'))
        else:
            return render_index(
                request,
                'users/submit.html', {'form': codesibmitform})

    return render_index(
        request,
        'users/submit.html', {'form': CodeSubmitForm(initial={'pid': pid})})


def register_confirm(request, activation_key):
    '''check if user is already logged in and if he
    is redirect him to some other url, e.g. home
    '''
    if request.user.is_authenticated():
        HttpResponseRedirect(reverse('index:index'))

    '''check if there is UserProfile which matches
    the activation key (if not then display 404)
    '''
    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)
    user = user_profile.user
    user.is_active = True
    user.save()
    logger.info('user %s has already been activated' % user.username)
    user_profile.delete()
<<<<<<< HEAD
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
    return render(
=======
    return render_index(
>>>>>>> upstream/dev
        request,
        'users/confirm.html',
        {'username':user.username})

@login_required()
def notification(request, current_tab='none'):

    unread_notifications = Notification.objects.filter \
        (receiver=request.user, read=False).order_by('-id')

    all_notifications = Notification.objects.filter \
        (receiver=request.user).order_by('-id')

    return render_index(
        request, 'users/notification.html',
        {'all_notifications':all_notifications,
         'unread_notifications':unread_notifications,
         'current_tab':current_tab})

@login_required()
def readify(request, read_id, current_tab):
    try:
        Notification.objects.filter \
            (id=long(read_id), receiver=request.user).update(read=True)
        logger.info('Notification id %ld updates successfully!' % long(read_id))
    except Notification.DoesNotExist:
        logger.warning('Notification id %ld does not exsit!' % long(read_id))
    return HttpResponseRedirect(reverse('users:tab', kwargs={'current_tab':current_tab}))

@login_required()
def delete_notification(request, delete_ids, current_tab):
    id_list = delete_ids.split(',')
    if delete_ids != '':
        for delete_id in id_list:
            try:
                Notification.objects.filter \
                    (id=long(delete_id), receiver=request.user).delete()
                logger.info('Notification id %ld deletes successfully!' % long(delete_id))
            except Notification.DoesNotExist:
                logger.warning('Notification id %ld does not exsit!' % long(delete_id))

    return HttpResponseRedirect(reverse('users:tab', kwargs={'current_tab':current_tab}))
