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
from django.template import RequestContext

def render_404(request, message):
    '''Helper to render 404 page

    example: 
        render500(request, 'Page not found')
    '''
    return render(request, 'index/404.html',
        {'error_message': message}, status=500)


def render_500(request, message):
    '''Helper to render 500 page

    example: 
        render500(request, 'Request query does not exist')
    '''
    return render(request, 'index/500.html',
        {'error_message': message}, status=500)

def render_index(request, *args, **kwargs):
    '''Helper to render index page with custom_proc'''
    # add context_instance keyword
    kwargs.update({'context_instance': RequestContext(request, processors=[custom_proc])})

    return render(request, *args, **kwargs)
