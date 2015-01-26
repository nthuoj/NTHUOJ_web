from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^index/', include('index.urls')),
    url(r'^contest/', include('contest.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^team/', include('team.urls')),
)
