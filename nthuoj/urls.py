from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^broken/', 'index.views.broken'),
    url(r'^get_time/', 'index.views.get_time'),
    url(r'^index/', include('index.urls', namespace='index')),
    url(r'^problem/', include('problem.urls', namespace='problem')),
    url(r'^contest/', include('contest.urls', namespace='contest')),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^team/', include('team.urls', namespace='team')),
    url(r'^group/', include('group.urls', namespace='group')),
    url(r'^status/', include('status.urls', namespace='status')),
)
handler404 = 'index.views.custom_404'
handler500 = 'index.views.custom_500'
