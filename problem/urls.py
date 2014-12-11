from django.conf.urls import patterns, include, url
from problem import views

urlpatterns = patterns('',
	url(r'^$', views.problem, name='problem'),  # /problem  : problem panel
	url(r'^(?P<problem_id>)\d+/$', views.detail, name='detail'),   # /problem/10 : detail of problem 10
	url(r'^(?P<problem_id>)\d+/edit/$', views.edit, name='edit'),  # /problem/10/edit : edit problem 10
	url(r'^new/$', views.new, name='new'), # /problem/new : create new problem
	url(r'^preview/$', views.preview, name='new'),  # /problem/preview  :  preview problem when editting
)
