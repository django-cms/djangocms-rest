import unittest

from cms.api import add_plugin, create_page
from cms.models import PageContent
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from rest_framework.reverse import reverse

from tests.base import BaseCMSRestTestCase
from tests.types import PLACEHOLDER_FIELD_TYPES
from tests.utils import assert_field_types

try:
    from djangocms_alias.models import Alias, AliasContent, Category

    HAS_ALIAS = True
except ImportError:
    HAS_ALIAS = False


@unittest.skipUnless(HAS_ALIAS and apps.is_installed("djangocms_alias"), "djangocms_alias is not installed")
class AliasAPITestCase(BaseCMSRestTestCase):
    @classmethod
    def setUpClass(cls):
        """
        Add alias with plugin content to a test page placeholder.
        """
        super().setUpClass()

        cls.page = create_page(
            title="Alias Test Page",
            template="INHERIT",
            language="en",
            in_navigation=True,
        )
        cls.page_content = PageContent.objects.get(page=cls.page, language="en")
        cls.page_content_type = ContentType.objects.get(model="pagecontent")
        cls.page_placeholder = cls.page.get_placeholders(language="en").get(slot="content")

        cls.category = Category.objects.create()
        cls.category.set_current_language("en")
        cls.category.name = "Alias Category"
        cls.category.save()

        cls.alias = Alias.objects.create(category=cls.category, static_code="test-alias")
        cls.alias_content = AliasContent.objects.create(
            alias=cls.alias,
            name="Alias Content",
            language="en",
        )
        cls.alias_placeholder = cls.alias_content.placeholder

        add_plugin(
            placeholder=cls.alias_placeholder,
            plugin_type="TextPlugin",
            language="en",
            body="<p>Alias text</p>",
        )

        add_plugin(
            placeholder=cls.page_placeholder,
            plugin_type="Alias",
            language="en",
            alias=cls.alias,
        )

    def test_get(self):
        """
        Tests alias plugin rendering via the placeholder detail endpoint.

        Verifies:
        - Endpoint returns 200 OK for valid requests
        - Response structure matches placeholder field types
        - Alias plugin resolves its content with nested plugins
        """

        type_checks = PLACEHOLDER_FIELD_TYPES

        plugin_type_checks = {
            "plugin_type": str,
            "content": list,
        }

        # GET request
        response = self.client.get(
            reverse(
                "placeholder-detail",
                kwargs={
                    "language": "en",
                    "content_type_id": self.page_content_type.id,
                    "object_id": self.page_content.id,
                    "slot": "content",
                },
            )
        )
        self.assertEqual(response.status_code, 200)
        placeholder = response.json()

        # Placeholder Validation
        for field, expected_type in type_checks.items():
            assert_field_types(
                self,
                placeholder,
                field,
                expected_type,
            )

        # Plugin Type Validation
        for plugin in placeholder["content"]:
            for field, expected_type in plugin_type_checks.items():
                assert_field_types(
                    self,
                    plugin,
                    field,
                    expected_type,
                )

        # Alias content validation
        alias_plugin = placeholder["content"][0]
        self.assertTrue(alias_plugin["content"])
        self.assertEqual(alias_plugin["content"][0]["plugin_type"], "TextPlugin")
        self.assertIn("Alias text", alias_plugin["content"][0]["body"])

    def test_circular_alias(self):
        """
        Tests that a circular alias reference returns empty content
        instead of recursing infinitely.
        """
        # Add the alias as a plugin inside its own placeholder
        add_plugin(
            placeholder=self.alias_placeholder,
            plugin_type="Alias",
            language="en",
            alias=self.alias,
        )

        response = self.client.get(
            reverse(
                "placeholder-detail",
                kwargs={
                    "language": "en",
                    "content_type_id": self.page_content_type.id,
                    "object_id": self.page_content.id,
                    "slot": "content",
                },
            )
        )
        self.assertEqual(response.status_code, 200)
        placeholder = response.json()

        # The top-level alias plugin should resolve its content
        alias_plugin = placeholder["content"][0]
        self.assertTrue(alias_plugin["content"])

        # The nested self-referencing alias plugin should have empty content
        nested_alias = next(
            plugin for plugin in alias_plugin["content"] if plugin.get("plugin_type") in ("Alias", "AliasPlugin")
        )
        self.assertEqual(nested_alias["content"], [])
