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
