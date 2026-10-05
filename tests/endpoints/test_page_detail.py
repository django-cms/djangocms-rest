from cms.api import create_page_content
from cms.models import PageUrl

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

    # GET PREVIEW - Specific page content
    def test_get_preview_content(self):
        page = PageUrl.objects.get(path="page-0", language="en").page
        en_content = page.get_admin_content("en")
        it_content = create_page_content("it", "pagina 0", page)
        url = reverse("page-detail", kwargs={"language": "en", "path": "page-0"})

        # Anonymous users cannot use the content selector
        response = self.client.get(f"{url}?preview=1&content={en_content.pk}")
        self.assertEqual(response.status_code, 403)

        self.client.force_login(self.user)

        # Content selector requires preview mode and is ignored otherwise
        response = self.client.get(f"{url}?content={it_content.pk}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "page 0")

        response = self.client.get(f"{url}?preview=1&content={en_content.pk}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["is_preview"])
        self.assertTrue(data["placeholders"])
        for placeholder in data["placeholders"]:
            self.assertIn(f"/{en_content.pk}/", placeholder["details"])

        # Content of another language, another page or an invalid id
        other_content = PageUrl.objects.get(path="page-1", language="en").page.get_admin_content("en")
        for content_id in (it_content.pk, other_content.pk, "invalid"):
            response = self.client.get(f"{url}?preview=1&content={content_id}")
            self.assertEqual(response.status_code, 404)

        it_url = reverse("page-detail", kwargs={"language": "it", "path": "pagina-0"})
        response = self.client.get(f"{it_url}?preview=1&content={it_content.pk}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "pagina 0")
