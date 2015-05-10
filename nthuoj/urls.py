from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
import autocomplete_light

# OP autodiscover
autocomplete_light.autodiscover()

urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    url(r'^autocomplete/', include('autocomplete_light.urls')),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^get_time/', 'index.views.get_time'),
    url(r'^', include('index.urls', namespace='index')),
    url(r'^problem/', include('problem.urls', namespace='problem')),
    url(r'^contest/', include('contest.urls', namespace='contest')),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^team/', include('team.urls', namespace='team')),
    #url(r'^group/', include('group.urls', namespace='group')),
    url(r'^status/', include('status.urls', namespace='status')),
)
handler400 = 'index.views.custom_400'
handler403 = 'index.views.custom_403'
handler404 = 'index.views.custom_404'
handler500 = 'index.views.custom_500'
