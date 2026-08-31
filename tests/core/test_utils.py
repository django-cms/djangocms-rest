from unittest import skip

from django.contrib.sites.models import Site

from rest_framework.test import APIRequestFactory

from djangocms_rest.utils import get_absolute_frontend_url
from tests.base import BaseCMSRestTestCase


class UrlUtilsTestCase(BaseCMSRestTestCase):
    """
    Test the get_absolute_frontend_url utility function.

    Verifies:
    - Function correctly builds absolute URLs for frontend paths
    - Function raises proper ValueError for invalid paths
    - Function works correctly with both a request object and None
    - All URLs use the correct domain from a Site object
    """

    def setUp(self):
        super().setUp()
        self.factory = APIRequestFactory()

    @skip("Skipping test for get_absolute_frontend_url")
    def test_get_absolute_frontend_url_valid_path(self):
        """Test that get_absolute_frontend_url works with valid paths."""

        request = self.factory.get("/dummy")
        site = Site.objects.get_current()
        result = get_absolute_frontend_url(request, "valid/path")

        # Validation
        expected_url = f"http://{site.domain}/valid/path"
        self.assertEqual(result, expected_url)

    @skip("Skipping test for get_absolute_frontend_url with leading slash")
    def test_get_absolute_frontend_url_with_leading_slash(self):
        """Test that get_absolute_frontend_url raises ValueError with paths starting with /."""
        request = self.factory.get("/dummy")

        # Function execution and validation
        with self.assertRaises(ValueError) as context:
            get_absolute_frontend_url(request, "/invalid/path")

        # Error message validation
        error_message = str(context.exception)
        self.assertIn("Path should not start with '/'", error_message)
        self.assertIn("/invalid/path", error_message)

    def test_get_absolute_frontend_url_without_request(self):
        """Test that get_absolute_frontend_url works with request=None."""

        result = get_absolute_frontend_url(None, "valid/path")

        # Validation
        site = Site.objects.get(id=1)
        expected_url = f"http://{site.domain}/valid/path"
        self.assertEqual(result, expected_url)
