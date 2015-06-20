from django.conf.urls import patterns, include, url
from django.contrib import admin
import views

urlpatterns = patterns('',
    url(r'^viewall_contest/(?P<group_id>\d+)/$', views.get_running_contest, name='viewall_contest'),
    url(r'^viewall_archive/(?P<group_id>\d+)/$', views.get_ended_contest, name='viewall_archive'),
    url(r'^viewall_announce/(?P<group_id>\d+)/$', views.get_all_announce, name='viewall_announce'),
    url(r'^list/$', views.list, name='list'),
    url(r'^my_list/$', views.my_list, name='my_list'),
    url(r'^detail/(?P<group_id>\d+)/$', views.detail, name='detail'),
    #Group Add/Delete/Edit Part
    url(r'^new/$', views.new, name='new'),
    url(r'^delete/(?P<group_id>\d+)/$', views.delete, name='delete'),
    url(r'^edit/(?P<group_id>\d+)/$', views.edit, name='edit'),
    #Announce Part
    url(r'^add_announce/(?P<group_id>\d+)/$', views.add_announce, name='add_announce'),
    url(r'^delete_announce/(?P<announce_id>\d+)/(?P<group_id>\d+)/(?P<redirect_page>\w+)/$', views.delete_announce, name='delete_announce'),
    url(r'^edit_announce/(?P<announce_id>\d+)/(?P<group_id>\d+)/(?P<redirect_page>\w+)/$', views.edit_announce, name='edit_announce'),
    #Member Part
    #url(r'^delete_member/(?P<group_id>\d+)/(?P<student_name>\w+)/$', views.delete_member, name='delete_member'),
)
