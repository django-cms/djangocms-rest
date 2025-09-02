from django.test import TestCase

from djangocms_rest.utils import get_absolute_frontend_url


class UtilityTestCase(TestCase):
    def test_get_absolute_frontend_url_adds_site(self):
        url = get_absolute_frontend_url("/some/path/")
        self.assertEqual(url, "http://testserver/some/path/")

    def test_get_absolute_frontend_url_keeps_none(self):
        url = get_absolute_frontend_url(None)
        self.asserIsNone(url)
