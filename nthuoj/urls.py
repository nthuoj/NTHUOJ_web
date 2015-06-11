from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from ckeditor.views import upload, browse
from utils.user_info import validate_user
import autocomplete_light

# OP autodiscover
autocomplete_light.autodiscover()


def judge_auth_required(view):
    """A decorator to ensure user has judge auth."""
    def f(request, *args, **kwargs):
        user = validate_user(request.user)
        if user.has_judge_auth():
            return view(request, *args, **kwargs)
        return HttpResponseRedirect(settings.LOGIN_URL)
    return f

urlpatterns = patterns(
    '',
    url(r'^ckeditor/upload/', csrf_exempt(judge_auth_required(upload)),
        name='ckeditor_upload'),
    url(r'^ckeditor/browse/', csrf_exempt(judge_auth_required(browse)),
        name='ckeditor_browse'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    url(r'^autocomplete/', include('autocomplete_light.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^get_time/', 'index.views.get_time'),
    url(r'^', include('index.urls', namespace='index')),
    url(r'^problem/', include('problem.urls', namespace='problem')),
    url(r'^contest/', include('contest.urls', namespace='contest')),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^team/', include('team.urls', namespace='team')),
    url(r'^group/', include('group.urls', namespace='group')),
    url(r'^status/', include('status.urls', namespace='status')),

)
handler400 = 'index.views.custom_400'
handler403 = 'index.views.custom_403'
handler404 = 'index.views.custom_404'
handler500 = 'index.views.custom_500'
