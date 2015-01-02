from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'index.views.home'),
    url(r'^broken/', 'index.views.broken'),
    url(r'^get_time/', 'index.views.get_time'),
    url(r'^status/', 'index.views.status'),
    url(r'^submit/', 'index.views.submit'),
    url(r'^group_list/', 'index.views.group_list'),
    url(r'^team_list/', 'index.views.team_list'),
)
