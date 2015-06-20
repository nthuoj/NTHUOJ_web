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
from users.models import User
from group.forms import GroupForm, GroupFormEdit, AnnounceForm
from group.models import Group, Announce
from utils.user_info import has_group_ownership, has_group_coownership
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from utils.render_helper import render_index
from utils.log_info import get_logger

from group.getter import get_group
from group.getter import get_announce

logger = get_logger()

##Announce
@login_required
def add_announce(request, group_id):
    group = get_group(group_id)

    if has_group_ownership(request.user, group) or has_group_coownership(request.user, group):
        if request.method == 'POST':
            form = AnnounceForm(request.POST)
            if form.is_valid():
                new_announce = form.save()
                group.announce.add(new_announce)
                logger.info('Announce: User %s add Announce %s!' % (request.user.username, new_announce.id))
            return HttpResponseRedirect(reverse('group:detail', kwargs={'group_id': group_id}))
    else:
        raise PermissionDenied

@login_required
def delete_announce(request, announce_id, group_id, redirect_page):
    group = get_group(group_id)

    if has_group_ownership(request.user, group) or has_group_coownership(request.user, group):  
        get_announce(announce_id).delete()
        logger.info('Announce: User %s delete Announce %s!' % (request.user.username, announce_id))
        if redirect_page == 'detail':
            return HttpResponseRedirect(reverse('group:detail', kwargs={'group_id': group_id}))
        else : #redirect_page=='viewall'
            return HttpResponseRedirect(reverse('group:viewall_announce', kwargs={'group_id': group_id}))
    else:
        raise PermissionDenied

@login_required
def edit_announce(request, announce_id, group_id, redirect_page):
    announce = get_announce(announce_id)
    group = get_group(group_id)
    user_is_owner = has_group_ownership(request.user, group)
    user_is_coowner = has_group_coownership(request.user, group)
    if user_is_owner or user_is_coowner:
        if request.method == 'GET':
            announce_dic = model_to_dict(announce)
            form = AnnounceForm(initial=announce_dic)
            return render_index(
                request,'group/editAnnounce.html', {
                    'form':form,
                    'group_id': group.id,
                    'announce_id': announce_id,
                })
        if request.method == 'POST':
            form = AnnounceForm(request.POST, instance=announce)
            if form.is_valid():
                modified_announce = form.save()
                logger.info('Announce: Announce %s has been changed!' % (announce.id))
                if redirect_page == 'detail':
                    return HttpResponseRedirect(reverse('group:detail', kwargs={'group_id': group_id}))
                else : #redirect_page=='viewall'
                    return HttpResponseRedirect(reverse('group:viewall_announce', kwargs={'group_id': group_id}))
            else:
                 return render_index(
                        request,'group/editAnnounce.html', {
                        'form':form,
                    })
    else:
        raise PermissionDenied
