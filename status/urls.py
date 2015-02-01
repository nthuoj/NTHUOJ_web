from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',
    url(r'^$', views.status),
    url(r'^error_message/(?P<sid>\d+)$', views.error_message, name="error_message"),
)
