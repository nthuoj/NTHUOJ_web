from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^problem/', include('problem.urls')),
    url(r'^get_time/', 'index.views.get_time'),
    url(r'^index/', include('index.urls')),
    url(r'^contest/', include('contest.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^team/', include('team.urls')),
    url(r'^group/', include('group.urls')),
    url(r'^status/', include('status.urls')),
)
