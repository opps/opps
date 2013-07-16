from django.conf import settings
from django.contrib.sites.models import get_current_site
from django.test import TestCase
from django.test.client import RequestFactory

from opps.channels.context_processors import channel_context


class ChannelContextTest(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/")
        self.result = channel_context(self.request)

    def test_site(self):
        expected = get_current_site(self.request)
        self.assertEqual(expected, self.result['site'])

    def test_conf(self):
        self.assertEqual(settings.OPPS_CHANNEL_CONF,
                         self.result['opps_channel_conf_all'])
