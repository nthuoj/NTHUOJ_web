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
import hashlib, datetime, random
from index.views import custom_proc
from django.core.mail import send_mail
from users.models import User, UserProfile
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.context_processors import csrf
from utils.log_info import get_logger, get_client_ip
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from users.admin import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, render_to_response
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


@login_required()
def submit(request):
    return render(
        request,
        'users/submit.html', {},
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
    args = {}
    args.update(csrf(request))
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        args['user_form'] = user_form
        if user_form.is_valid():
            user = user_form.save()

            username = user_form.cleaned_data['username']
            email = user_form.cleaned_data['email']
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
            activation_key = hashlib.sha1(salt+email).hexdigest()
            
            
            #Get user by username
            user=User.objects.get(username=username)

            # Create and save user profile
            new_profile = UserProfile(user=user, activation_key=activation_key)
            new_profile.save()

            #Send email with activation key
            email_subject = 'Account confirmation'
            email_body = "Hey %s, thanks for signing up.\n \
To activate your account, click the link below.\n" % (username) + \
            request.META['HTTP_HOST'] + \
            reverse('users:confirm', kwargs={'activation_key': activation_key})

            send_mail(email_subject, email_body, 'nthucsoj@gmail.com', [email], fail_silently=False)

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
    User.objects.filter(username=user.username).update(active=True)
    return render(
        request,
        'users/confirm.html',
        {'username':user.username},
        context_instance=RequestContext(request, processors=[custom_proc]))
