from rest_framework.reverse import reverse

from tests.base import BaseCMSRestTestCase
from tests.types import PAGE_CONTENT_FIELD_TYPES
from tests.utils import assert_field_types


class PageDetailAPITestCase(BaseCMSRestTestCase):
    def test_get(self):
        """
        Test the page detail endpoint ('/api/{language}/pages/{path}/').

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
        response = self.client.get(reverse("page-detail", kwargs={"language": "en", "path": "page-0"}))
        self.assertEqual(response.status_code, 200)
        page = response.json()

        # Data & Type Validation
        for field, expected_type in type_checks.items():
            assert_field_types(
                self,
                page,
                field,
                expected_type,
            )

        # Check Invalid Path
        response = self.client.get(reverse("page-detail", kwargs={"language": "en", "path": "nonexistent-page"}))
        self.assertEqual(response.status_code, 404)

        # Check Invalid Language
        response = self.client.get(reverse("page-detail", kwargs={"language": "xx", "path": "page-0"}))
        self.assertEqual(response.status_code, 404)

    # GET PREVIEW - Protected
    def test_get_protected(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("page-detail", kwargs={"language": "en", "path": "page-0"}))
        self.assertEqual(response.status_code, 200)
