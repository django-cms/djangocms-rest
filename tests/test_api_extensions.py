"""Prototype coverage for third-party API extensions.

Exercises the two contracts:

* cms_config endpoints (alias-style, independent of pages)
* path-mirrored apphook REST urls + page discovery block (stories-style)
"""

import sys
from importlib import reload

from django.conf import settings
from django.urls import clear_url_caches

from cms.api import create_page
from cms.appresolver import clear_app_resolvers

from tests.base import RESTTestCase


def reload_urlconf():
    """Rebuild the urlconf so newly mounted apphook patterns are picked up."""
    clear_app_resolvers()
    clear_url_caches()
    for module in ("djangocms_rest.urls", settings.ROOT_URLCONF):
        if module in sys.modules:
            reload(sys.modules[module])


class CMSConfigEndpointTestCase(RESTTestCase):
    """Alias-style: an endpoint contributed via cms_config is mounted."""

    def test_extension_endpoint_is_collected(self):
        from django.apps import apps

        extension = apps.get_app_config("djangocms_rest").cms_extension
        names = {p.name for p in extension.endpoints}
        self.assertIn("demo-alias-detail", names)

    def test_extension_endpoint_responds(self):
        response = self.client.get("/api/en/demo-aliases/42/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"id": 42, "language": "en", "kind": "demo-alias"},
        )


class ApphookRESTTestCase(RESTTestCase):
    """Stories-style: an apphook page exposes its REST urls path-mirrored."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.page = create_page(
            "Blog",
            language="en",
            template="INHERIT",
            apphook="DemoStoriesApphook",
            apphook_namespace="demo_stories",
            in_navigation=True,
        )
        reload_urlconf()

    @classmethod
    def tearDownClass(cls):
        from cms.models import Page

        Page.objects.all().delete()
        reload_urlconf()
        super().tearDownClass()

    def test_page_serializer_exposes_app_block(self):
        response = self.client.get("/api/en/pages/blog/")
        self.assertEqual(response.status_code, 200)
        app = response.json()["app"]
        self.assertEqual(app["namespace"], "demo_stories")
        self.assertTrue(app["api_endpoint"].endswith("/api/en/blog/"))

    def test_apphook_rest_endpoint_is_mounted_path_mirrored(self):
        response = self.client.get("/api/en/blog/posts/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"language": "en", "posts": []})

    def test_language_is_captured_from_the_url(self):
        # The ``<slug:language>`` segment is captured explicitly, exactly like
        # every other endpoint in the API.
        response = self.client.get("/api/de/blog/posts/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["language"], "de")
