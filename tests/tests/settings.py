"""
Django settings for tests project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import djcelery
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7c1ovpas%39#&bi_f-z)r-1!wgq2f6p6nd_z2n@eh^csg%rc$u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = []

SITE_ID = 1


# Application definition

INSTALLED_APPS = (
    'opps.contrib.admin',
    'opps.contrib.fileupload',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.redirects',

    'opps.core',
    'opps.core.tags',
    'opps.images',
    'opps.containers',
    'opps.boxes',
    'opps.channels',
    'opps.articles',
    'opps.sitemaps',
    'opps.flatpages',
    'opps.archives',
    'opps.views',
    'opps.fields',
    'opps.db',
    'opps.api',
    'opps.contrib.notifications',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'opps.channels.context_processors.channel_context',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
)


ROOT_URLCONF = 'tests.urls'

WSGI_APPLICATION = 'tests.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'


#TEST_RUNNER = 'django_coverage.coverage_runner.CoverageRunner'
TEST_RUNNER = 'tests.runner.Runner'

BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
djcelery.setup_loader()

OPPS_MIRROR_CHANNEL = True

OPPS_DB_HOST='127.0.0.1'
OPPS_DB_PORT=6379
OPPS_DB_NAME='opps'
OPPS_DB_ENGINE='opps.db._redis.Redis'
