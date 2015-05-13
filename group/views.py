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
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, render
from django.utils import timezone
from django.forms.models import model_to_dict
from group.forms import GroupForm, GroupFormEdit, AnnounceForm
from group.models import Group, Announce
from utils.user_info import has_group_ownership, has_group_coownership
from utils.log_info import get_logger
from utils.render_helper import render_index, get_current_page
from users.models import User

logger = get_logger()

def get_group(group_id):
    try:
        group = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        logger.warning('Group: Can not edit group %s! Group does not exist!' % group_id)
        raise Http404('Group: Can not edit group %s! Group does not exist!' % group_id)
    return group

def get_announce(announce_id):
    try:
        announce = Announce.objects.get(id=announce_id)
    except Announce.DoesNotExist:
        logger.warning('Announce: Can not edit announce %s! Announce does not exist!' % announce_id)
        raise Http404('Announce: Can not edit announce %s! Announce does not exist!' % announce_id)
    return announce

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

    redirect_id = 1; #return to detail page.
    group = get_group(group_id)
    show_number = 5; #number for brief list to show in group detail page.
    all_contest = group.trace_contest.order_by('-start_time')
    annowence_list = group.announce.all()
    student_list = group.member.order_by('user_level')
    coowner_list = group.coowner.all()
    owner = group.owner
    form = AnnounceForm()

    if not request.user.is_anonymous():
        user_is_owner = has_group_ownership(request.user, group)
        user_is_coowner = has_group_coownership(request.user, group)
        user_has_admin_auth = request.user.has_admin_auth()
    else: 
        user_is_owner = False
        user_is_coowner = False
        user_has_admin_auth = False
    
    user_has_no_auth = not user_is_owner and not user_is_owner and not user_has_admin_auth

    running_contest_list = []
    ended_contest_list = []
    now = timezone.now()
    for contest in all_contest:
        if contest.start_time < now and contest.end_time > now:
            running_contest_list.append(contest)
        elif contest.end_time < now:
            ended_contest_list.append(contest)

    student_list = get_current_page(request, student_list)

    return render_index(
        request, 'group/groupDetail.html', {
            'running_contest_list': running_contest_list[0:show_number],
            'ended_contest_list': ended_contest_list[0:show_number],
            'announce_list': annowence_list,
            'coowner_list': coowner_list,
            'owner': owner,
            'student_list': student_list,
            'group_name': group.gname, 
            'group_description': group.description,
            'group_id': group.id,
            'user_has_no_auth': user_has_no_auth,
            'form': form,
            'redirect_id' : redirect_id,
        })

def list(request):
    all_group = Group.objects.order_by('id')
    if request.user.is_anonymous():
        my_group = []
    else:
        my_group = Group.objects.filter(Q(member__username__contains=request.user.username) \
                                        |Q(owner__username=request.user.username) \
                                        |Q(coowner__username=request.user.username) \
                                        ).distinct().order_by('id')
    
    all_group = get_current_page(request, all_group)
    my_group = get_current_page(request, my_group)

    return render_index(
        request,'group/groupList.html', {
            'all_group_list': all_group,
            'my_group_list': my_group,
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

##Announce
@login_required
def add_announce(request, group_id):
    group = get_group(group_id)

    if has_group_ownership(request.user, group) or has_group_coownership(request.user, group) or \
       request.user.has_admin_auth():
        if request.method == 'POST':
            form = AnnounceForm(request.POST)
            if form.is_valid():
                new_announce = form.save()
                group.announce.add(new_announce)
                logger.info('Announce: User %s add Announce %s!' % (request.user.username, new_announce.id))
                return HttpResponseRedirect(reverse('group:detail', kwargs={'group_id': group_id}))
            else:
                return HttpResponseRedirect(reverse('group:detail', kwargs={'group_id': group_id}))
    else:
        raise PermissionDenied

@login_required
def delete_announce(request, announce_id, group_id):
    group = get_group(group_id)

    if has_group_ownership(request.user, group) or has_group_coownership(request.user, group) or \
       request.user.has_admin_auth():  
        try:
            Announce.objects.get(id=announce_id).delete()
            return HttpResponseRedirect(reverse('group:detail', kwargs={'group_id': group_id}))
        except Announce.objects.get(id=announce_id).DoesNotExist:
            logger.info('Announce: already deleted %s!' % announce_id)
            raise Http404('Announce: already deleted %s!' % announce_id)
    else:
        raise PermissionDenied

@login_required
def edit_announce(request, announce_id, group_id, redirect_id):
    announce = get_announce(announce_id)
    group = get_group(group_id)
    user_is_owner = has_group_ownership(request.user, group)
    user_is_coowner = has_group_coownership(request.user, group)
    if user_is_owner or user_is_coowner or request.user.has_admin_auth():
        if request.method == 'GET':
            announce_dic = model_to_dict(announce)
            form = AnnounceForm(initial=announce_dic)
            logger.info('Now I GETT!!!!!!!')
            return render_index(
                request,'group/editAnnounce.html', {
                    'form':form,
                    'group_id': group.id,
                    'announce_id': announce_id,
                    'user_is_owner': user_is_owner,
                    'user_is_coowner': user_is_coowner,
                    'user_has_admin_auth': request.user.has_admin_auth(),
                })
        if request.method == 'POST':
            logger.info('Now I PosTTTTTT!!!!!')
            form = AnnounceForm(request.POST, instance=announce)
            if form.is_valid():
                modified_announce = form.save()
                logger.info('redirect_id: %s!' % redirect_id)
                if redirect_id == '1':
                    return HttpResponseRedirect(reverse('group:detail', kwargs={'group_id': group_id}))
                elif redirect_id == '0' :
                    return HttpResponseRedirect(reverse('group:viewall_announce', kwargs={'group_id': group_id}))
            else:
                 return render_index(
                        request,'group/editAnnounce.html', {
                        'form':form,
                        'user_is_owner': user_is_owner,
                        'user_is_coowner': user_is_coowner,
                        'user_has_admin_auth': request.user.has_admin_auth(),
                    })
        else:
            logger.info('aid:%s gid:%s method:%s bool:%s' % (announce_id,group_id,request.method, request.method=='GET'))
    else:
        raise PermissionDenied
