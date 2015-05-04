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
import time
from datetime import datetime

from django.shortcuts import render
from django.template import RequestContext
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.core.exceptions import SuspiciousOperation
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import resolve, reverse

from users.models import Notification
from utils.config_info import get_config

DEFAULT_THEME = get_config('theme_settings', 'default')

class CustomHttpExceptionMiddleware(object):
    def process_exception(self, request, exception):
        message = unicode(exception)
        if isinstance(exception, Http404):
            return render_index(request, 'index/404.html', {'error_message': message}, status=404)
        elif isinstance(exception, SuspiciousOperation):
            return render_index(request, 'index/400.html', {'error_message': message}, status=400)
        elif isinstance(exception, PermissionDenied):
            return render_index(request, 'index/403.html', {'error_message': message}, status=403)
        elif isinstance(exception, Exception):
            return render_index(request, 'index/500.html', {'error_message': message}, status=500)


def render_index(request, *args, **kwargs):
    """Helper to render index page with custom_proc"""
    # add context_instance keyword
    kwargs.update({'context_instance': RequestContext(request, processors=[custom_proc])})

    return render(request, *args, **kwargs)


def custom_proc(request):
    amount = Notification.objects.filter \
        (receiver=request.user, read=False).count()

    t = time.time()
    tstr = datetime.fromtimestamp(t).strftime('%Y/%m/%d %H:%M:%S')
    return {
        'tstr': tstr,
        'amount': amount,
        'default_theme': DEFAULT_THEME,
        'request': request
    }


def get_current_page(request, objects, slice=25):
    """Template for paging
        `objects` is the universe of the set.

        Returns a subset of `objects` according to the given page.
    """
    paginator = Paginator(objects, slice)  # Show 25 items per page by default
    page = request.GET.get('page')

    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        objects = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        objects = paginator.page(paginator.num_pages)

    return objects


def get_next_page(next_page):
    try:
        resolve(next_page)
    except:
        # Redirect to index if the given location can not be resolved.
        next_page = reverse('index:index')

    return next_page
