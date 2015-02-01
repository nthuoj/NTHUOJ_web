from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext

from problem.models import Submission, SubmissionDetail
from index.views import custom_proc
# Create your views here.


def status(request):
    submission_details = SubmissionDetail.objects.all()
    submission_details = submission_details.extra(order_by=['-sid'])

    return render(
        request,
        'status/status.html',
        {'submission_details': submission_details},
        context_instance=RequestContext(request, processors=[custom_proc]))


def error_message(request, sid):
    submission = Submission.objects.filter(id=sid).first()
    error_msg = submission.error_msg

    return render(
        request,
        'status/error_message.html',
        {'error_message': error_msg})
