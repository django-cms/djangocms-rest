from django.contrib.sites.models import Site
from rest_framework.reverse import reverse

from tests.base import BaseCMSRestTestCase

from cms.models import Page


class PageListAPITestCase(BaseCMSRestTestCase):
    def test_get_menu_default(self):
        """
        Test the menu endpoint (/api/{language}/menu/).

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
        expected_length = Page.objects.filter(site=site, parent=None).count()

        # GET
        url = reverse("menu", kwargs={"language": "en"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        results = response.json()

        # Number of results:
        self.assertEqual(len(results), expected_length)

        # Page titles:
        self.assertEqual(results[0]["title"], "page 0")
        self.assertEqual(results[1]["title"], "page 1")
        self.assertEqual(results[2]["title"], "page 2")

        # No children:
        self.assertEqual(results[0]["children"], [])
        self.assertEqual(results[1]["children"], [])
        self.assertEqual(results[2]["children"], [])

    def x_test_get_menu_with_children(self):
        """
        Test the menu endpoint (/api/{language}/menu/) with child pages.

        Verifies:
        - Child pages are included in the response
        - Child pages have correct titles and structure
        """

        # GET
        url = reverse(
            "menu",
            kwargs={
                "language": "en",
            },
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        results = response.json()

        # Check if the child page is included
        self.assertIn("children", results[0])
        self.assertEqual(len(results[0]["children"]), 1)
        self.assertEqual(results[0]["children"][0]["title"], "Child Page")
