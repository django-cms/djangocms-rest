from django.urls import reverse

from tests.base import BaseCMSRestTestCase

from django.contrib.sites.models import Site
from cms.api import create_page, publish_page


class SiteContextMiddlewareTestCase(BaseCMSRestTestCase):
    @classmethod
    def setUpClass(cls):
        """
        Sets up a test environment with multiple sites.
        """
        super().setUpClass()

        cls.site1 = Site.objects.get(id=1)
        cls.site1.domain = "site1.example.com"
        cls.site1.name = "Site 1"
        cls.site1.save()

        cls.site2 = Site.objects.create(domain="site2.example.com", name="Site 2")

    @classmethod
    def tearDownClass(cls):
        """
        Clean up the test environment and reset site 1.
        """
        try:
            cls.site2.delete()
        except Site.DoesNotExist:
            pass

        try:
            cls.site1.domain = "example.com"
            cls.site1.name = "example.com"
            cls.site1.save()
        except Site.DoesNotExist:
            pass

        super().tearDownClass()

    def test_site_middleware_with_header(self):
        """
        Test the SiteContextMiddleware correctly handles X-Site-ID header
        and returns different pages based on the site id.

        Verifies:
        - Middleware uses the site ID from X-Site-ID header
        - the Same path returns different content based on site ID
        - Invalid site ID returns appropriate error
        - Missing site ID uses default site
        """
        # Create specific test pages with unique titles for each site
        site1_test_page = create_page(
            title="Site 1 Test Page",
            template="page.html",
            language="en",
            slug="test-page",
            site=self.site1,
        )
        publish_page(site1_test_page, "en", True)

        site2_test_page = create_page(
            title="Site 2 Test Page",
            template="page.html",
            language="en",
            slug="test-page",
            site=self.site2,
        )
        publish_page(site2_test_page, "en", True)

        # Test with site 1 header
        response = self.client.get(
            reverse("page-detail", kwargs={"language": "en", "path": "test-page"}),
            HTTP_X_SITE_ID="1",
        )
        self.assertEqual(response.status_code, 200)
        site1_data = response.json()

        # Test with site 2 header
        response = self.client.get(
            reverse("page-detail", kwargs={"language": "en", "path": "test-page"}),
            HTTP_X_SITE_ID="2",
        )
        self.assertEqual(response.status_code, 200)
        site2_data = response.json()

        # Compare titles - these should be different
        self.assertEqual(site1_data.get("title"), "Site 1 Test Page")
        self.assertEqual(site2_data.get("title"), "Site 2 Test Page")
        self.assertNotEqual(site1_data.get("title"), site2_data.get("title"))

        # Test invalid site ID
        response = self.client.get(
            reverse("page-detail", kwargs={"language": "en", "path": "test-page"}),
            HTTP_X_SITE_ID="999",
        )
        self.assertEqual(response.status_code, 404)

        # Test invalid site ID format
        response = self.client.get(
            reverse("page-detail", kwargs={"language": "en", "path": "test-page"}),
            HTTP_X_SITE_ID="invalid",
        )
        self.assertEqual(response.status_code, 400)

        # Test without a site ID header (should default to site 1)
        response = self.client.get(
            reverse("page-detail", kwargs={"language": "en", "path": "test-page"})
        )
        self.assertEqual(response.status_code, 200)
        default_data = response.json()

        # Verify default site returns the same content as site 1
        self.assertEqual(default_data.get("title"), site1_data.get("title"))
        self.assertEqual(default_data.get("title"), "Site 1 Test Page")
