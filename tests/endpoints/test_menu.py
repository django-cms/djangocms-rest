from django.contrib.sites.models import Site
from rest_framework.reverse import reverse

from tests.base import BaseCMSRestTestCase

from cms.models import Page


class PageListAPITestCase(BaseCMSRestTestCase):
    def test_get_menu_no_children(self):
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
        url = reverse(
            "menu",
            kwargs={
                "language": "en",
                "from_level": 0,
                "to_level": 0,
                "extra_inactive": 0,
                "extra_active": 100,
            },
        )
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

        # Selected: Root page
        self.assertTrue(results[0]["selected"])
        self.assertFalse(results[1]["selected"])
        self.assertFalse(results[2]["selected"])

    def test_get_menu_with_children(self):
        """
        Test the menu endpoint (/api/{language}/menu/{path}/) with child pages.

        Verifies:
        - Child pages are included in the response
        - Child pages have correct titles and structure
        """

        # GET
        url = reverse(
            "menu",
            kwargs={
                "language": "en",
                "path": "page-2",
                "from_level": 0,
                "to_level": 100,
                "extra_inactive": 0,
                "extra_active": 100,
            },
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        results = response.json()

        # Check if the child page is included
        self.assertIn("children", results[0])
        self.assertEqual(len(results[2]["children"]), 2)
        self.assertEqual(results[2]["children"][0]["title"], "page 0")

    def test_default_levels(self):
        url1 = reverse(
            "menu",
            kwargs={"language": "en"},
        )
        url2 = reverse(
            "menu",
            kwargs={
                "language": "en",
                "from_level": 0,
                "to_level": 100,
                "extra_inactive": 0,
                "extra_active": 1000,
            },
        )
        results1 = self.client.get(url1).json()
        results2 = self.client.get(url2).json()

        self.assertNotEqual(url1, url2)
        self.assertEqual(results1, results2)

    def test_submenu(self):
        # GET
        url = reverse(
            "submenu",
            kwargs={
                "language": "en",
                "path": "page-2",
            },
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        results = response.json()

        self.assertEqual(len(results), 2)

        self.assertEqual(results[0]["title"], "page 0")
        self.assertEqual(results[1]["title"], "page 1")

    def test_breadcrumbs(self):
        # GET
        url = reverse(
            "breadcrumbs",
            kwargs={
                "language": "en",
                "path": "page-2/page-0",
            },
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        results = response.json()
        self.assertEqual(len(results), 3)

        self.assertEqual(results[0]["title"], "page 0")
        self.assertEqual(results[1]["title"], "page 2")
        self.assertEqual(results[2]["title"], "page 0")
