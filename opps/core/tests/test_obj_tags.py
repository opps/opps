from django.test import TestCase

from opps.core.templatetags.obj_tags import ofKey


class OfKeyTest(TestCase):
    def test_tag(self):
        result = ofKey({"name": "andrews"}, "name")
        self.assertEqual(result, "andrews")

    def test_tag_is_none(self):
        result = ofKey(None, "name")
        self.assertEqual(result, "")
