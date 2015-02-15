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
import json
import random
from users.models import User
from users.forms import UserProfileForm, UserLevelForm
from index.views import custom_proc
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from utils.log_info import get_logger, get_client_ip
from django.contrib.auth import authenticate, login, logout
from users.admin import UserCreationForm, AuthenticationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

logger = get_logger()

def list(request):
    users = User.objects.all()
    paginator = Paginator(users, 25)  # Show 25 users per page
    page = request.GET.get('page')

    try:
        user = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        user = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        user = paginator.page(paginator.num_pages)

    return render(
        request,
        'users/userList.html',
        {'users': user},
        context_instance=RequestContext(request, processors=[custom_proc]))

def submit(request):
    return render(
        request,
        'users/submit.html', {},
        context_instance=RequestContext(request, processors=[custom_proc]))


def profile(request, username):
    try:
        profile_user = User.objects.get(username=username)
        piechart_data = []
        for l in ['WA', 'AC', 'RE', 'TLE', 'MLE', 'OLE', 'Others']:
            piechart_data += [{'label': l, 'data': random.randint(50, 100)}]

        render_data = {}
        render_data['profile_user'] = profile_user
        render_data['piechart_data'] = json.dumps(piechart_data)
        if request.user == profile_user:
            render_data['profile_form'] = UserProfileForm(instance=profile_user)
        if request.user.has_judge_auth():
            render_data['userlevel_form'] = UserLevelForm(instance=profile_user)

        if request.method == 'POST':
            profile_form = UserProfileForm(request.POST, instance=profile_user)
            render_data['profile_form'] = profile_form
            if profile_form.is_valid() and request.user == profile_user:
                logger.info('User %s update profile' % username)
                profile_form.save()
                render_data['message'] = 'Update successfully'

            userlevel_form = UserLevelForm(request.POST, instance=profile_user)
            if userlevel_form.is_valid() and request.user.has_judge_auth():
                user_level = userlevel_form.cleaned_data['user_level']
                # admin can change user to all levels
                # judge can change user to sub-judge, user
                if request.user.has_admin_auth() or \
                    request.user.has_judge_auth and \
                    (user_level == User.SUB_JUDGE or user_level == User.USER):
                    logger.info('User %s update %s\'s user_level to %s' %
                        (request.user, username, user_level))
                    render_data['userlevel_form'] = userlevel_form
                    userlevel_form.save()
        
        return render(
            request,
            'users/profile.html',
            render_data,
            context_instance=RequestContext(request, processors=[custom_proc]))
    
    except User.DoesNotExist:
        logger.warning('User %s does not exist' % username)
        return render(
            request,
            'index/500.html',
            {'error_message': 'User %s does not exist' % username})


def user_create(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            logger.info('user %s created' % str(user))
            login(request, user)
            return redirect(reverse('index:index'))
        else:
            return render(
                request, 'users/auth.html',
                {'form': user_form, 'title': 'Sign Up'},
                context_instance=RequestContext(request, processors=[custom_proc]))
    return render(
        request,
        'users/auth.html',
        {'form': UserCreationForm(), 'title': 'Sign Up'},
        context_instance=RequestContext(request, processors=[custom_proc]))


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
            ip = get_client_ip(request)
            logger.info('user %s @ %s logged in' % (str(user), ip))
            login(request, user)
            return redirect(reverse('index:index'))
        else:
            return render(
                request,
                'users/auth.html',
                {'form': user_form, 'title': 'Login'},
                context_instance=RequestContext(request, processors=[custom_proc]))
    return render(
        request,
        'users/auth.html',
        {'form': AuthenticationForm(), 'title': 'Login'},
        context_instance=RequestContext(request, processors=[custom_proc]))
