from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.shortcuts import get_current_site
from django.core.cache import cache

from cms.api import add_plugin
from cms.models import PageContent

from rest_framework.reverse import reverse

from djangocms_rest.serializers.utils.cache import get_placeholder_rest_cache
from tests.base import BaseCMSRestTestCase


class CachingAPITestCase(BaseCMSRestTestCase):
    @classmethod
    def setUpClass(cls):
        """
        Set up test data for cache testing, using existing pages from BaseCMSRestTestCase.
        """
        super().setUpClass()
        # Use the first page created in BaseCMSRestTestCase
        cls.page = cls.pages[0]
        cls.page_content = PageContent.objects.get(page=cls.page, language="en")
        cls.page_content_type = ContentType.objects.get(model="pagecontent")
        cls.placeholder = cls.page.get_placeholders(language="en").get(slot="content")

        # Add a plugin to the placeholder for testing
        cls.plugin = add_plugin(
            placeholder=cls.placeholder,
            plugin_type="TextPlugin",
            language="en",
            body="<p>Cache test content</p>",
        )

    def setUp(self):
        """Clear the cache before each test"""
        cache.clear()

    def get_placeholder_url(self):
        """Helper to generate the placeholder URL"""
        return reverse(
            "placeholder-detail",
            kwargs={
                "language": "en",
                "content_type_id": self.page_content_type.id,
                "object_id": self.page_content.id,
                "slot": "content",
            },
        )

    def test_cache_hit_and_miss(self):
        """
        Test the cache hit-and-miss functionality:
        1. The first request should miss the cache and store content
        2. The second request should hit the cache and return the same content
        3. After clearing the cache, the request should miss again
        """

        # Request #1 - should miss cache
        response1 = self.client.get(self.get_placeholder_url())
        self.assertEqual(response1.status_code, 200)
        placeholder1 = response1.json()

        # Request #1 - Check if the cache contains our content
        cached_content = get_placeholder_rest_cache(
            self.placeholder, lang="en", site_id=get_current_site(None).pk, request=None
        )
        self.assertIsNotNone(cached_content, "Cache was not populated after first request")

        # Request #1 - Modify content but don't invalidate cache (testing if cache is used)
        self.plugin.body = "<p>Updated content that should not appear while cached</p>"
        self.plugin.save()

        # Request #2 - should hit cache
        response2 = self.client.get(self.get_placeholder_url())
        self.assertEqual(response2.status_code, 200)
        placeholder2 = response2.json()

        # Request #2 - Responses should be identical (using cached content)
        self.assertEqual(placeholder1, placeholder2, "Responses differ - cache might not be working")

        # Request #3 - Clear cache and verify we get fresh content
        cache.clear()
        response3 = self.client.get(self.get_placeholder_url())
        self.assertEqual(response3.status_code, 200)
        placeholder3 = response3.json()

        # Request #3 - Content should be different after cache cleared (should contain updated text)
        self.assertNotEqual(
            placeholder1["content"],
            placeholder3["content"],
            "After clearing cache, content should be different",
        )

        # Request #3 - Verify the updated content is present in the response
        self.assertIn("Updated content", placeholder3["content"][0]["body"])

    def test_staff_bypass_cache(self):
        """
        Test that staff users bypass the cache:
        1. Anonymous user request populates cache
        2. Content is updated
        3. Staff user should see updated content (bypass cache)
        4. Anonymous user should still see cached content
        """

        # Anonymous request #1 - Populate cache
        response1 = self.client.get(self.get_placeholder_url())
        self.assertEqual(response1.status_code, 200)
        placeholder1 = response1.json()

        # Anonymous request #1 - Update content
        original_content = self.plugin.body
        self.plugin.body = "<p>Staff should see this content</p>"
        self.plugin.save()

        # Staff request #2 - Bypass cache
        self.client.force_login(self.user)
        response2 = self.client.get(self.get_placeholder_url())
        self.assertEqual(response2.status_code, 200)
        placeholder2 = response2.json()

        # Staff request #2 - Update content
        self.assertIn("Staff should see this content", placeholder2["content"][0]["body"])
        self.assertNotEqual(
            placeholder1["content"],
            placeholder2["content"],
            "Staff user should bypass cache and see updated content",
        )

        # Anonymous request #3 - fetch content from request #1
        self.client.logout()
        response3 = self.client.get(self.get_placeholder_url())
        self.assertEqual(response3.status_code, 200)
        placeholder3 = response3.json()
        self.assertEqual(placeholder1, placeholder3, "Anonymous user should still get cached content")

        # Restore content
        self.plugin.body = original_content
        self.plugin.save()

    def test_cache_version_edge_cases(self):
        """
        Test edge cases in cache version functions to improve code coverage.
        """
        from django.contrib.sites.shortcuts import get_current_site
        from django.core.cache import cache

        from djangocms_rest.serializers.utils.cache import (
            _get_placeholder_cache_version,
            _set_placeholder_cache_version,
        )

        # Clear the cache to start with a clean state
        cache.clear()

        # Test _get_placeholder_cache_version with no cached data (should create new)
        version1, vary_list1 = _get_placeholder_cache_version(self.placeholder, "en", get_current_site(None).pk)
        self.assertIsNotNone(version1)
        self.assertEqual(vary_list1, [])

        # Test _set_placeholder_cache_version with None version (should create new)
        _set_placeholder_cache_version(self.placeholder, "en", get_current_site(None).pk, None)
        version2, _vary_list2 = _get_placeholder_cache_version(self.placeholder, "en", get_current_site(None).pk)
        self.assertIsNotNone(version2)
        self.assertNotEqual(version1, version2)  # Should be a new timestamp

        # Test _set_placeholder_cache_version with negative version (should create new)
        _set_placeholder_cache_version(self.placeholder, "en", get_current_site(None).pk, -1)
        version3, _vary_list3 = _get_placeholder_cache_version(self.placeholder, "en", get_current_site(None).pk)
        self.assertIsNotNone(version3)
        self.assertNotEqual(version2, version3)  # Should be a new timestamp

        # Test _set_placeholder_cache_version with None vary_on_list
        _set_placeholder_cache_version(self.placeholder, "en", get_current_site(None).pk, 12345, None)
        version4, vary_list4 = _get_placeholder_cache_version(self.placeholder, "en", get_current_site(None).pk)
        self.assertEqual(version4, 12345)
        self.assertEqual(vary_list4, [])
