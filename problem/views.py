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
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from users.models import User
from problem.models import Problem, Tag, Testcase
from problem.forms import ProblemForm
from problem.problem_info import *
from utils import log_info
from utils.render_helper import render_index

import os
import json

logger = log_info.get_logger()

# Create your views here.
def problem(request):
    can_add_problem = False
    if request.user.is_anonymous():
        can_add_problem = False
    else:
        can_add_problem = request.user.has_subjudge_auth()
    all_problem_list = get_problem_list(request.user)
    paginator = Paginator(all_problem_list, 10)
    if "page" in request.GET:
        page = request.GET["page"]
    else:
        page = 1
    try:
        all_problem = paginator.page(page)
    except PageNotAnInteger:
        all_problem = paginator.page(1)
    except EmptyPage:
        all_problem = paginator.page(paginator.num_pages)
    for p in all_problem:
        if p.total_submission != 0:
            p.pass_rate = float(p.ac_count) / float(p.total_submission) * 100.0
            p.not_pass_rate = 100.0 - p.pass_rate

    return render_index(request, 'problem/panel.html', 
                  {'all_problem': all_problem, 
                   'can_add_problem': can_add_problem})

def detail(request, pid):
    user = request.user
    try:
        problem = Problem.objects.get(pk=pid)
    except Problem.DoesNotExist:
        logger.warning('problem %s not found' % (pid))
        raise Http404('problem %s does not exist' % (pid))
    problem.testcase = get_testcase(problem)
    return render_index(request, 'problem/detail.html', {'problem': problem})

@login_required
def edit(request, pid=None):
    if pid is not None:
        is_new = False
        try:
            problem = Problem.objects.get(pk=pid)
            if not request.user.is_admin and request.user != problem.owner:
                logger.warning("user %s has no permission to edit problem %s" % (request.user, pid))
                raise PermissionDenied()
        except Problem.DoesNotExist:
            logger.warning("problem %s does not exist" % (pid))
            raise Http404("problem %s does not exist" % (pid))
        testcase = Testcase.objects.filter(problem=problem)
        tags = problem.tags.all()
    else:
        is_new = True
    if request.method == 'GET':
        if is_new:
            form = ProblemForm(initial={'owner': request.user.username})
        else:
            form = ProblemForm(instance=problem,
                               initial={'owner': request.user.username})
    if request.method == 'POST':
        if is_new:
            form = ProblemForm(request.POST,
                               initial={'owner': request.user.username})
        else:
            form = ProblemForm(request.POST,
                               instance=problem,
                               initial={'owner': request.user.username})
        if form.is_valid():
            problem = form.save()
            problem.description = request.POST['description']
            problem.input= request.POST['input_description']
            problem.output = request.POST['output_description']
            problem.sample_in = request.POST['sample_in']
            problem.sample_out = request.POST['sample_out']
            problem.save()
            logger.info('edit problem, pid = %d' % (problem.pk))
            return redirect('/problem/%d' % (problem.pk))
    if not request.user.is_admin:
        del form.fields['owner']
    if is_new:
        return render_index(request, 'problem/edit.html', 
                    { 'form': form, 'owner': request.user, 'is_new': True })
    else:
        return render_index(request, 'problem/edit.html', 
                  {'form': form, 'pid': pid, 'is_new': False,
                   'tags': tags, 'description': problem.description,
                   'input': problem.input, 'output': problem.output,
                   'sample_in': problem.sample_in, 'sample_out': problem.sample_out,
                   'testcase': testcase })

@login_required
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

@login_required
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

@login_required
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
            return HttpResponse(json.dumps({'tid': testcase.pk}), 
                                content_type="application/json")
    return HttpResponse()

@login_required
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
    form = ProblemForm(request.GET)
    problem = form.save()
    problem.description = request.GET['description']
    problem.input= request.GET['input_description']
    problem.output = request.GET['output_description']
    problem.sample_in = request.GET['sample_in']
    problem.sample_out = request.GET['sample_out']
    return render_index(request, 'problem/preview.html', {'problem': problem, 'preview': True})
