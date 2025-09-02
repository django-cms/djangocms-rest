from django.test import TestCase
from django.test import RequestFactory

from djangocms_rest.utils import get_absolute_frontend_url


class UtilityTestCase(TestCase):
    def test_get_absolute_frontend_url_adds_site(self):
        request = RequestFactory().get("http://testserver/")
        url = get_absolute_frontend_url(request, "/some/path/")
        self.assertEqual(url, "http://testserver/some/path/")

    def test_get_absolute_frontend_url_keeps_none(self):
        request = RequestFactory().get("http://testserver/")
        url = get_absolute_frontend_url(request, None)
        self.assertIsNone(url)
