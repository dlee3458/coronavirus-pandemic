"""
Django settings for covid19 project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from celery.schedules import crontab
import django_heroku

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# dotenv_file = os.path.join(BASE_DIR, ".env")
# if os.path.isfile(dotenv_file):
#     dotenv.load_dotenv(dotenv_file)
# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = '_0t)l$=1v!i!nr_z2iu$d0(k@@%(pvnk9q$jmkuua)cnt%zcvc'
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = (os.environ.get('DEBUG_VALUE') == 'True')
# DEBUG = 'True'

ALLOWED_HOSTS = ['coronaviruspandemic.herokuapp.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'news.apps.NewsConfig',
    'stats.apps.StatsConfig',
    'django.contrib.humanize',
    'django_countries',
    'django_crontab',
    'django_celery_beat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'covid19.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'covid19.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'covid19',
        'USER': 'dlee',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

CELERY_BROKER_URL = os.environ.get('REDISCLOUD_URL', 'redis://localhost:6379')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
# If time zones are active (USE_TZ = True) define your local
CELERY_TIMEZONE = 'US/Pacific'
# We're going to have our tasks rolling soon, so that will be handy
CELERY_BEAT_SCHEDULE = {
    'get-stats': {
        'task': 'stats',
        'schedule': crontab(minute=26, hour=5),
    },
    'get-countries': {
        'task': 'countries',
        'schedule': crontab(minute=26, hour=5),
    },
    'get-trending': {
        'task': 'trending',
        'schedule': crontab(minute=26, hour=5),
    },
    'get-new': {
        'task': 'new',
        'schedule': crontab(minute=26, hour=5),
    },
    'get-rate': {
        'task': 'rate',
        'schedule': crontab(minute=26, hour=5)
    },
    'state-stats': {
        'task': 'states',
        'schedule': crontab(minute=26, hour=5)
    }
}

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

django_heroku.settings(locals())
