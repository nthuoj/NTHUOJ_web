from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
<<<<<<< HEAD
    url(r'^admin/', include(admin.site.urls)),
<<<<<<< HEAD
    url(r'^$', 'index.views.home'),
    url(r'^broken/', 'index.views.broken'),
    url(r'^get_time/', 'index.views.get_time'),
    url(r'^status/', 'index.views.status'),
    url(r'^submit/', 'index.views.submit'),
    url(r'^group_list/', 'index.views.group_list'),
    url(r'^team_list/', 'index.views.team_list'),
=======
=======
	url(r'^admin/', include(admin.site.urls)),
    url(r'^contest/', include('contest.urls')),
>>>>>>> e415e994c11a12bae43f6c9c8b0342a95b3a600d
    url(r'^submit/$', 'users.views.submit'),
    url(r'^profile/$', 'users.views.profile'),
>>>>>>> 654949c4f754f18ef1967c591d509451e6a99545
)
