from django.conf.urls import patterns, include, url
from django.contrib import admin
import views

urlpatterns = patterns('',
    url(r'^viewall_contest/(?P<group_id>[0-9]+)/$', views.get_running_contest, name='viewall_contest'),
    url(r'^viewall_archive/(?P<group_id>[0-9]+)/$', views.get_ended_contest, name='viewall_archive'),
    url(r'^viewall_announce/(?P<group_id>[0-9]+)/$', views.get_all_announce, name='viewall_announce'),
    url(r'^list/$', views.list, name='list'),
    url(r'^detail/(?P<group_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^new/$', views.new, name='new'),
)
