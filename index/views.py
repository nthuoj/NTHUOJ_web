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
import time
import random
import autocomplete_light
from django.http import Http404
from django.utils import timezone
from utils.log_info import get_logger
from contest.models import Contest
from django.http import HttpResponse
from datetime import datetime, timedelta
from index.models import Announcement
from users.models import User, Notification
from django.shortcuts import render, redirect
from utils.render_helper import render_index
from django.template import RequestContext
from utils.user_info import validate_user
from django.core.urlresolvers import reverse
from django.template import RequestContext
from index.forms import AnnouncementCreationForm
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from problem.models import Problem
from group.models import Group

# Create your views here.
logger = get_logger()


def index(request, alert_info='none'):

    present = timezone.now()
    time_threshold = datetime.now() + timedelta(days=1);
    c_runnings = Contest.objects.filter \
        (start_time__lt=present, end_time__gt=present, is_homework=False)
    c_upcomings = Contest.objects.filter \
        (start_time__gt=present, start_time__lt=time_threshold, is_homework=False).order_by('start_time')
    announcements = Announcement.objects.filter \
        (start_time__lt=present, end_time__gt=present)
    return render_index(request, 'index/index.html',
                {'c_runnings':c_runnings, 'c_upcomings':c_upcomings,
                'announcements':announcements, 'alert_info':alert_info})

@login_required()
def announcement_create(request):
    if User.has_admin_auth(request.user) == False:
        raise PermissionDenied('User %s does not have the permission!' % str(request.user))
    if request.method == 'POST':
        form = AnnouncementCreationForm(request.POST)
        if form.is_valid():
            announcement = form.save()
            announcement.backend = 'django.contrib.auth.backends.ModelBackend'
            return redirect(reverse('index:index'))
    else:
        form = AnnouncementCreationForm()
    return render_index(request, 'index/announcement.html',
                {'form': form, 'title': 'Create Announcement'})

@login_required()
def announcement_update(request, aid):
    if User.has_admin_auth(request.user) == False:
        raise PermissionDenied('User %s does not have the permission' % str(request.user))

    try:
        announcement = Announcement.objects.get(id=long(aid))
    except Announcement.DoesNotExist:
        raise Exception('Announcement %ld does not exist' % long(aid))

    if request.method == 'POST':
        form = AnnouncementCreationForm(request.POST, instance=announcement)
        if form.is_valid():
            updating = form.save()
            updating.backend = 'django.contrib.auth.backends.ModelBackend'
            return redirect(reverse('index:index'))
    else:
        form = AnnouncementCreationForm(instance=announcement)
    return render_index(request, 'index/announcement.html',
                {'form': form, 'announcement':announcement, 'title': 'Update Announcement'})

@login_required()
def announcement_delete(request, aid):
    if User.has_admin_auth(request.user) == False:
        raise PermissionDenied('User %s does not have the permission' % str(request.user))

    try:
        announcement = Announcement.objects.get(id=long(aid))
        announcement.delete()
    except Announcement.DoesNotExist:
        raise Exception('Announcement %ld does not exist' % long(aid))
    return redirect(reverse('index:index'))

def navigation_autocomplete(request):
    now = datetime.now()
    q = request.GET.get('q', '')

    queries = {}

    queries['users'] = User.objects.filter(
        username__istartswith=q
    )[:5]

    queries['problems'] = Problem.objects.filter(
        Q(visible=True) & (Q(pname__icontains=q) | Q(id__contains=q))
    )[:10]

    queries['contests'] = Contest.objects.filter(
        Q(start_time__lt=now) & (Q(cname__icontains=q) | Q(id__contains=q))
    )[:5]

    queries['groups'] = Group.objects.filter(
        Q(gname__icontains=q) | Q(id__contains=q)
    )[:5]

    return render(request, 'index/navigation_autocomplete.html', queries)

def custom_400(request):
    return render(request, 'index/400.html', status=400)

def custom_403(request):
    return render(request, 'index/403.html', status=403)

def custom_404(request):
    return render(request, 'index/404.html', status=404)

def custom_500(request):
    return render(request, 'index/500.html',{'error_message':'error'}, status=500)

def base(request):
    return render_index(request, 'index/base.html',{})

def get_time(request):
    t = time.time()
    tstr = datetime.fromtimestamp(t).strftime('%Y/%m/%d %H:%M:%S')
    return HttpResponse(tstr)
