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

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime

from django.shortcuts import redirect
from django.forms.models import model_to_dict
from contest.contest_info import get_scoreboard
from contest.contest_info import get_scoreboard_csv
from contest.contest_info import get_clarifications
from contest.contest_info import can_ask
from contest.contest_info import can_reply
from contest.contest_archive import get_contests
from contest.models import Contest
from contest.models import Contestant
from contest.models import Clarification
from contest.forms import ContestForm
from contest.forms import ClarificationForm
from contest.forms import ReplyForm
from contest.register_contest import register_user
from contest.register_contest import register_group as register_group_impl
from contest.contest_info import can_create_contest
from contest.contest_info import can_edit_contest
from contest.contest_info import can_delete_contest
from contest.contest_info import can_register_log
from contest.contest_info import get_contest_or_404

from problem.problem_info import get_testcase

from group.models import Group
from group.group_info import get_owned_group
from group.group_info import get_group_or_404
from utils.log_info import get_logger
from utils import user_info
from utils.render_helper import render_index
from status.views import *


logger = get_logger()

def archive(request, page = None):
    user = request.user
    all_contests = get_contests(user)
    groups = get_owned_group(user)
    #show 15 contests
    paginator = Paginator(all_contests, 15)

    try:
        contests = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page = 1
        contests = paginator.page(page)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page = paginator.num_pages
        contests = paginator.page(page)
    previous = int(page)-1
    this = int(page)
    next = int(page)+1
    max_page = int(paginator.num_pages)
    pager = {'previous':previous, 'this':this, 'next':next, 'max_page':max_page}
    return render_index(request,
        'contest/contestArchive.html',
        {'contests':contests,'user':user,'groups':groups,'pager':pager})

def contest(request, contest_id):
    try:
        contest = Contest.objects.get(id = contest_id)
    except Contest.DoesNotExist:
        logger.warning('Contest: Can not find contest %s!' % contest_id)
        raise Http404('Contest does not exist')

    now = datetime.now()
    #if contest has not started and user is not the owner
    if ((contest.start_time < now) or user_info.has_contest_ownership(request.user,contest) or\
        request.user.has_admin_auth()):
        for problem in contest.problem.all():
            problem.testcase = get_testcase(problem)
        scoreboard = get_scoreboard(contest)
        status = contest_status(request, contest)
        user = request.user
        clarifications = get_clarifications(user,contest)

        initial_form = {'contest':contest,'asker':user}
        form = ClarificationForm(initial=initial_form)

        initial_reply_form = {'contest':contest,'replier':user}
        reply_form = ReplyForm(initial = initial_reply_form)
        return render_index(request, 'contest/contest.html',
            {'contest':contest, 'clarifications':clarifications, 'user':user,
            'form':form, 'reply_form':reply_form,
            'scoreboard':scoreboard, 'status': status})
    else:
        raise PermissionDenied


@login_required
def new(request):
    if can_create_contest(request.user):
        if request.method == 'GET':
            form = ContestForm(initial={'owner':request.user})
            title = "New Contest"
            return render_index(request,'contest/editContest.html',{'form':form,'title':title})
        if request.method == 'POST':
            form = ContestForm(request.POST)
            if form.is_valid():
                new_contest = form.save()
                logger.info('Contest: User %s Create a new contest %s!' %
                    (request.user ,new_contest.id))
                return redirect('contest:archive')
    raise PermissionDenied

@login_required
def edit(request, contest_id):
    try:
        contest = Contest.objects.get(id = contest_id)
    except Contest.DoesNotExist:
        logger.warning('Contest: Can not edit contest %s! Contest not found!' % contest_id)
        raise Http404('Contest does not exist, can not edit.')
    title = "Edit Contest"
    if can_edit_contest(request.user,contest):
        if request.method == 'GET':
            contest_dic = model_to_dict(contest)
            form = ContestForm(initial = contest_dic)
            return render_index(request,'contest/editContest.html',
                    {'form':form,'user':request.user,'title':title})
        if request.method == 'POST':
            form = ContestForm(request.POST, instance = contest)
            if form.is_valid():
                modified_contest = form.save()
                logger.info('Contest: User %s edited contest %s!' %
                    (request.user, modified_contest.id))
                return archive(request)
            else:
                return render_index(request,'contest/editContest.html',
                    {'form':form,'user':request.user,'title':title})

@login_required
def delete(request, contest_id):
    try:
        contest = Contest.objects.get(id = contest_id)
    except Contest.DoesNotExist:
        logger.warning('Contest: Can not delete contest %s! Contest not found!' % contest_id)
        raise Http404('Contest does not exist, can not delete.')

    if can_delete_contest(request.user, contest):
        deleted_contest_id = contest.id
        contest.delete()
        logger.info('Contest: User %s delete contest %s!' %
            (request.user, deleted_contest_id))
        return redirect('contest:archive')
    raise PermissionDenied

@login_required
def register(request, contest_id):
    contest = get_contest_or_404(contest_id)
    #get group id or register as single user
    group_id = request.GET.get('group')
    if(group_id is not None):
        register_group(request, group_id, contest)
    else:
        register_user(request.user, contest)

    return redirect('contest:archive')


@login_required
def register_group(request, group_id, contest):
    group = get_group_or_404(group_id)
    if user_info.has_group_ownership(request.user, group):
        register_group_impl(group, contest)
    else:
        logger.warning('Contest: User %s can not register group %s. Does not have ownership!'
            % (request.user.username, group_id))
    return redirect('contest:archive')

@login_required
def ask(request):
    try:
        contest = request.POST['contest']
        contest_obj = Contest.objects.get(pk = contest)
    except:
        logger.warning('Clarification: Can not create Clarification! Contest %s not found!'
            % contest)
        return redirect('contest:archive')

    if can_ask(request.user,contest_obj):
        if request.method == 'POST':
            form = ClarificationForm(request.POST)
            if form.is_valid():
                new_clarification = form.save()
                logger.info('Clarification: User %s create Clarification %s!'
                    % (request.user.username, new_clarification.id))
            return redirect('contest:contest',contest)
    return redirect('contest:archive')

@login_required
def reply(request):
    try:
        clarification = request.POST['clarification']
        instance = Clarification.objects.get(pk = clarification)
        contest_obj = instance.contest
        contest = contest_obj.id
    except:
        logger.warning('Clarification: User %s can not reply Clarification %s!'
            % (request.user.username, clarification.id))
        return redirect('contest:archive')

    if can_reply(request.user,contest_obj):
        if request.method == 'POST':
            form = ReplyForm(request.POST or None, instance = instance)
            if form.is_valid():
                replied_clarification = form.save()
                replied_clarification.reply_time = datetime.now()
                replied_clarification.save()
                logger.info('Clarification: User %s reply Clarification %s!'
                    % (request.user.username, replied_clarification.id))
            return redirect('contest:contest',contest)
    return redirect('contest:archive')

def download(request):
    what = request.POST.get('type')
    if what == 'scoreboard':
        scoreboard_type = request.POST.get('scoreboard_type')
        contest_id = request.POST.get('contest')
        scoreboard_file = get_scoreboard_csv(contest_id, scoreboard_type)
        return scoreboard_file
    raise Http404('file not found')
