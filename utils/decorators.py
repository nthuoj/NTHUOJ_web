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
IMPLIED, INCLUDING BUT NOsT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from django.conf import settings
from utils.user_info import validate_user


def subjudge_auth_required(view):
    """A decorator to ensure user has judge auth."""
    def f(request, *args, **kwargs):
        user = validate_user(request.user)
        if user.has_subjudge_auth():
            return view(request, *args, **kwargs)
        return HttpResponseRedirect(settings.LOGIN_URL)
    return f


def judge_auth_required(view):
    """A decorator to ensure user has judge auth."""
    def f(request, *args, **kwargs):
        user = validate_user(request.user)
        if user.has_judge():
            return view(request, *args, **kwargs)
        return HttpResponseRedirect(settings.LOGIN_URL)
    return f


def admin_auth_required(view):
    """A decorator to ensure user has judge auth."""
    def f(request, *args, **kwargs):
        user = validate_user(request.user)
        if user.has_admin_auth():
            return view(request, *args, **kwargs)
        return HttpResponseRedirect(settings.LOGIN_URL)
    return f
