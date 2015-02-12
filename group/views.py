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
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, render
from group.models import Group
from django.utils import timezone
from general_tools import log
from group.forms import GroupForm
from django.http import HttpResponseRedirect


logger = log.get_logger()

def get_running_contest(request, group_id):
        
        try:
            group = Group.objects.get(id = group_id)
        except:
            logger.warning('Group: group does not exist - gid: %s!' % group_id)
            raise Http404('Group does not exist')

        all_contest = group.trace_contest.all()
        all_running_contest_list = []
        now = timezone.now()

        for contest in all_contest:
            if contest.start_time < now and contest.end_time > now:
                    all_running_contest_list.append(contest)

        return render(
            request, 'group/viewall.html', {
                'data_list': all_running_contest_list, 
                'title': 'running contest',
                'list_type': 'runContest',
            })

def get_ended_contest(request, group_id):
        
        try:
            group = Group.objects.get(id = group_id)
        except:
            logger.warning('Group: group does not exist - gid: %s!' % group_id)
            raise Http404('Group does not exist')

        all_contest = group.trace_contest.all()
        all_ended_contest_list = []
        now = timezone.now()

        for contest in all_contest:
            if contest.end_time < now:
                all_ended_contest_list.append(contest)

        return render(
            request, 'group/viewall.html', {
                'data_list': all_ended_contest_list, 
                'title': 'ended contest',
                'list_type': 'endContest',
            })

def get_all_announce(request, group_id):

        try:
            group = Group.objects.get(id = group_id)
        except:
            logger.warning('Group: group does not exist - gid: %s!' % group_id)
            raise Http404('Group does not exist')

        all_announce_list = group.announce.all()
        return render(
            request, 'group/viewall.html', {
                'data_list': all_announce_list, 
                'title': 'announce',
                'list_type': 'announce',
            })

    
def detail(request, group_id):
    
    try:
        group = Group.objects.get(id = group_id)
    except:
        logger.warning('Group: group does not exist - gid: %s!' % group_id)
        raise Http404('Group does not exist')

    all_contest = group.trace_contest.all()[0:5]
    annowence_list = group.announce.all()[0:5]
    student_list = group.member.all()
    coowner_list = group.coowner.all()
    owner = group.owner

    running_contest_list = []
    ended_contest_list = []
    now = timezone.now()
    for contest in all_contest:
        if contest.start_time < now and contest.end_time > now:
            running_contest_list.append(contest)
        elif contest.end_time < now:
            ended_contest_list.append(contest)

    return render(
        request, 'group/groupDetail.html', {
            'rc_list': running_contest_list, 
            'ec_list': ended_contest_list,
            'an_list': annowence_list,
            'coowner_list': coowner_list,
            'owner': owner,
            's_list': student_list,
            'group_name': group.gname, 
            'group_description': group.description,
            'group_id': group.id,
        })


def list(request):

    group_list = Group.objects.order_by('-creation_time')
    return render(
        request,'group/groupList.html', {
            'g_list': group_list
        })

def new(request):
    if request.method == 'GET':
            form = GroupForm()
            return render(request,'group/editGroup.html',{'form':form})
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            new_group = form.save()
            return HttpResponseRedirect('/group/list')
        else:
            raise Http404('Cannot create group! Info is blank!')
