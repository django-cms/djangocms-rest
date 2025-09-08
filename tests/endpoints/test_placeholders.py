from cms.api import add_plugin, create_page
from cms.models import PageContent
from django.contrib.contenttypes.models import ContentType
from rest_framework.reverse import reverse

from tests.base import BaseCMSRestTestCase
from tests.types import PLACEHOLDER_FIELD_TYPES
from tests.utils import assert_field_types


class PlaceholdersAPITestCase(BaseCMSRestTestCase):
    @classmethod
    def setUpClass(cls):
        """
        Add placeholder and plugin to a test page.
        """
        super().setUpClass()

        cls.page = create_page(
            title="Test Page",
            template="INHERIT",
            language="en",
            in_navigation=True,
        )
        cls.page_content = PageContent.objects.get(page=cls.page, language="en")
        cls.page_content_type = ContentType.objects.get(model="pagecontent")
        cls.placeholder = cls.page.get_placeholders(language="en").get(slot="content")
        cls.plugin = add_plugin(
            placeholder=cls.placeholder,
            plugin_type="TextPlugin",
            language="en",
            body="<p>Test content</p>",
            json={
                "type": "doc",
                "content": [
                    {
                        "type": "paragraph",
                        "attrs": {"textAlign": "left"},
                        "content": [{"text": "Test content", "type": "text"}],
                    }
                ],
            },
        )

    def test_get(self):
        """
        Tests the placeholder detail endpoint API functionality.

        Verifies:
        - Endpoint returns 200 OK for valid requests
        - Endpoint returns 404 for invalid language codes
        - Response structure contains required fields
        - Plugin content is properly structured
        - All fields have correct data types
        - Content list contains valid plugin data
        """

        type_checks = PLACEHOLDER_FIELD_TYPES

        plugin_type_checks = {
            "plugin_type": str,
            "body": str,
            "json": dict,
            "rte": str,
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

        # Test with html=1 parameter
        response = self.client.get(
            reverse(
                "placeholder-detail",
                kwargs={
                    "language": "en",
                    "content_type_id": self.page_content_type.id,
                    "object_id": self.page_content.id,
                    "slot": "content",
                },
            ),
            data={"html": "1"},
        )
        self.assertEqual(response.status_code, 200)

        # Error case - Invalid language
        response = self.client.get(
            reverse(
                "placeholder-detail",
                kwargs={
                    "language": "xx",
                    "content_type_id": self.page_content_type.id,
                    "object_id": self.page_content.id,
                    "slot": "content",
                },
            )
        )
        self.assertEqual(response.status_code, 404)

        # Error case - Invalid content type
        response = self.client.get(
            reverse(
                "placeholder-detail",
                kwargs={
                    "language": "en",
                    "content_type_id": 99999,
                    "object_id": self.page_content.id,
                    "slot": "content",
                },
            )
        )
        self.assertEqual(response.status_code, 404)

        # Error case - Invalid object ID
        response = self.client.get(
            reverse(
                "placeholder-detail",
                kwargs={
                    "language": "en",
                    "content_type_id": self.page_content_type.id,
                    "object_id": 99999,
                    "slot": "content",
                },
            )
        )
        self.assertEqual(response.status_code, 404)

        # Error case - Invalid slot
        response = self.client.get(
            reverse(
                "placeholder-detail",
                kwargs={
                    "language": "en",
                    "content_type_id": self.page_content_type.id,
                    "object_id": self.page_content.id,
                    "slot": "nonexistent",
                },
            )
        )
        self.assertEqual(response.status_code, 404)

        # GET PREVIEW
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
            + "?preview"
        )
        self.assertEqual(response.status_code, 403)

    # GET PREVIEW - Protected
    def test_get_protected(self):
        self.client.force_login(self.user)
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
            + "?preview"
        )
        self.assertEqual(response.status_code, 200)

    def test_serialize_page_fk(self):
        add_plugin(
            placeholder=self.placeholder,
            plugin_type="DummyLinkPlugin",
            language="en",
            page=self.page,
            label="Test Link",
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
        rendered_plugin = response.json()["content"][-1]
        self.assertIn("page", rendered_plugin)
        self.assertIsInstance(rendered_plugin["page"], str)
        self.assertEqual(
            rendered_plugin["page"],
            f"http://testserver{self.page.get_api_endpoint('en')}",
        )
