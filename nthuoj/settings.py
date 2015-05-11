#-*- encoding=UTF-8 -*-
"""
Django settings for nthuoj project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

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
DEBUG = True

TEMPLATE_DEBUG = True

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
    'vjudge',
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
    'axes.middleware.FailedLoginMiddleware',
)

ROOT_URLCONF = 'nthuoj.urls'

WSGI_APPLICATION = 'nthuoj.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
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
    'jquery',
    'jquery-ui#1.9.2',
    'https://github.com/thomaspark/bootswatch.git', # bootswatch
    'https://github.com/dimsemenov/Magnific-Popup.git', # Magnific-Popup
    'https://github.com/codemirror/CodeMirror.git', # CodeMirror
    'http://gregpike.net/demos/bootstrap-file-input/bootstrap.file-input.js', # bootstrap fileinput
    'https://github.com/lou/multi-select.git', # multiselect
    'https://github.com/riklomas/quicksearch.git', # quicksearch
    'https://gantry.googlecode.com/svn/trunk/root/js/jquery.url.min.js', # jquery url plugin
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'djangobower.finders.BowerFinder',
)

#maximum of public users for a single contest
MAX_PUBLIC_USER = 200
#public user username prefix
PUBLIC_USER_PREFIX = "TEAM"

PUBLIC_USER_DEFAULT_PASSWORD = "000"

