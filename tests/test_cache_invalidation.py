"""
Tests for cache invalidation risks and scenarios in djangocms-rest.

This test suite identifies and documents potential cache-related issues:
- Missing invalidation when CMS content changes
- Preview mode cache pollution
- Multi-language cache consistency
- Missing manual cache clear mechanisms
"""

from cms.api import add_plugin, create_page
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.test import RequestFactory, TestCase
from unittest.mock import MagicMock

from tests.base import BaseCMSRestTestCase


class CacheVersioningTests(TestCase):
    """Test cache versioning mechanism for placeholder cache invalidation."""

    def setUp(self):
        cache.clear()

    def tearDown(self):
        cache.clear()

    def test_cache_versioning_exists(self):
        """
        Verify that cache versioning system is in place.
        This allows tracking when placeholder content changes.
        """
        from djangocms_rest.serializers.utils.cache import (
            _get_placeholder_cache_version,
        )

        # Mock placeholder object with required attributes
        placeholder = MagicMock()
        placeholder.pk = 1
        placeholder.get_vary_cache_on = MagicMock(return_value=[])

        version1, vary_list1 = _get_placeholder_cache_version(placeholder, "en", 1)
        self.assertIsNotNone(version1)
        self.assertIsInstance(version1, int)


class CachePreviewModeTests(BaseCMSRestTestCase):
    """
    Test cache isolation between preview and public modes.

    Verifies that preview mode correctly bypasses cache to prevent
    draft content from leaking to public API responses.
    """

    def setUp(self):
        super().setUp()
        cache.clear()
        self.site = Site.objects.get_current()
        self.language = "en"
        self.factory = RequestFactory()

    def tearDown(self):
        cache.clear()

    def test_preview_mode_bypasses_cache(self):
        """
        Verify that preview mode does not use cache.
        When _preview_mode=True, cache should be bypassed.
        """
        from django.urls import reverse

        # Login as staff user for preview access
        self.client.force_login(self.get_staff_user_with_no_permissions())

        # Create a page with placeholder
        page = create_page(
            title="Test Page",
            template="page.html",
            language=self.language,
        )
        placeholder = page.get_placeholders(self.language).first()

        # Add a plugin
        plugin = add_plugin(
            placeholder,
            "TextPlugin",
            self.language,
            body="<p>Test content</p>",
        )

        # Build API URL for placeholder detail
        url = reverse(
            "placeholder-detail",
            args=[
                self.language,
                placeholder.content_type_id,
                placeholder.object_id,
                placeholder.slot,
            ],
        )

        # First call with preview mode - should NOT use cache
        response1 = self.client.get(url + "?preview=1")
        self.assertEqual(response1.status_code, 200)
        content1 = response1.json()

        # Modify plugin
        plugin.body = "<p>Modified content</p>"
        plugin.save()

        # Second call with preview mode - should get fresh data (no cache)
        response2 = self.client.get(url + "?preview=1")
        self.assertEqual(response2.status_code, 200)
        content2 = response2.json()

        # Content should be different because cache was bypassed
        # Check the actual plugin content changed
        self.assertNotEqual(
            content1["content"][0]["body"],
            content2["content"][0]["body"],
            "Preview mode should bypass cache and show updated content",
        )

    def test_public_mode_uses_cache(self):
        """
        Verify that public mode (no preview) uses cache.
        """
        from django.urls import reverse

        # Create a page with placeholder
        page = create_page(
            title="Test Page",
            template="page.html",
            language=self.language,
        )
        placeholder = page.get_placeholders(self.language).first()

        # Add a plugin
        plugin = add_plugin(
            placeholder,
            "TextPlugin",
            self.language,
            body="<p>Test content</p>",
        )

        # Build API URL for placeholder detail
        url = reverse(
            "placeholder-detail",
            args=[
                self.language,
                placeholder.content_type_id,
                placeholder.object_id,
                placeholder.slot,
            ],
        )

        # First call - should cache the response
        response1 = self.client.get(url)
        self.assertEqual(response1.status_code, 200)
        content1 = response1.json()

        # Modify plugin
        plugin.body = "<p>Modified content</p>"
        plugin.save()

        # Second call - should get cached data (old content)
        response2 = self.client.get(url)
        self.assertEqual(response2.status_code, 200)
        content2 = response2.json()

        # Content should be the same because of cache
        self.assertEqual(
            content1["content"][0]["body"],
            content2["content"][0]["body"],
            "Public mode should use cache and return old content",
        )

    def test_preview_and_public_cache_isolation(self):
        """
        Verify that preview and public modes don't share cache.
        Draft content should never leak to public API.
        """
        from django.urls import reverse
        from django.test import Client

        # Create a page with placeholder
        page = create_page(
            title="Test Page",
            template="page.html",
            language=self.language,
        )
        placeholder = page.get_placeholders(self.language).first()

        # Add a plugin
        plugin = add_plugin(
            placeholder,
            "TextPlugin",
            self.language,
            body="<p>Original content</p>",
        )

        # Build API URL for placeholder detail
        url = reverse(
            "placeholder-detail",
            args=[
                self.language,
                placeholder.content_type_id,
                placeholder.object_id,
                placeholder.slot,
            ],
        )

        # Use anonymous client for public mode (uses cache)
        public_client = Client()

        # Get public content (will be cached)
        public_response = public_client.get(url)
        self.assertEqual(public_response.status_code, 200)
        public_content = public_response.json()

        # Modify plugin (simulate draft change)
        plugin.body = "<p>DRAFT CONTENT - NOT PUBLISHED</p>"
        plugin.save()

        # Use authenticated staff client for preview mode (bypasses cache)
        preview_client = Client()
        preview_client.force_login(self.get_staff_user_with_no_permissions())

        # Get preview content (no cache, fresh data with changes)
        preview_response = preview_client.get(url + "?preview=1")
        self.assertEqual(preview_response.status_code, 200)
        preview_content = preview_response.json()

        # Get public content again (should still be cached, old content)
        public_response_after = public_client.get(url)
        self.assertEqual(public_response_after.status_code, 200)
        public_content_after = public_response_after.json()

        # Public content should not change (cache hit)
        self.assertEqual(
            public_content["content"][0]["body"],
            public_content_after["content"][0]["body"],
            "Public mode should return cached old content",
        )

        # Preview content should be different (has draft changes)
        self.assertNotEqual(
            preview_content["content"][0]["body"],
            public_content["content"][0]["body"],
            "Preview mode should show updated content, not cached content",
        )
        self.assertEqual(
            preview_content["content"][0]["body"],
            "<p>DRAFT CONTENT - NOT PUBLISHED</p>",
            "Preview should show the modified content",
        )

    def test_preview_parameter_in_details_url(self):
        """
        Verify that preview parameter is preserved in details URL.
        """
        from djangocms_rest.serializers.placeholders import PlaceholderSerializer

        # Create a page with placeholder
        page = create_page(
            title="Test Page",
            template="page.html",
            language=self.language,
        )
        placeholder = page.get_placeholders(self.language).first()

        request = self.factory.get("/api/en/placeholder/", {"preview": "1"})
        request.user = self.get_superuser()
        request._preview_mode = True

        serializer = PlaceholderSerializer(
            placeholder,
            request=request,
            language=self.language,
        )
        data = serializer.to_representation(placeholder)
        # Details URL should contain preview parameter
        self.assertIn("preview=1", data["details"])

    def test_preview_query_parameter_preserved_in_serializer(self):
        """
        Verify that preview parameter is preserved in get_params.
        """
        from djangocms_rest.serializers.placeholders import PlaceholderSerializer

        page = create_page(
            title="Test",
            template="page.html",
            language=self.language,
        )
        placeholder = page.get_placeholders(self.language).first()

        request = self.factory.get("/api/en/placeholder/", {"preview": "1", "html": "1"})
        request.user = self.get_superuser()

        serializer = PlaceholderSerializer(
            placeholder,
            request=request,
            language=self.language,
        )
        data = serializer.to_representation(placeholder)

        # Both preview and html should be in details URL
        self.assertIn("preview=1", data["details"])
        self.assertIn("html=1", data["details"])


class MenuCacheTests(BaseCMSRestTestCase):
    """
    Test cache behavior for menu endpoints.

    Note: These tests primarily document that menu caching faces similar
    invalidation challenges as placeholder caching. Menu data may be cached
    at multiple levels (CMS menu_pool, REST API response, etc.).
    """

    def setUp(self):
        super().setUp()
        cache.clear()
        self.site = Site.objects.get_current()
        self.language = "en"

    def tearDown(self):
        cache.clear()

    def test_menu_endpoint_responds(self):
        """
        Basic test: Verify menu endpoint returns valid response.
        """
        from django.urls import reverse

        # Create a page so menu has content
        create_page(
            title="Test Page",
            template="page.html",
            slug="test-page",
            language=self.language,
            in_navigation=True,
        )

        url = reverse("menu", args=[self.language])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        menu = response.json()
        self.assertIsInstance(menu, list)
        self.assertIn("http://testserver/", menu[1]["url"])  # Basic check

    def test_menu_preview_parameter_support(self):
        """
        Document that menu endpoint accepts preview parameter.

        Note: Menu caching behavior with preview mode may differ from
        placeholder caching as menus use Django CMS's menu_pool which
        has its own caching mechanism.
        """
        from django.urls import reverse

        staff_user = self.get_staff_user_with_no_permissions()
        self.client.force_login(staff_user)

        create_page(
            title="Test Page",
            template="page.html",
            language=self.language,
            in_navigation=True,
        )
        url = reverse("menu", args=[self.language])

        # Menu endpoint should accept preview parameter without error
        response = self.client.get(f"{url}?preview=1")
        self.assertEqual(response.status_code, 200)
        menu = response.json()
        self.assertIsInstance(menu, list)
        self.assertIn("/cms/placeholder/object/", menu[0]["url"])  # Preview urls

    def test_menu_cache_with_page_changes(self):
        """
        Document that menu does not reflect page changes immediately.

        This is expected - menu data comes from Django CMS's menu_pool
        which has its own caching layer separate from our REST API
        placeholder caching.
        """
        from django.urls import reverse

        page = create_page(
            title="Original Title",
            template="page.html",
            language=self.language,
            in_navigation=True,
        )

        url = reverse("menu", args=[self.language])

        # Get menu
        response1 = self.client.get(url)
        self.assertEqual(response1.status_code, 200)

        # Modify page title
        page_content = page.get_content_obj(self.language)
        page_content.title = "Modified Title"
        page_content.save()

        # Get menu again
        response2 = self.client.get(url)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response1.content, response2.content)

    def test_menu_preview_cache_with_page_changes(self):
        """
        Document that menu does not reflect page changes immediately.

        This is expected - menu data comes from Django CMS's menu_pool
        which has its own caching layer separate from our REST API
        placeholder caching.
        """
        from django.urls import reverse

        # Login as superuser for preview access
        self.client.force_login(self.get_superuser())

        page = create_page(
            title="Original Title",
            template="page.html",
            language=self.language,
            in_navigation=True,
        )

        url = reverse("menu", args=[self.language]) + "?preview=1"

        # Get menu
        response1 = self.client.get(url)
        self.assertEqual(response1.status_code, 200)

        # Modify page title
        page_content = page.get_content_obj(self.language)
        page_content.title = "Modified Title"
        page_content.save()

        # Get menu again
        response2 = self.client.get(url)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response1.content, response2.content)

        # Invalidate cache
        from menus.menu_pool import menu_pool

        menu_pool.clear(all=True)
        response3 = self.client.get(url)
        self.assertEqual(response3.status_code, 200)
        self.assertNotEqual(response1.content, response3.content)
