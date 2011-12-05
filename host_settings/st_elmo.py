from host_settings.common import *
from os.path import *

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    join(PROJECT_DIR, 'templates'),
    join(join(PROJECT_DIR, 'templates'), 'st-elmo'),
)

SITE_NAME = 'St. Elmo'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'django.contrib.comments',
    'grappelli',
    'filebrowser',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'neighborlink.apps.account',
    'neighborlink.apps.content',
    'neighborlink.apps.entity',
    'neighborlink.apps.stelmo',
)

