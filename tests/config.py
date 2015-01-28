import djcelery

from django.conf import settings


def configure():
    if settings.configured:
        return

    test_settings = {
        'DATABASES': {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            },
        },
        'INSTALLED_APPS': [
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
            'opps.core.permissions',
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
            'opps.api',
            'opps.contrib.notifications',
        ],
        'TEMPLATE_CONTEXT_PROCESSORS': (
            'opps.channels.context_processors.channel_context',
        ),
        'MIDDLEWARE_CLASSES': (
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
            'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
        ),
        'HAYSTACK_CONNECTIONS': {
            'default': {
                'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
            }
        },
        'OPPS_MULTISITE_FALLBACK': False,
        'ROOT_URLCONF': 'tests._site.urls',
        'STATIC_URL': '/static/',
        'ADMINS': ('admin@example.com',),
        'DEBUG': False,
        'SITE_ID': 1,
        'BROKER_URL': 'redis://localhost:6379/0',
        'CELERY_RESULT_BACKEND': 'redis://localhost:6379/0',
        'OPPS_MIRROR_CHANNEL': True,
        'OPPS_DB_HOST': '127.0.0.1',
        'OPPS_DB_PORT': 6379,
        'OPPS_DB_NAME': 'opps',
        'OPPS_DB_ENGINE': 'opps.db._redis.Redis',
        'OPPS_MULTISITE_ADMIN': True,
    }

    djcelery.setup_loader()
    settings.configure(**test_settings)
