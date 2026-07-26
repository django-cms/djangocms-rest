"""Prototype coverage for third-party API extensions.

Exercises the two contracts:

* cms_config endpoints (alias-style, independent of pages)
* path-mirrored apphook REST urls + page discovery block (stories-style)
"""

import sys
from importlib import reload
from types import SimpleNamespace
from unittest import mock

from django.apps import apps
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ImproperlyConfigured
from django.db.utils import OperationalError, ProgrammingError
from django.urls import clear_url_caches, path

from cms.api import create_page, create_page_content
from cms.appresolver import clear_app_resolvers

from djangocms_rest import appresolver
from djangocms_rest.cms_config import RESTExtension
from djangocms_rest.serializers.pages import get_apphook_api_endpoint
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

    def test_nested_apphook_pattern_is_reachable(self):
        response = self.client.get("/api/en/blog/posts/hello-world/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"language": "en", "slug": "hello-world"})


class RESTApphookResolverTestCase(RESTTestCase):
    """Unit-level coverage of :mod:`djangocms_rest.appresolver`.

    These exercise the resolver directly, so no urlconf reload is needed and the
    pages created here are rolled back with the test transaction.
    """

    def test_rest_apphook_ignores_pages_without_apphook(self):
        self.assertIsNone(appresolver._rest_apphook(None))
        self.assertIsNone(appresolver._rest_apphook(""))

    def test_rest_apphook_ignores_apphooks_without_rest_urls(self):
        self.assertIsNone(appresolver._rest_apphook("DemoPlainApphook"))
        self.assertIsNone(appresolver._rest_apphook("NoSuchApphook"))

    def test_rest_apphook_accepts_rest_capable_apphook(self):
        app = appresolver._rest_apphook("DemoStoriesApphook")
        self.assertIsNotNone(app)
        self.assertEqual(app.app_name, "demo_stories")

    def test_plain_apphook_page_is_not_mounted(self):
        create_page(
            "Plain",
            language="en",
            template="INHERIT",
            apphook="DemoPlainApphook",
            apphook_namespace="demo_plain",
        )
        self.assertEqual(appresolver._get_rest_app_patterns(None), [])

    def test_same_path_in_several_languages_mounts_once(self):
        page = create_page(
            "Blog",
            language="en",
            template="INHERIT",
            slug="blog",
            apphook="DemoStoriesApphook",
            apphook_namespace="demo_stories",
        )
        # A second language whose localized path is identical -- the mount is
        # language-agnostic, so it must be de-duplicated.
        create_page_content("it", "Blog", page, slug="blog")

        patterns = appresolver._get_rest_app_patterns(None)
        # ``tests.test_app.rest_urls`` declares two patterns; one mount only.
        self.assertEqual(len(patterns), 2)

    def test_site_scoped_and_site_independent_modes_agree(self):
        create_page(
            "Blog",
            language="en",
            template="INHERIT",
            slug="blog",
            apphook="DemoStoriesApphook",
            apphook_namespace="demo_stories",
        )
        site_scoped = appresolver._get_rest_app_patterns(Site.objects.get_current())
        site_independent = appresolver._get_rest_app_patterns(None)
        self.assertEqual(len(site_scoped), len(site_independent))
        self.assertEqual(len(site_scoped), 2)

    def test_falls_back_to_site_independent_mode_without_site_id(self):
        with (
            mock.patch.object(appresolver.Site.objects, "get_current", side_effect=ImproperlyConfigured),
            mock.patch.object(
                appresolver, "_get_rest_app_patterns", wraps=appresolver._get_rest_app_patterns
            ) as patched,
        ):
            self.assertEqual(appresolver.get_rest_app_patterns(), [])
        self.assertEqual(patched.call_args_list, [mock.call(None)])

    def test_returns_no_patterns_when_the_database_is_not_ready(self):
        for error in (OperationalError, ProgrammingError):
            with (
                self.subTest(error=error),
                mock.patch.object(appresolver, "_get_rest_app_patterns", side_effect=error),
            ):
                self.assertEqual(appresolver.get_rest_app_patterns(), [])


class RESTExtensionTestCase(RESTTestCase):
    """Unit-level coverage of the cms_config collector and its url hook."""

    def test_configure_app_ignores_apps_without_endpoints(self):
        extension = RESTExtension()
        extension.configure_app(SimpleNamespace())
        extension.configure_app(SimpleNamespace(cms_rest_endpoints=[]))
        self.assertEqual(extension.endpoints, [])

    def test_configure_app_collects_endpoints(self):
        extension = RESTExtension()
        pattern = path("demo/", lambda request: None, name="demo")
        extension.configure_app(SimpleNamespace(cms_rest_endpoints=[pattern]))
        self.assertEqual(extension.endpoints, [pattern])

    def test_extension_endpoints_are_empty_while_the_app_registry_is_not_ready(self):
        # Imported lazily: importing the urlconf builds the apphook patterns,
        # which hits the database.
        from djangocms_rest.urls import _extension_endpoints

        with mock.patch.object(apps, "get_app_config", side_effect=LookupError):
            self.assertEqual(_extension_endpoints(), [])

    def test_extension_endpoints_are_empty_before_cms_config_autodiscovery(self):
        from djangocms_rest.urls import _extension_endpoints

        # ``cms_extension`` is only set on the app config once cms has run its
        # autodiscovery; before that the attribute lookup raises.
        with mock.patch.object(apps, "get_app_config", return_value=SimpleNamespace()):
            self.assertEqual(_extension_endpoints(), [])


class ApphookDiscoveryBlockTestCase(RESTTestCase):
    """Unit-level coverage of the ``app`` block on the page serializer."""

    def test_no_apphook_yields_no_discovery_block(self):
        page = create_page("Plain", language="en", template="INHERIT", slug="plain")
        self.assertIsNone(get_apphook_api_endpoint(None, page, "en"))

    def test_apphook_without_rest_urls_yields_no_discovery_block(self):
        page = create_page(
            "Plain",
            language="en",
            template="INHERIT",
            slug="plain",
            apphook="DemoPlainApphook",
            apphook_namespace="demo_plain",
        )
        self.assertIsNone(get_apphook_api_endpoint(None, page, "en"))

    def test_unknown_apphook_yields_no_discovery_block(self):
        page = create_page("Plain", language="en", template="INHERIT", slug="plain")
        page.application_urls = "NoSuchApphook"
        self.assertIsNone(get_apphook_api_endpoint(None, page, "en"))

    def test_apphook_on_the_homepage_points_at_the_language_root(self):
        page = create_page(
            "Blog",
            language="en",
            template="INHERIT",
            slug="blog",
            apphook="DemoStoriesApphook",
            apphook_namespace="demo_stories",
        )
        page.set_as_homepage()
        page.refresh_from_db()
        # Without an instance namespace the block falls back to ``app_name``.
        page.application_namespace = ""

        block = get_apphook_api_endpoint(None, page, "en")
        self.assertEqual(block["namespace"], "demo_stories")
        # The homepage has an empty localized path, so the apphook root *is*
        # the language root of the API.
        self.assertTrue(block["api_endpoint"].endswith("/api/en/"))
