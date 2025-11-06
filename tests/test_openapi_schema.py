"""
Tests for OpenAPI schema generation with drf-spectacular.

Ensures that all serializer fields are properly documented in the OpenAPI schema,
particularly dynamically populated fields like PlaceholderSerializer.content.
"""
from rest_framework.reverse import reverse

from tests.base import RESTTestCase


class OpenAPISchemaTestCase(RESTTestCase):
    """Test OpenAPI schema generation for djangocms-rest endpoints."""

    def test_schema_endpoint_accessible(self):
        """
        Test that the OpenAPI schema endpoint is accessible.
        """
        url = reverse("schema")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("openapi", response.data)
        self.assertIn("info", response.data)
        self.assertIn("paths", response.data)
        self.assertIn("components", response.data)

    def test_all_endpoints_have_valid_schemas(self):
        """
        Test that all endpoints have valid schema definitions.

        Ensures that:
        - All paths have at least one operation defined
        - All operations have response schemas
        - No operations have error markers
        """
        url = reverse("schema")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        paths = response.data.get("paths", {})
        self.assertTrue(len(paths) > 0, "Schema should contain at least one endpoint")

        errors = []
        for path, path_item in paths.items():
            # Check that path has at least one HTTP method
            methods = [m for m in path_item.keys() if m in ["get", "post", "put", "patch", "delete"]]
            if not methods:
                errors.append(f"Path '{path}' has no HTTP methods defined")
                continue

            for method, operation in path_item.items():
                if method not in ["get", "post", "put", "patch", "delete"]:
                    continue

                # Check that operation has responses
                if "responses" not in operation:
                    errors.append(f"{method.upper()} {path} has no 'responses' defined")
                    continue

                # Check for at least one successful response (2xx)
                responses = operation["responses"]
                has_success = any(str(code).startswith("2") for code in responses.keys())
                if not has_success:
                    errors.append(f"{method.upper()} {path} has no successful (2xx) response defined")

                # Check that 200/201 responses have content with schema
                for code in ["200", "201"]:
                    if code in responses:
                        response_obj = responses[code]
                        if "content" in response_obj:
                            content = response_obj["content"]
                            if "application/json" in content:
                                json_content = content["application/json"]
                                if "schema" not in json_content:
                                    errors.append(f"{method.upper()} {path} response {code} has no schema defined")

        if errors:
            self.fail("Schema validation errors:\n" + "\n".join(f"  - {e}" for e in errors))

    def test_all_serializers_in_components(self):
        """
        Test that all used serializers are properly defined in components/schemas.
        """
        url = reverse("schema")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        components = response.data.get("components", {})
        schemas = components.get("schemas", {})

        # Expected serializers based on our API
        expected_serializers = [
            "Language",
            "PageContent",
            "PageMeta",
            "PageList",
            "Placeholder",
            "PluginDefinition",
        ]

        missing = []
        for serializer_name in expected_serializers:
            if serializer_name not in schemas:
                missing.append(serializer_name)

        if missing:
            available = list(schemas.keys())
            self.fail(f"Missing serializers in schema: {missing}\n" f"Available serializers: {available}")

    def test_all_serializers_have_required_structure(self):
        """
        Test that all serializers in the schema have proper structure.

        Checks:
        - Each schema has 'type' defined
        - Each schema has 'properties' (for object types)
        - Properties have types defined
        """
        url = reverse("schema")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        schemas = response.data.get("components", {}).get("schemas", {})
        errors = []

        for schema_name, schema_def in schemas.items():
            # Check type is defined
            if "type" not in schema_def and "$ref" not in schema_def and "allOf" not in schema_def:
                errors.append(f"Schema '{schema_name}' has no 'type', '$ref', or 'allOf' defined")
                continue

            # For object types, check properties
            if schema_def.get("type") == "object":
                if "properties" not in schema_def:
                    # Some object types might be empty or use additionalProperties
                    if "additionalProperties" not in schema_def:
                        errors.append(
                            f"Schema '{schema_name}' (type: object) has no 'properties' or 'additionalProperties'"
                        )
                    continue

                # Check each property has a type or $ref
                properties = schema_def.get("properties", {})
                for prop_name, prop_def in properties.items():
                    if isinstance(prop_def, dict):
                        if (
                            "type" not in prop_def
                            and "$ref" not in prop_def
                            and "allOf" not in prop_def
                            and "anyOf" not in prop_def
                        ):
                            errors.append(
                                f"Schema '{schema_name}' property '{prop_name}' has no type or reference defined"
                            )

        if errors:
            self.fail("Schema structure errors:\n" + "\n".join(f"  - {e}" for e in errors))

    def test_placeholder_serializer_content_field_in_schema(self):
        """
        Test that the PlaceholderSerializer.content field appears in the OpenAPI schema.

        This is a regression test for the issue where dynamically populated fields
        were not appearing in the schema documentation.
        """
        url = reverse("schema")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Get the schema data
        schema = response.data
        components = schema.get("components", {})
        schemas = components.get("schemas", {})

        # Find the PlaceholderSerializer schema
        placeholder_schema = schemas.get("Placeholder")
        self.assertIsNotNone(
            placeholder_schema,
            "PlaceholderSerializer should be present in the schema components",
        )

        # Check that the content field is defined
        properties = placeholder_schema.get("properties", {})
        self.assertIn(
            "content",
            properties,
            "The 'content' field should be present in PlaceholderSerializer schema",
        )

        # Verify the content field has the correct type
        content_field = properties["content"]
        self.assertEqual(
            content_field.get("type"),
            "array",
            "The 'content' field should be of type 'array'",
        )

        # Verify the array items are objects
        items = content_field.get("items", {})
        self.assertEqual(
            items.get("type"),
            "object",
            "The 'content' field items should be of type 'object'",
        )

        # Verify description is present
        self.assertIn(
            "description",
            content_field,
            "The 'content' field should have a description",
        )

    def test_placeholder_serializer_all_fields_in_schema(self):
        """
        Test that all PlaceholderSerializer fields are present in the schema.
        """
        url = reverse("schema")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        schema = response.data
        schemas = schema.get("components", {}).get("schemas", {})
        placeholder_schema = schemas.get("Placeholder")

        self.assertIsNotNone(placeholder_schema)

        properties = placeholder_schema.get("properties", {})
        expected_fields = ["slot", "label", "language", "content", "details", "html"]

        for field in expected_fields:
            self.assertIn(
                field,
                properties,
                f"Field '{field}' should be present in PlaceholderSerializer schema",
            )

    def test_placeholder_detail_endpoint_in_schema(self):
        """
        Test that the placeholder detail endpoint is documented in the schema.
        """
        url = reverse("schema")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        schema = response.data
        paths = schema.get("paths", {})

        # Check for placeholder detail endpoint pattern
        placeholder_endpoints = [path for path in paths.keys() if "placeholder" in path.lower()]
        self.assertTrue(
            len(placeholder_endpoints) > 0,
            "At least one placeholder endpoint should be documented in the schema",
        )

    def test_preview_parameter_documented(self):
        """
        Test that the 'preview' query parameter is documented for relevant endpoints.
        """
        url = reverse("schema")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        paths = response.data.get("paths", {})

        # Endpoints that should support preview parameter
        preview_endpoints = [path for path in paths.keys() if any(x in path for x in ["/pages/", "/placeholders/"])]

        missing_preview = []
        for path in preview_endpoints:
            path_item = paths[path]
            if "get" in path_item:
                operation = path_item["get"]
                parameters = operation.get("parameters", [])

                # Check if preview parameter is documented
                has_preview = any(
                    param.get("name") == "preview" and param.get("in") == "query" for param in parameters
                )

                if not has_preview:
                    missing_preview.append(path)

        # This is informational - some endpoints might not need preview
        # So we just check that at least some have it
        if preview_endpoints and len(missing_preview) == len(preview_endpoints):
            self.fail(f"No preview parameter found in any of the relevant endpoints: {preview_endpoints}")
