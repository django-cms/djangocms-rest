from rest_framework.reverse import reverse

from tests.base import BaseCMSRestTestCase
from tests.types import PLUGIN_FIELD_TYPES
from tests.utils import assert_field_types


class PluginListTestCase(BaseCMSRestTestCase):
    maxDiff = None

    def test_get(self):
        from cms.plugin_pool import plugin_pool

        type_checks = PLUGIN_FIELD_TYPES
        expected_plugin_types = [plugin.__name__ for plugin in plugin_pool.get_all_plugins()]
        expected_dummy_plugin_signature = {
            "plugin_type": "DummyNumberPlugin",
            "title": "Dummy Number Plugin",
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "integer": {"type": "integer"},
                "json": {"type": "object"},
                "float": {"type": "number"},
                "title": {"enum": ["title", "subtitle", "header"], "type": "string"},
                "kvp": {
                    "properties": {
                        "prop1": {"type": "string"},
                        "prop2": {"type": "string"},
                        "prop3": {"type": "string"},
                    },
                    "type": "object",
                },
            },
        }

        # GET
        response = self.client.get(reverse("plugin-list"))
        self.assertEqual(response.status_code, 200)
        data = response.json()

        # Data & Type Validation
        self.assertIsInstance(data, list)
        self.assertTrue(len(data) > 0, "Plugin list should not be empty")

        # Check completeness
        for plugin_type in expected_plugin_types:
            self.assertIn(
                plugin_type,
                [plugin.get("plugin_type") for plugin in data],
                f"Plugin type {plugin_type} not found in response",
            )

        # Check Plugin Types
        for plugin in data:
            for field, expected_type in type_checks.items():
                assert_field_types(
                    self,
                    plugin,
                    field,
                    expected_type,
                    f"plugin {plugin.get('plugin_type', 'unknown')}",
                )

        # Check signature of DummyNumberPlugin
        dummy_plugin = next(
            (plugin for plugin in data if plugin.get("plugin_type") == "DummyNumberPlugin"),
            None,
        )
        self.assertIsNotNone(dummy_plugin, "DummyNumberPlugin not found in response")
        # "position" is a base_exclude member and must be skipped from the schema.
        self.assertNotIn("position", dummy_plugin["properties"])
        self.assertDictEqual(dummy_plugin, expected_dummy_plugin_signature)

    def test_relations_are_typed_as_strings(self):
        """Foreign keys serialize to an API endpoint (a string), not a raw pk.

        Regression test for #68: the definition endpoint reported ``integer`` for
        relational fields while the content endpoint returned a URL string, which
        broke type validation in generated clients.
        """
        response = self.client.get(reverse("plugin-list"))
        self.assertEqual(response.status_code, 200)
        definitions = {plugin["plugin_type"]: plugin["properties"] for plugin in response.json()}

        # A nullable FK to a CMS page ...
        self.assertEqual(
            definitions["DummyLinkPlugin"]["page"],
            {"type": "string", "nullable": True},
        )
        # ... and a nullable FK to a third-party model behave the same.
        self.assertEqual(
            definitions["DummyImagePlugin"]["filer_image"],
            {"type": "string", "nullable": True},
        )

    def test_parent_plugin_type_is_nullable(self):
        """``parent_plugin_type`` is ``null`` for top-level plugins, so say so."""
        response = self.client.get(reverse("plugin-list"))
        self.assertEqual(response.status_code, 200)

        for plugin in response.json():
            properties = plugin["properties"]
            if "parent_plugin_type" not in properties:
                continue  # Plugins with a custom serializer_class opt in themselves.
            self.assertEqual(
                properties["parent_plugin_type"],
                {"type": "string", "nullable": True},
                f"{plugin['plugin_type']} does not declare parent_plugin_type as nullable",
            )
