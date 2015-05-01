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
SOFTWARE.'''
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from django.forms.models import model_to_dict
from group.forms import GroupForm, GroupFormEdit
from group.models import Group
from utils.user_info import has_group_ownership
from utils.log_info import get_logger
from utils.render_helper import render_index

logger = get_logger()

def get_group(group_id):
    try:
        group = Group.objects.get(id = group_id)
    except Group.DoesNotExist:
        logger.warning('Group: Can not edit group %s! Group is not exist!' % group_id)
        return render(
            request,
            'index/404.html',
            {'error_message': 'Group: Can not edit group %s! Group is not exist!' % group_id})
    return group

def get_running_contest(request, group_id):

    group = get_group(group_id)

    all_contest = group.trace_contest.all()
    all_running_contest_list = []
    now = timezone.now()

    for contest in all_contest:
        if contest.start_time < now and contest.end_time > now:
            all_running_contest_list.append(contest)

    return render_index(
        request, 'group/viewall.html', {
            'data_list': all_running_contest_list,
            'title': 'running contest',
            'list_type': 'runContest',
        })

def get_ended_contest(request, group_id):

    group = get_group(group_id)

    all_contest = group.trace_contest.all()
    all_ended_contest_list = []
    now = timezone.now()

    for contest in all_contest:
        if contest.end_time < now:
            all_ended_contest_list.append(contest)

    return render_index(
        request, 'group/viewall.html', {
            'data_list': all_ended_contest_list,
            'title': 'ended contest',
            'list_type': 'endContest',
        })

def get_all_announce(request, group_id):

    group = get_group(group_id)

    all_announce_list = group.announce.all()
    return render_index(
        request, 'group/viewall.html', {
            'data_list': all_announce_list,
            'title': 'announce',
            'list_type': 'announce',
        })


def detail(request, group_id):

    group = get_group(group_id)
    show_number = 5; #number for brief list to show in group detail page.
    all_contest = group.trace_contest.all()
    annowence_list = group.announce.all()
    student_list = group.member.order_by('user_level')
    coowner_list = group.coowner.all()
    owner = group.owner
    user_is_owner = has_group_ownership(request.user, group)

    running_contest_list = []
    ended_contest_list = []
    now = timezone.now()
    for contest in all_contest:
        if contest.start_time < now and contest.end_time > now:
            running_contest_list.append(contest)
        elif contest.end_time < now:
            ended_contest_list.append(contest)

    return render_index(
        request, 'group/groupDetail.html', {
            'rc_list': running_contest_list[0:show_number],
            'ec_list': ended_contest_list[0:show_number],
            'an_list': annowence_list,
            'coowner_list': coowner_list,
            'owner': owner,
            's_list': student_list,
            'group_name': group.gname,
            'group_description': group.description,
            'group_id': group.id,
            'user_is_owner': user_is_owner,
        })


def list(request):

    all_group_list = Group.objects.order_by('-creation_time')
    unsorted_group_list = Group.objects.filter(member__username__contains=request.user.username)
    my_group_list = unsorted_group_list.order_by('-creation_time')
    return render_index(
        request,'group/groupList.html', {
            'a_g_list': all_group_list,
            'm_g_list': my_group_list,
        })

def new(request):

    if request.user.has_judge_auth():
        if request.method == 'GET':
            form = GroupForm()
            return render_index(request,'group/editGroup.html',{'form':form})
        if request.method == 'POST':
            form = GroupForm(request.POST)
            if form.is_valid():
                new_group = form.save()
                logger.info('Group: Create a new group %s!' % new_group.id)
                return HttpResponseRedirect('/group/list')
            else:
                return render(
                    request,
                    'index/404.html',
                    {'error_message': 'Cannot create group! Info is blank!'})
    else:
        raise PermissionDenied

def delete(request, group_id):

    if request.user.has_judge_auth():
        get_group(group_id)
        deleted_gid = group.id
        group.delete()
        logger.info('Group: Delete group %s!' % deleted_gid)
        return HttpResponseRedirect('/group/list')
    else:
        raise PermissionDenied

def edit(request, group_id):

        group = get_group(group_id)

        coowner_list = []
        all_coowner = group.coowner.all()
        for coowner in all_coowner:
            coowner_list.append(coowner.username)

        if request.user.username == group.owner.username or \
           request.user.username in coowner_list:
            if request.method == 'GET':
                group_dic = model_to_dict(group)
                form = GroupFormEdit(initial = group_dic)
                return render_index(request,'group/editGroup.html',{'form':form})
            if request.method == 'POST':
                form = GroupFormEdit(request.POST, instance = group)
                if form.is_valid():
                    modified_group = form.save()
                    logger.info('Group: Modified group %s!' % modified_group.id)
                    return HttpResponseRedirect('/group/detail/%s' % modified_group.id)
        else:
            raise PermissionDenied
