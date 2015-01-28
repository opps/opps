from django.test import TestCase
from django.test.client import RequestFactory

from opps.contrib.mobile import template
from opps.contrib.mobile.middleware import (
    MobileDetectionMiddleware, MobileRedirectMiddleware
)


class TestMobileTemplatesDir(TestCase):

    def setUp(self):
        self.detection_middleware = MobileDetectionMiddleware()
        self.factory = RequestFactory()
        self.template_loader = template.Loader()

    def test_useragent_based_templatedirs(self):
        # Override the TEMPLATE_LOADERS and MIDDLEWARE_CLASSES settings
        # to use the middlewares in ``opps.contrib.mobile.middleware``
        # and the ``opps.contrib.mobile.template.Loader``
        MIDDLEWARE_CLASSES = (
            'django.middleware.common.CommonMiddleware',
            'opps.contrib.mobile.middleware.MobileDetectionMiddleware',
            'opps.contrib.mobile.middleware.MobileRedirectMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
        )
        TEMPLATE_LOADERS = (
            'opps.contrib.mobile.template.Loader',
            'django.template.loaders.app_directories.Loader',
        )
        TEMPLATE_DIRS_MOBILE = ('mobile-templates',)
        TEMPLATE_DIRS_WEB = ('web-templates',)

        custom_settings = self.settings(
            MIDDLEWARE_CLASSES=MIDDLEWARE_CLASSES,
            TEMPLATE_LOADERS=TEMPLATE_LOADERS,
            TEMPLATE_DIRS_MOBILE=TEMPLATE_DIRS_MOBILE,
            TEMPLATE_DIRS_WEB=TEMPLATE_DIRS_WEB,
            OPPS_CHECK_MOBILE=True,
            OPPS_DOMAIN_MOBILE='m.testserver'
        )
        with custom_settings:
            mobile_request = self.factory.get('/', HTTP_USER_AGENT='mobi')
            desktop_request = self.factory.get('/',
                                               HTTP_USER_AGENT='Mozilla/5.0')

            get_template_sources = self.template_loader.get_template_sources

            self.detection_middleware.process_request(desktop_request)
            self.assertEqual(
                get_template_sources('index.html').next(),
                get_template_sources('index.html', TEMPLATE_DIRS_WEB).next()
            )

            self.detection_middleware.process_request(mobile_request)
            self.assertEqual(
                get_template_sources('index.html').next(),
                get_template_sources('index.html', TEMPLATE_DIRS_MOBILE).next()
            )
