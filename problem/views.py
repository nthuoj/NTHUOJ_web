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
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied

from users.models import User
from problem.models import Problem, Tag, Testcase
from problem.forms import ProblemForm
from problem.problem_info import *
from utils import log_info

import os
import json

logger = log_info.get_logger()

# Create your views here.
def problem(request):
    can_add_problem = False
    my_problem = Problem.objects.filter(owner=request.user)
    if request.user.is_anonymous():
        can_add_problem = False
    else:
        can_add_problem = request.user.has_subjudge_auth()
    all_problem = get_problem_list(request.user)

    return render(request, 'problem/panel.html', 
                  {'my_problem': my_problem, 'all_problem': all_problem, 
                   'can_add_problem': can_add_problem})

def volume(request):
    problem_id=[]
    if Problem.objects.count() != 0:
        problems = Problem.objects.latest('id')
        volume_number = (problems.id - 1) // 100
        for i in range(1,volume_number + 2):
            start_id = ((i - 1) * 100 + 1)
            if problems.id < i * 100:
                end_id = problems.id
            else:
                end_id = i * 100
            problem_id.append(str(start_id) + ' ~ ' + str(end_id))

    return render(request, 'problem/volume.html', {'problem_id':problem_id})

def detail(request, pid):
    user = request.user
    try:
        problem = Problem.objects.get(pk=pid)
    except Problem.DoesNotExist:
        logger.warning('problem %s not found' % (pid))
        raise Http404('problem %s does not exist' % (pid))
    problem = get_problem(problem)
    return render(request, 'problem/detail.html', {'problem': problem})

def edit(request, pid):
    if request.user.is_anonymous():
        raise PermissionDenied()
    try:
        problem = Problem.objects.get(pk=pid)
        if not request.user.is_admin or request.user != problem.owner:
            raise PermissionDenied()
    except Problem.DoesNotExist:
        logger.warning("problem %s does not exist" % (pid))
        raise Http404("problem %s does not exist" % (pid))
    testcase = Testcase.objects.filter(problem=problem)
    tags = problem.tags.all()
    if request.method == 'GET':
        form = ProblemForm(instance=problem)
    if request.method == 'POST':
        form = ProblemForm(request.POST, instance=problem)
        if form.is_valid():
            problem = form.save()
            problem.description = request.POST['description']
            problem.input= request.POST['input_description']
            problem.output = request.POST['output_description']
            problem.sample_in = request.POST['sample_input']
            problem.sample_out = request.POST['sample_output']
            problem.save()
            logger.info('edit problem, pid = %d' % (problem.pk))
            return redirect('/problem/%d' % (problem.pk))
    if not request.user.is_admin:
        del form.fields['owner']
    return render(request, 'problem/edit.html', 
                  {'form': form, 'pid': pid, 'is_new': False,
                   'tags': tags, 'description': problem.description,
                   'input': problem.input, 'output': problem.output,
                   'sample_in': problem.sample_in, 'sample_out': problem.sample_out,
                   'testcase': testcase })

def new(request):
    if request.user.is_anonymous():
        raise PermissionDenied()
    if not request.user.has_subjudge_auth():
        logger.warning("user %s has no auth to add new problem" % (request.user))
        raise Http404("you can't add new problem")
    if request.method == 'GET':
        form = ProblemForm()
    if request.method == 'POST':
        form = ProblemForm(request.POST)
        if form.is_valid():
            problem = form.save()
            problem.description = request.POST['description']
            problem.input= request.POST['input_description']
            problem.output = request.POST['output_description']
            problem.sample_in = request.POST['sample_input']
            problem.sample_out = request.POST['sample_output']
            problem.save()
            logger.info('post new problem, pid = %d' % (problem.pk))
            return redirect('/problem/%d' % (problem.pk))
    if not request.user.is_admin:
        del form.fields['owner']
    return render(request, 'problem/edit.html', 
                    { 'form': form, 'owner': request.user, 'is_new': True })

def tag(request, pid):
    if request.method == "POST":
        tag = request.POST['tag']
        try:
            problem = Problem.objects.get(pk=pid)
        except Problem.DoesNotExist:
            logger.warning("problem %s does not exist" % (pid))
            raise Http404("problem %s does not exist" % (pid))
        if not problem.tags.filter(tag_name=tag).exists():
            logger.info("add new tag '%s' to problem %s" % (tag, pid))
            new_tag, created = Tag.objects.get_or_create(tag_name=tag)
            problem.tags.add(new_tag)
            problem.save()
            return HttpResponse(json.dumps({'tag_id': new_tag.pk}),
                                content_type="application/json")
        return HttpRequestBadRequest()
    return HttpResponse()

def delete_tag(request, pid, tag_id):
    try:
        problem = Problem.objects.get(pk=pid)
        tag = Tag.objects.get(pk=tag_id)
    except Problem.DoesNotExist:
        logger.warning("problem %s does not exist" % (pid))
        raise Http404("problem %s does not exist" % (pid))
    except Tag.DoesNotExist:
        logger.warning("tag %s does not exist" % (tag_id))
        raise Http404("tag %s does not exist" % (tag_id))
    if not request.user.is_admin and request.user != problem.owner:
        raise PermissionDenied()
    logger.info("tag %d deleted" % (tag.pk))
    problem.tags.remove(tag)
    return HttpResponse()

def testcase(request, pid, tid=None):
    if request.method == 'POST':
        try:
            problem = Problem.objects.get(pk=pid)
        except Problem.DoesNotExist:
            logger.warning("problem %s does not exist" % (pid))
            raise Http404("problem %s does not exist" % (pid))
        if tid == None:
            testcase = Testcase()
            testcase.problem = problem
        else:
            try:
                testcase = Testcase.objects.get(pk=tid)
            except Testcase.DoesNotExist:
                logger.warning("testcase %s does not exist" % (tid))
                raise Http404("testcase %s does not exist" % (tid))
            if testcase.problem != problem:
                logger.warning("testcase %s does not belong to problem %s" % (tid, pid))
                raise Http404("testcase %s does not belong to problem %s" % (tid, pid))
        if 'time_limit' in request.POST:
            testcase.time_limit = request.POST['time_limit']
            testcase.memory_limit = request.POST['memory_limit']
            testcase.save()
            logger.info("testcase saved, tid = %s" % (testcase.pk))
            return HttpResponse(json.dumps({'tid': testcase.pk}), content_type="application/json")
    return HttpResponse()

def delete_testcase(request, pid, tid):
    try:
        problem = Problem.objects.get(pk=pid)
        testcase = Testcase.objects.get(pk=tid)
    except Problem.DoesNotExist:
        logger.warning("problem %s does not exist" % (pid))
        raise Http404("problem %s does not exist" % (pid))
    except Testcase.DoesNotExist:
        logger.warning("testcase %s does not exist" % (tid))
        raise Http404("testcase %s does not exist" % (tid))
    if not request.user.is_admin and request.user != problem.owner:
        raise PermissionDenied
    logger.info("testcase %d deleted" % (testcase.pk))
    testcase.delete()
    return HttpResponse()

def delete_problem(request, pid):
    try:
        problem = Problem.objects.get(pk=pid)
    except Problem.DoesNotExist:
        logger.warning("problem %s does not exist" % (pid))
        raise Http404("problem %s does not exist" % (pid))
    if not request.user.is_admin and request.user != problem.owner:
        raise PermissionDenied
    logger.info("problem %d deleted" % (problem.pk))
    problem.delete()
    return redirect('/problem/')

def preview(request):
    return render(request, 'problem/preview.html')
