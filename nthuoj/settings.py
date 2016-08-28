"""
Django settings for nthuoj project.
For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
# -*- encoding=UTF-8 -*-

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from utils.config_info import get_config

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."),)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'kivl1x)by8$98z6y3b^7texw&+d1arad2qlq-(sn=8g^lw_(+&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'autocomplete_light',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'utils',
    'problem',
    'index',
    'contest',
    'users',
    'team',
    'group',
    'status',
    'axes',
    'bootstrapform',
    'djangobower',
    'datetimewidget',
    'ckeditor',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'utils.render_helper.CustomHttpExceptionMiddleware',
)

ROOT_URLCONF = 'nthuoj.urls'

WSGI_APPLICATION = 'nthuoj.wsgi.application'

CONFIG_PATH = os.path.join(BASE_DIR, 'nthuoj/config/nthuoj.cfg')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': CONFIG_PATH,
        },
    }
}

# Custom User auth

AUTH_USER_MODEL = 'users.User'
# where @login_required will redirect to
LOGIN_URL = '/users/login/'


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'

# django-axes 1.3.8 configurations
# https://pypi.python.org/pypi/django-axes/

# redirect to broken page when exceed wrong-try limits
AXES_LOCKOUT_URL = '/users/block_wrong_tries'
# freeze login access for that ip for 0.1*60 = 6 minites
AXES_COOLOFF_TIME = 0.1

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = get_config('email', 'user')
EMAIL_HOST_PASSWORD = get_config('email', 'password')
EMAIL_PORT = 587

# django-ckeditor configurations
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
    },
}


# django-bower settings
BOWER_COMPONENTS_ROOT = os.path.join(PROJECT_ROOT, 'components')

BOWER_INSTALLED_APPS = (
    'Chart.js',
    'jquery#=2.2.4',
    'jquery-ui#1.9.2',
    'https://github.com/thomaspark/bootswatch.git#3.3.6+1',  # bootswatch
    'https://github.com/dimsemenov/Magnific-Popup.git',  # Magnific-Popup
    'https://github.com/codemirror/CodeMirror.git',  # CodeMirror
    # bootstrap fileinput
    'http://gregpike.net/demos/bootstrap-file-input/bootstrap.file-input.js',
    'https://github.com/lou/multi-select.git',  # multiselect
    'https://github.com/riklomas/quicksearch.git',  # quicksearch
    # jquery url plugin
    'https://github.com/websanova/js-url.git'
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'djangobower.finders.BowerFinder',
)

# maximum of public users for a single contest
MAX_PUBLIC_USER = 200
# public user username prefix
PUBLIC_USER_PREFIX = "TEAM"

PUBLIC_USER_DEFAULT_PASSWORD = "000"

if DEBUG:
    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

    INSTALLED_APPS += (
        'debug_toolbar',
    )
    SHOW_TOOLBAR_CALLBACK = True
#    INTERNAL_IPS = ('127.0.0.1')
    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ]

