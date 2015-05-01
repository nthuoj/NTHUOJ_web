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
    url(r'^$', views.problem, name='problem'),
    # /problem  : problem panel
    url(r'^(?P<pid>\d+)/$', views.detail, name='detail'),
    # /problem/10 : detail of problem 10
    url(r'^(?P<pid>\d+)/delete/$', views.delete_problem, name='delete_problem'),
    # /problem/10/delete : delete problem 10
    url(r'^(?P<pid>\d+)/edit/$', views.edit, name='edit'),
    # /problem/10/edit : edit problem 10
    url(r'^new/$', views.new, name='new'),
    # /problem/new : create new problem
    url(r'^(?P<pid>\d+)/tag/$', views.tag, name='tag'),
    # post /problem/10/tag: add tag to problem 10
    url(r'^(?P<pid>\d+)/tag/(?P<tag_id>\d+)/delete/$', views.delete_tag, name='delete_tag'),
    # /problem/10/tag/123/delete/: delete tag id=123 of problem 10
    url(r'^(?P<pid>\d+)/testcase/$', views.testcase, name='testcase'),
    # post /problem/10/testcase: add testcase to problem 10
    url(r'^(?P<pid>\d+)/testcase/(?P<tid>\d+)/$', views.testcase, name='testcase'),
    # post /problem/10/testcase/123: update testcase 123 of problem 10
    url(r'^(?P<pid>\d+)/testcase/(?P<tid>\d+)/delete/$', 
        views.delete_testcase, name='delete_testcase'),
    # /problem/10/testcase/123/delete/: delete testcase 123 of problem 10
    url(r'^preview/$', views.preview, name='preview'),
    # /problem/preview  :  preview problem when editting
    url(r'^testcase/(?P<filename>.+)/$', views.download_testcase, name="download_testcase"),
    url(r'^partial/(?P<filename>.+)/$', views.download_partial, name="download_partial"),
    url(r'^special/(?P<filename>.+)/$', views.download_special, name="download_special"),
)
