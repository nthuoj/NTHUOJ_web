"""
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
"""
import re

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render
from django.core.exceptions import PermissionDenied

from problem.models import Submission, SubmissionDetail
from status.templatetags.status_filters import show_detail
from users.forms import CodeSubmitForm
from users.models import User
from utils.log_info import get_logger
from utils.file_info import get_extension
from utils.render_helper import render_index, get_current_page

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
            raise Http404('User %s not found' % username)

    submissions = get_current_page(request, submissions)

    submissions.object_list = regroup_submission(submissions.object_list)

    return render_index(request, 'status/status.html', {'submissions': submissions})


def contest_status(request, contest):
    """Return a status table of given contest"""
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


@login_required()
def error_message(request, sid):
    try:
        submission = Submission.objects.get(id=sid)
        error_msg = submission.error_msg
        if show_detail(submission, request.user):
            return render_index(request, 'status/errorMessage.html', {'error_message': error_msg})
        else:
            logger.warning('User %s attempt to view detail of SID %s' % (request.user, sid))
            raise PermissionDenied("You don't have permission to view detail of SID %s" % sid)

    except Submission.DoesNotExist:
        logger.warning('SID %s Not Found!' % sid)
        raise Http404('SID %s Not Found!' % sid)


@login_required()
def view_code(request, sid):
    try:
        submission = Submission.objects.get(id=sid)
        filename = '%s.%s' % (sid, get_extension(submission.language))
        if show_detail(submission, request.user):
            f = open('%s%s' % (CodeSubmitForm.SUBMIT_PATH, filename), 'r')
            code = f.read()
            f.close()
            codesubmitform = CodeSubmitForm(
                initial={'code': code, 'pid': submission.problem.id, 'language': submission.language})
            return render_index(request, 'users/submit.html', {'form': codesubmitform})
        else:
            logger.warning('User %s attempt to view detail of SID %s' % (request.user, sid))
            raise PermissionDenied("You don't have permission to view detail of SID %s" % sid)
    except Submission.DoesNotExist:
        logger.warning('SID %s Not Found!' % sid)
        raise Http404('SID %s Not Found!' % sid)
    except IOError:
        logger.warning('File %s Not Found!' % filename)
        raise Http404('File %s Not Found!' % filename)
