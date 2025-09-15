from rest_framework.reverse import reverse

from tests.base import BaseCMSRestTestCase
from tests.types import PAGE_CONTENT_FIELD_TYPES
from tests.utils import assert_field_types


class PageRootAPITestCase(BaseCMSRestTestCase):
    def test_get(self):
        """
        Test the page root endpoint ('/api/{language}/pages/').

        Verifies:
        - Endpoint returns correct HTTP status code
        - Response contains required fields
        - All fields have correct data types and values from the page model
        - Fields are properly formatted in JSON response
        - Invalid language code returns 404
        - Proper parsing of response JSON data
        - Response structure matches API contract
        """

        type_checks = PAGE_CONTENT_FIELD_TYPES

        # GET
        response = self.client.get(reverse("page-root", kwargs={"language": "en"}))
        self.assertEqual(response.status_code, 200)
        page = response.json()
        self.assertFalse(response.json().get("is_preview"))

        # GET with ?preview=false
        response = self.client.get(
            reverse("page-root", kwargs={"language": "en"}) + "?preview=false"
        )
        self.assertEqual(response.status_code, 200)
        page = response.json()
        self.assertFalse(response.json().get("is_preview"))

        # Data & Type Validation
        for field, expected_type in type_checks.items():
            self.assertIn(field, page, f"Field {field} is missing")

            if isinstance(expected_type, tuple):
                assert_field_types(
                    self,
                    page,
                    field,
                    expected_type,
                )

        # Check Invalid Language
        response = self.client.get(reverse("page-root", kwargs={"language": "xx"}))
        self.assertEqual(response.status_code, 404)

        # GET PREVIEW
        response = self.client.get(
            reverse("page-root", kwargs={"language": "en"}) + "?preview"
        )
        self.assertEqual(response.status_code, 403)

        response = self.client.get(
            reverse("page-root", kwargs={"language": "xx"}) + "?preview"
        )
        self.assertEqual(response.status_code, 403)

    # GET PREVIEW - Protected
    def test_get_protected(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("page-root", kwargs={"language": "en"}) + "?preview"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json().get("is_preview"))
