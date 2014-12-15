from django.conf.urls import patterns, url
from contest import views

urlpatterns = patterns('',
    url(r'^$',views.index,name='index'),
    url(r'^admin/$',views.admin,name='admin'),
    url(r'^contest/(?P<contest_id>\d+)/$',views.contest,name='contest'),
    url(r'^navbar/$',views.navbar,name='navbar'),
    )
