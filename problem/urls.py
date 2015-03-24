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
from django.conf.urls import patterns, include, url
from problem import views

urlpatterns = patterns('',
    url(r'^$', views.problem, name='problem'),  # /problem  : problem panel
    url(r'^volume/$', views.volume, name='volume'),
    url(r'^(?P<pid>\d+)/$', views.detail, name='detail'),   # /problem/10 : detail of problem 10
    url(r'^(?P<pid>\d+)/edit/$', views.edit, name='edit'),  # /problem/10/edit : edit problem 10
    url(r'^new/$', views.new, name='new'), # /problem/new : create new problem
    url(r'^preview/$', views.preview, name='new'),  # /problem/preview  :  preview problem when editting
)
