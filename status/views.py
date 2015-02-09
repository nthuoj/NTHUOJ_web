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
from django.template import RequestContext

from problem.models import Submission, SubmissionDetail
from index.views import custom_proc
from utils.log_info import get_logger
# Create your views here.

logger = get_logger()


def status(request):
    submissions = Submission.objects.order_by('-id')[0:50]
    submissions_id = map(lambda submission: submission.id, submissions)
    submission_details = SubmissionDetail. \
        objects.filter(sid__in=submissions_id).order_by('-sid')

    return render(
        request,
        'status/status.html',
        {'submission_details': submission_details},
        context_instance=RequestContext(request, processors=[custom_proc]))


def error_message(request, sid):
    try:
        submission = Submission.objects.get(id=sid)
        error_msg = submission.error_msg
        return render(
            request,
            'status/error_message.html',
            {'error_message': error_msg})

    except Submission.DoesNotExist:
        logger.warning('SID %s Not Found!' % sid)
        return render(
            request,
            'index/500.html',
            {'error_message': 'SID %s Not Found!' % sid})
