"""
Django settings for reminder project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

from decouple import config, Csv
from django.utils.translation import gettext_lazy as _
from django.contrib.messages import constants as messages

import dj_database_url
import os
import django.conf.locale
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

ADMINS = (
    (config('ADMIN'), config('ADMIN_EMAIL')),
)


# Application definition

INSTALLED_APPS = [
    'main.apps.MainConfig',
    'users.apps.UsersConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'crispy_forms',
    'widget_tweaks',
    'cookielaw',
    'vinaigrette',
    'django_cron',
    'django_inlinecss',
    'maintenancemode',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'maintenancemode.middleware.MaintenanceModeMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.AllowAllUsersModelBackend'
]

ROOT_URLCONF = 'reminder.urls'

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

TEMPLATE_CONTEXT_PROCESSORS = ['django.core.context_processors.i18n']

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

WSGI_APPLICATION = 'reminder.wsgi.application'

CRON_CLASSES = [
    "cron.cron.SendReminders",
]

SITE_ID = 2
MAINTENANCE_503_TEMPLATE = 'main/503.html'

DATABASES = {
    'default': dj_database_url.config(default=config('DATABASE_URL'))
    }

# Password validation

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

LANGUAGE_CODE = 'en'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

LANGUAGES = [
    ('cs', 'Česky'),
    ('en', _('English')),
]

EXTRA_LANG_INFO = {
    'cs': {
        'bidi': False, # right-to-left
        'code': 'cs',
        'name': 'Czech',
        'name_local': u'Česky', #unicode codepoints here
    },
}

LANG_INFO = dict({**django.conf.locale.LANG_INFO, **EXTRA_LANG_INFO})
django.conf.locale.LANG_INFO = LANG_INFO

FORMAT_MODULE_PATH = [
    'reminder.formats',
]

# Email

EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
CONTACT_FORM_EMAIL = config('CONTACT_FORM_EMAIL')
EMAIL_SUBJECT_PREFIX = _('[NeverExpire] Expiration reminder ')


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'staticfiles')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

SESSION_COOKIE_AGE = 3600

# Sentry settings

sentry_sdk.init(
    dsn="https://a16e56cf14e5442e8cd6400ffc2011e7@o485345.ingest.sentry.io/5540568",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
         'require_debug_false': {
             '()': 'django.utils.log.RequireDebugFalse'
         }
     },
    'formatters': {
            'verbose': {
                'format': '[contactor] %(levelname)s %(asctime)s %(message)s'
            },
        },
    'handlers': {
        # Send all messages to console
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        # Log to a text file that can be rotated by logrotate
        'logfile': {
            'class': 'logging.handlers.WatchedFileHandler',
            'level': 'WARNING',
            'filename': '/home/reminder/logs/log.log'
        },
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'level': 'WARNING',
            'filters': ['require_debug_false'],
            # 'include_html': True,
        },
        # critical errors are logged to sentry
        'sentry': {
            'level': 'WARNING',
            'filters': ['require_debug_false'],
            'class': 'raven.contrib.django.handlers.SentryHandler',
        },
    },
    'loggers': {
        # The "catch all" logger
        '': {
            'handlers': ['console', 'logfile', 'mail_admins', 'sentry'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
