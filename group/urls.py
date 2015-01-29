from django.conf.urls import patterns, include, url
from django.contrib import admin
import views

urlpatterns = patterns('',
	url(r'^get_time/', views.get_time),
    url(r'^list/$', views.list, name='list'),
    url(r'^detail/(?P<group_id>[0-9]+)/$', views.detail, name='detail'),
)
