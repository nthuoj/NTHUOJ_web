from django.conf.urls import patterns, include, url
from problem import views

urlpatterns = patterns('',
	url(r'^$', views.problem, name='problem'),
	url(r'^(?P<problem_id>)\d+/$', views.detail, name='detail'), 
	url(r'^(?P<problem_id>)\d+/edit/$', views.edit, name='edit'),
	url(r'^new/$', views.new, name='new'),
	url(r'^preview/$', views.preview, name='new'),
)
