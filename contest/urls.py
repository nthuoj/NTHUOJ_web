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
from django.conf.urls import patterns, url
from contest import views

urlpatterns = patterns('contest.views',
    #default contest archive
    url(r'^$',views.archive,name='archive'),
    #get contest info modal
    url(r'^info/(?P<cid>\d+)/$',views.contest_info,name='contest_info'),
    #get contest register modal
    url(r'^register-page/(?P<cid>\d+)/$',views.register_page,name='register_page'),
    #create new contest
    url(r'^new/$',views.new,name='new'),
    #edit existing contest
    url(r'^edit/(?P<cid>\d+)/$',views.edit,name='edit'),
    #delete contest
    url(r'^delete/(?P<cid>\d+)/$',views.delete,name='delete'),
    #detail of contest
    url(r'^(?P<cid>\d+)/$',views.contest,name='contest'),
    #user register contest
    url(r'^register/(?P<cid>\d+)/$',views.register,name='register'),
    #user create new clarification
    url(r'^ask/$',views.ask,name='ask'),
    url(r'^reply/$',views.reply,name='reply'),
    url(r'^download/$',views.download,name='download'),
)
