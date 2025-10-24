from typing import Any, Union
from unittest import TestCase


def assert_field_types(
    test_case: TestCase,
    obj: dict[str, Any],
    field: str,
    expected_type: type | tuple[type, ...] | list | dict,
    obj_type: str = "object",
):
    """
    Utility function to check if a field exists and has the correct type in an object.
    Supports nested type checking for lists and dictionaries.

    Args:
        test_case: TestCase instance (self in test methods)
        obj: Dict containing the fields to check
        field: String name of the field to check
        expected_type: Type specification that can be:
            - A type (e.g., str, int)
            - A tuple of types (e.g., (str, None))
            - A list with a single item that is a dict, indicating a list of objects with that structure
            - A dict specifying the structure of a nested object
        obj_type: String describing the type of object being checked (for error messages)
    """
    # Check if the field exists
    test_case.assertIn(field, obj, f"Field {field} is missing in {obj_type}")

    # Get the field value
    field_value = obj[field]

    # Handle a list of structured objects [{}]
    if (
        isinstance(expected_type, list)
        and len(expected_type) == 1
        and isinstance(expected_type[0], dict)
    ):
        # First, verify this is a list
        test_case.assertIsInstance(
            field_value,
            list,
            f"Field {field} should be a list, got {type(field_value)}",
        )

        # Then verify each item in the list
        nested_structure = expected_type[0]
        for i, item in enumerate(field_value):
            for nested_field, nested_type in nested_structure.items():
                assert_field_types(
                    test_case, item, nested_field, nested_type, f"{field}[{i}]"
                )

    # Handle dictionary of a structured object {}
    elif isinstance(expected_type, dict):
        # First, verify this is a dict
        test_case.assertIsInstance(
            field_value,
            dict,
            f"Field {field} should be a dictionary, got {type(field_value)}",
        )

        # Then verify each field in the dictionary
        for nested_field, nested_type in expected_type.items():
            assert_field_types(test_case, field_value, nested_field, nested_type, field)

    # Handle tuple of types (type1, type2)
    elif isinstance(expected_type, tuple):
        test_case.assertTrue(
            isinstance(field_value, expected_type),
            f"Field {field} should be one of types {expected_type}, got {type(field_value)}",
        )

    # Handle basic types (str, int, etc.)
    else:
        test_case.assertIsInstance(
            field_value,
            expected_type,
            f"Field {field} should be {expected_type}, got {type(field_value)}",
        )
