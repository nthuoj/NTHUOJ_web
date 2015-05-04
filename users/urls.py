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
from django.conf.urls import patterns, include, url
from axes.decorators import watch_login

import views

urlpatterns = patterns('',
    #url(r'^list/$', views.user_list, name='list'),
    url(r'^submit/$', views.submit, name='submit'),
    url(r'^create/$', views.user_create, name='create'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^forget_password/$', views.user_forget_password, name='forget_password'),
    url(r'^submit/(?P<pid>\d+)$', views.submit, name='submit'),
    url(r'^notification/$', views.user_notification, name='notification'),
    url(r'^profile/(?P<username>\w+)$', views.user_profile, name='profile'),
    url(r'^readify/(?P<read_id>.*)/(?P<current_tab>.*)$', views.user_readify),
    url(r'^notification/(?P<current_tab>\w+)/$', views.user_notification, name='tab'),
    url(r'^confirm/(?P<activation_key>\w+)/', views.register_confirm, name='confirm'),
    url(r'^forget_password_confirm/(?P<activation_key>\w+)/',
        views.forget_password_confirm, name='forget_password_confirm'),
    url(r'^delete_notification/(?P<delete_ids>.*)/(?P<current_tab>.*)$', views.user_delete_notification),
    url(r'^block_wrong_tries/$', views.user_block_wrong_tries, name='block_wrong_tries'),

)
