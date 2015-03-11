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
from django.shortcuts import render
from index.views import custom_proc
from utils.log_info import get_logger
from django.conf import settings
from users.forms import CodeSubmitForm
from django.template import RequestContext
from problem.models import Submission, SubmissionDetail
from django.contrib.auth.decorators import login_required
from status.templatetags.status_filters import show_detail

# Create your views here.

logger = get_logger()


def regroup_submission(submissions, submission_details):
    submission_groups = []
    for submission in submissions:
        submission_groups.append({
            'grouper': submission,
            'list': submission_details.filter(sid=submission)
        })

    return submission_groups


def status(request):
    submissions = Submission.objects.order_by('-id')[0:50]
    submissions_id = map(lambda submission: submission.id, submissions)
    submission_details = SubmissionDetail. \
        objects.filter(sid__in=submissions_id).order_by('-sid')

    submissions = regroup_submission(submissions, submission_details)

    return render(
        request,
        'status/status.html',
        {'submissions': submissions},
        context_instance=RequestContext(request, processors=[custom_proc]))


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
