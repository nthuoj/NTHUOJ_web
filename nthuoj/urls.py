from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^contest/', include('contest.urls')),
    url(r'^submit/$', 'users.views.submit'),
    url(r'^profile/$', 'users.views.profile'),
)
