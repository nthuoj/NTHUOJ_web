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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render
from django.template import RequestContext
from index.views import custom_proc
from problem.models import Submission, SubmissionDetail
from status.templatetags.status_filters import show_detail
from users.forms import CodeSubmitForm
from users.models import User
from utils.log_info import get_logger
import re
# Create your views here.

logger = get_logger()


def regroup_submission(submissions):
    submission_groups = []
    for submission in submissions:
        submission_groups.append({
            'grouper': submission,
            'list': SubmissionDetail.objects.filter(sid=submission.id).order_by('-sid')
        })

    return submission_groups

def status(request, username=None):
    submissions = Submission.objects.all().order_by('-id')

    if username:
        try:
            user = User.objects.get(username=username)
            submissions = submissions.filter(user=user)
        except:
            raise Http404('User %s Not Found!' % username)

    paginator = Paginator(submissions, 25)  # Show 25 submissions per page
    page = request.GET.get('page')

    try:
        submissions = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        submissions = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        submissions = paginator.page(paginator.num_pages)

    submissions.object_list = regroup_submission(submissions.object_list)

    return render(
        request,
        'status/status.html',
        {'submissions': submissions},
        context_instance=RequestContext(request, processors=[custom_proc]))


def contest_status(request, contest):
    '''Return a status table of given contest'''
    problems = contest.problem.all()
    submissions = Submission.objects.filter(
        problem__in=problems,
        submit_time__gte=contest.start_time,
        submit_time__lte=contest.end_time).order_by('-id')[0:25]

    submissions = regroup_submission(submissions)
    table_content = str(render(request, 'status/statusTable.html', {'submissions': submissions}))
    # remove rendered response header
    table_content = re.sub('Content-Type: text/html; charset=utf-8', '', table_content)
    return table_content


def error_message(request, sid):

    try:
        submission = Submission.objects.get(id=sid)
        error_msg = submission.error_msg
        if show_detail(submission, request.user):
            return render(
                request,
                'status/error_message.html',
                {'error_message': error_msg})
        else:
            logger.warning('User %s attempt to view detail of SID %s' % (request.user, sid))
            return render(
                request,
                'index/500.html',
                {'error_message': 'You don\'t have permission to view detail of SID %s' % sid})

    except Submission.DoesNotExist:
        logger.warning('SID %s Not Found!' % sid)
        return render(
            request,
            'index/500.html',
            {'error_message': 'SID %s Not Found!' % sid})


@login_required()
def view_code(request, sid):
    try:
        submission = Submission.objects.get(id=sid)
        if show_detail(submission, request.user):
            f = open('%s%s.cpp' % (CodeSubmitForm.SUBMIT_PATH, sid), 'r')
            code = f.read()
            f.close()
            codesubmitform = CodeSubmitForm(
                initial={'code': code, 'pid': submission.problem.id})
            return render(request, 'users/submit.html', {'form': codesubmitform})
        else:
            logger.warning('User %s attempt to view detail of SID %s' % (request.user, sid))
            return render(
                request,
                'index/500.html',
                {'error_message': 'You don\'t have permission to view detail of SID %s' % sid})
    except Submission.DoesNotExist:
        logger.warning('SID %s Not Found!' % sid)
        return render(
            request,
            'index/500.html',
            {'error_message': 'SID %s Not Found!' % sid})
    except IOError:
        logger.warning('File %s.cpp Not Found!' % sid)
        return render(
            request,
            'index/500.html',
            {'error_message': 'File of SID %s Not Found!' % sid})
