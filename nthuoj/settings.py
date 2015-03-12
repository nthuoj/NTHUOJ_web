"""
Django settings for nthuoj project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from emailInfo import EMAIL_HOST_USER
from emailInfo import EMAIL_HOST_PASSWORD

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


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
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.FailedLoginMiddleware',
)

ROOT_URLCONF = 'nthuoj.urls'

WSGI_APPLICATION = 'nthuoj.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
INI_PATH = os.path.join(BASE_DIR, 'nthuoj.ini')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': INI_PATH,
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

STATIC_URL = '/static/'

# django-axes 1.3.8 configurations
# https://pypi.python.org/pypi/django-axes/

# redirect to broken page when exceed wrong-try limits
AXES_LOCKOUT_TEMPLATE = 'index/404.html'
# freeze login access for that ip for 0.1*60 = 6 minites
AXES_COOLOFF_TIME = 0.1

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
