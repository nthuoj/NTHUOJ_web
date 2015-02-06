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
from index.views import custom_proc
from general_tools.log import get_logger
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from users.admin import UserCreationForm, AuthenticationForm
# Create your views here.

logger = get_logger()

def submit(request):
    return render(request, 'users/submit.html', {},
                context_instance=RequestContext(request, processors=[custom_proc]))


def profile(request):
    piechart_data = []
    for l in ['WA', 'AC', 'RE', 'TLE', 'MLE', 'OLE', 'Others']:
        piechart_data += [{'label': l, 'data': random.randint(50, 100)}]
    return render(
        request,
        'users/profile.html',
        {'piechart_data': json.dumps(piechart_data)},
        context_instance=RequestContext(request, processors=[custom_proc]))


def user_create(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            logger.info('user %s created' % str(user))
            login(request, user)
            return redirect('/index')
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
    return redirect('/index')


def user_login(request):
    if request.user.is_authenticated():
        return redirect('/index')
    if request.method == 'POST':
        user_form = AuthenticationForm(data=request.POST)
        if user_form.is_valid():
            user = authenticate(
                username=user_form.cleaned_data['username'],
                password=user_form.cleaned_data['password'])
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            ip = request.META.get('HTTP_X_FORWARDED_FOR')
            logger.info('user %s @ %s logged in' % (user, ip))
            login(request, user)
            return redirect('/index')
        else:
            print request.SESSION['login_tries']
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
