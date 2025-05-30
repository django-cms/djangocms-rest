from rest_framework.reverse import reverse

from djangocms_rest.serializers.pages import PageMetaSerializer, PageTreeSerializer
from tests.base import BaseCMSRestTestCase
from tests.types import PAGE_TREE_META_FIELD_TYPES
from tests.utils import assert_field_types


class PageTreeListAPITestCase(BaseCMSRestTestCase):
    def test_get(self):
        """
        Test the page tree list endpoint (/api/{language}/pages-tree/).

        Verifies:
        - Endpoint returns correct HTTP status code
        - Response contains hierarchical page structure
        - All pages contain required fields
        - All fields have correct data types
        - Child pages follow same structure as parent pages
        - Invalid language code returns 404
        """

        type_checks = PAGE_TREE_META_FIELD_TYPES

        # GET
        response = self.client.get(reverse("page-tree-list", kwargs={"language": "en"}))
        self.assertEqual(response.status_code, 200)
        data = response.json()

        # Data & Type Validation
        self.assertIsInstance(data, list)
        for page in data:
            for field, expected_type in type_checks.items():
                assert_field_types(
                    self,
                    page,
                    field,
                    expected_type,
                )

            # Nested Data & Type Validation
            for child in page["children"]:
                for field, expected_type in type_checks.items():
                    self.assertIn(field, child)
                    if isinstance(expected_type, tuple):
                        self.assertTrue(isinstance(child[field], expected_type))
                    else:
                        self.assertIsInstance(child[field], expected_type)

        # Check Invalid Language
        response = self.client.get(reverse("page-tree-list", kwargs={"language": "xx"}))
        self.assertEqual(response.status_code, 404)

        # GET PREVIEW
        response = self.client.get(reverse("preview-page-tree-list", kwargs={"language": "en"}))
        self.assertEqual(response.status_code, 403)

        response = self.client.get(reverse("preview-page-tree-list", kwargs={"language": "xx"}))
        self.assertEqual(response.status_code, 403)

    # GET PREVIEW - Protected
    def test_get_protected(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("preview-page-tree-list", kwargs={"language": "en"}))
        self.assertEqual(response.status_code, 200)

    # TEST SERIALIZER EDGE CASES
    def test_tree_serializer_type_error(self):
        """Test that PageTreeSerializer raises TypeError when a tree is not a dict"""
        # Create a mock dictionary with the tree parameter explicitly as a string
        mock_kwargs = {"tree": "not_a_dict"}
        with self.assertRaises(TypeError):
            PageTreeSerializer(**mock_kwargs)

    def test_page_meta_serializer_many_init(self):
        """Test that PageMetaSerializer.many_init returns a PageTreeSerializer instance"""
        serializer = PageMetaSerializer.many_init(context={})
        self.assertIsInstance(serializer, PageTreeSerializer)
