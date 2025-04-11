from cms.models import PageContent
from django.contrib.sites.models import Site
from rest_framework.reverse import reverse

from tests.base import BaseCMSRestTestCase
from tests.utils import assert_field_types


class PageListAPITestCase(BaseCMSRestTestCase):
    def test_get_paginated_list(self):
        """
        Test the paginated page list endpoint (/api/{language}/pages/).

        Verifies:
        - Endpoint returns correct HTTP status code
        - Response contains paginated structure
        - All pages contain required fields
        - All fields have correct data types
        - Pagination metadata is present
        - Invalid language code returns 404
        """

        # Get current site
        site = Site.objects.get_current()
        expected_total = PageContent.objects.filter(language="en", page__node__site=site).count()

        type_checks = {
            "title": str,
            "page_title": str,
            "menu_title": str,
            "meta_description": (str, type(None)),
            "redirect": (str, type(None)),
            "in_navigation": bool,
            "soft_root": bool,
            "template": str,
            "xframe_options": (int, str),
            "limit_visibility_in_menu": (str, type(None)),
            "language": str,
            "path": str,
            "absolute_url": str,
            "is_home": bool,
            "languages": list,
            "is_preview": bool,
            "creation_date": str,
            "changed_date": str,
        }

        # GET
        response = self.client.get(reverse("page-list", kwargs={"language": "en"}))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        results = data["results"]

        # Validate REST Pagination Attributes
        self.assertIn("count", data)
        self.assertIn("next", data)
        self.assertIn("previous", data)
        self.assertIn("results", data)
        self.assertIsInstance(results, list)
        self.assertEqual(data["count"], expected_total)

        # Data & Type Validation
        for page in results:
            for field, expected_type in type_checks.items():
                assert_field_types(
                    self,
                    page,
                    field,
                    expected_type,
                )

        # Check Invalid Language
        response = self.client.get(reverse("page-list", kwargs={"language": "xx"}))
        self.assertEqual(response.status_code, 404)

        # Check Non-Public language
        response = self.client.get(reverse("page-list", kwargs={"language": "fr"}))
        self.assertEqual(response.status_code, 404)

        # GET PREVIEW
        response = self.client.get(reverse("preview-page-list", kwargs={"language": "en"}))
        self.assertEqual(response.status_code, 403)

        response = self.client.get(reverse("preview-page-list", kwargs={"language": "xx"}))
        self.assertEqual(response.status_code, 403)

    # GET PREVIEW - Protected
    def test_get_protected(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("preview-page-list", kwargs={"language": "en"}))
        self.assertEqual(response.status_code, 200)
