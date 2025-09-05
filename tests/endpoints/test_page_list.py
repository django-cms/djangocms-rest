from django.contrib.sites.models import Site
from djangocms_rest.utils import get_site_filtered_queryset
from rest_framework.reverse import reverse

from tests.base import BaseCMSRestTestCase
from tests.types import PAGE_META_FIELD_TYPES
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
        expected_total = get_site_filtered_queryset(site).count()

        type_checks = PAGE_META_FIELD_TYPES

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
        response = self.client.get(
            reverse("page-list", kwargs={"language": "en"}) + "?preview"
        )
        self.assertEqual(response.status_code, 403)

        response = self.client.get(
            reverse("page-list", kwargs={"language": "xx"}) + "?preview"
        )
        self.assertEqual(response.status_code, 403)

    # GET PREVIEW - Protected
    def test_get_protected(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("page-list", kwargs={"language": "en"}) + "?preview"
        )
        self.assertEqual(response.status_code, 200)
