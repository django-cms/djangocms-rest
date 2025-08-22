from typing import Any, Optional

from django.apps import apps
from django.db.models import Field, Model
from django.http import HttpRequest
from django.urls import NoReverseMatch, reverse

from cms.models import CMSPlugin
from cms.plugin_pool import plugin_pool

from rest_framework import serializers

from djangocms_rest.utils import get_absolute_frontend_url


def serialize_fk(
    request: HttpRequest,
    related_model: type[CMSPlugin],
    pk: Any,
    obj: Optional[Model] = None,
) -> dict[str, Any]:
    """
    Serializes a foreign key reference to a related model as a URL or identifier.

    Attempts to serialize the foreign key in the following order:
    1. If the related model has a `get_api_endpoint` method, it uses this to obtain the API endpoint for the object.
    2. If not, it tries to reverse a DRF-style detail URL using the model's name and primary key.
    3. If reversing fails, it falls back to returning a string in the format "<app_label>.<model_name>:<pk>".

    Args:
        related_model (type[CMSPlugin]): The related model class.
        pk (Any): The primary key of the related object.
        obj (Optional[Model], optional): The related model instance, if already available. Defaults to None.

    Returns:
        dict[str, Any]: A dictionary representing the serialized foreign key, typically as a URL or identifier.
    """
    # First choice: Check for get_api_endpoint method
    if hasattr(related_model, "get_api_endpoint"):
        if obj is None:
            obj = related_model.objects.filter(pk=pk).first()
        if obj:
            return get_absolute_frontend_url(request, obj.get_api_endpoint())

    # Second choice: Use DRF naming conventions to build the default API URL for the related model
    model_name = related_model._meta.model_name
    try:
        return get_absolute_frontend_url(
            request, reverse(f"{model_name}-detail", args=(pk,))
        )
    except NoReverseMatch:
        pass

    # Fallback:
    app_name = related_model._meta.app_label
    return f"{app_name}.{model_name}:{pk}"


def serialize_soft_refs(request: HttpRequest, data: Any) -> Any:
    """
    Serialize soft references in a dictionary or list.

    This function recursively traverses the input data structure and serializes
    any soft references (dictionaries with 'model' and 'pk' keys) into a more
    usable format.

    Attention: This function modifies the input data in place.

    Args:
        data (Any): The input data structure, which can be a dict, list, or other types.

    Returns:
        Any: The serialized data structure with soft references replaced.
    """
    if isinstance(data, list):
        return [serialize_soft_refs(request, item) for item in data]
    for key, value in data.items():
        if isinstance(value, dict) and set(value.keys()) == {"model", "pk"}:
            app_name, model_name = value["model"].split(".", 1)
            model_class = apps.get_model(app_name, model_name)
            pk = value["pk"]
            data[key] = serialize_fk(request, model_class, pk)
        elif key == "attrs" and isinstance(value, dict) and value.get("data-cms-href"):
            model, pk = value["data-cms-href"].split(":", 1)
            app_name, model_name = model.split(".", 1)
            model_class = apps.get_model(app_name, model_name)
            value["data-cms-href"] = serialize_fk(request, model_class, pk)
        elif isinstance(value, dict) and "internal_link" in value:
            model, pk = value["internal_link"].split(":", 1)
            app_name, model_name = model.split(".", 1)
            model_class = apps.get_model(app_name, model_name)
            data[key] = serialize_fk(request, model_class, pk)
        elif isinstance(value, dict) and "file_link" in value:
            model_class = apps.get_model("filer", "file")
            data[key] = serialize_fk(request, model_class, value["file_link"])
        elif isinstance(value, (dict, list)):
            data[key] = serialize_soft_refs(request, value)
    return data


base_exclude = {
    "id",
    "placeholder",
    "language",
    "position",
    "creation_date",
    "changed_date",
    "parent",
}
#: Excluded fields for plugin serialization

JSON_FIELDS = tuple(
    field
    for field, value in serializers.ModelSerializer.serializer_field_mapping.items()
    if value is serializers.JSONField
)


class GenericPluginSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = self.context.get("request", None)

    def to_representation(self, instance: CMSPlugin):
        request = getattr(self, "request", None)

        ret = super().to_representation(instance)
        for field in self.Meta.model._meta.get_fields():
            if field.is_relation and not field.many_to_many and not field.one_to_many:
                if field.name in ret and getattr(instance, field.name, None):
                    ret[field.name] = serialize_fk(
                        request,
                        field.related_model,
                        getattr(instance, f"{field.name}_id"),
                        obj=(
                            getattr(instance, field.name)
                            if field.is_cached(instance)
                            else None
                        ),
                    )
            elif isinstance(field, JSON_FIELDS) and ret.get(field.name):
                # If the field is a subclass of JSONField, serialize its value directly
                ret[field.name] = serialize_soft_refs(request, ret[field.name])
        return ret


class PluginDefinitionSerializer(serializers.Serializer):
    """
    Serializer for plugin type definitions.
    """

    plugin_type = serializers.CharField(
        help_text="Unique identifier for the plugin type"
    )
    title = serializers.CharField(help_text="Human readable name of the plugin")
    type = serializers.CharField(help_text="Schema type")
    properties = serializers.DictField(help_text="Property definitions")

    @staticmethod
    def get_field_format(field: Field) -> Optional[str]:
        """
        Get the format for specific field types.

        Args:
            field (Field): Django model field instance

        Returns:
            Optional[str]: JSON Schema format string if applicable, None otherwise
        """
        format_mapping = {
            "URLField": "uri",
            "EmailField": "email",
            "DateField": "date",
            "DateTimeField": "date-time",
            "TimeField": "time",
            "FileField": "uri",
            "ImageField": "uri",
        }
        return format_mapping.get(field.__class__.__name__)

    @staticmethod
    def generate_plugin_definitions() -> dict[str, Any]:
        """
        Generate simple plugin definitions for rendering.
        """
        definitions = {}

        for plugin in plugin_pool.plugins.values():
            # Use plugin's serializer_class or create a simple fallback
            serializer_cls = getattr(plugin, "serializer_class", None)

            if not serializer_cls:

                class DynamicModelSerializer(serializers.ModelSerializer):
                    class Meta:
                        model = plugin.model
                        fields = "__all__"

                serializer_cls = DynamicModelSerializer

            try:
                serializer_instance = serializer_cls()
                properties = {}

                for field_name, field in serializer_instance.fields.items():
                    # Skip internal CMS fields
                    if field_name in base_exclude:
                        continue

                    properties[
                        field_name
                    ] = PluginDefinitionSerializer.map_field_to_schema(
                        field, field_name
                    )

                definitions[plugin.__name__] = {
                    "name": getattr(plugin, "name", plugin.__name__),
                    "title": getattr(plugin, "name", plugin.__name__),
                    "type": "object",
                    "properties": properties,
                }

            except Exception:
                # Skip plugins that fail to process
                continue

        return definitions

    @staticmethod
    def map_field_to_schema(field: serializers.Field, field_name: str = "") -> dict:
        """
        Map DRF field to simple JSON Schema definition for rendering.

        Args:
            field: DRF serializer field instance
            field_name: Name of the field (unused but kept for compatibility)

        Returns:
            dict: Basic JSON Schema definition for the field for TypeScript compatibility
        """

        # Field type mapping for TypeScript compatibility
        field_mapping = {
            "CharField": {"type": "string"},
            "TextField": {"type": "string"},
            "URLField": {"type": "string", "format": "uri"},
            "EmailField": {"type": "string", "format": "email"},
            "IntegerField": {"type": "integer"},
            "FloatField": {"type": "number"},
            "DecimalField": {"type": "number"},
            "BooleanField": {"type": "boolean"},
            "DateField": {"type": "string", "format": "date"},
            "DateTimeField": {"type": "string", "format": "date-time"},
            "TimeField": {"type": "string", "format": "time"},
            "FileField": {"type": "string", "format": "uri"},
            "ImageField": {"type": "string", "format": "uri"},
            "JSONField": {"type": "object"},
            "ForeignKey": {"type": "integer"},
            "PrimaryKeyRelatedField": {"type": "integer"},
            "ListField": {"type": "array"},
            "DictField": {"type": "object"},
            "UUIDField": {"type": "string", "format": "uuid"},
        }

        # Handle special cases first
        if isinstance(field, serializers.ChoiceField):
            schema = {"type": "string", "enum": list(field.choices.keys())}
        elif hasattr(field, "fields"):  # Nested serializer
            schema = {"type": "object"}
            # Extract nested properties
            properties = {}
            for nested_field_name, nested_field in field.fields.items():
                properties[
                    nested_field_name
                ] = PluginDefinitionSerializer.map_field_to_schema(
                    nested_field, nested_field_name
                )
            if properties:
                schema["properties"] = properties
        else:
            # Use mapping or default to string
            schema = field_mapping.get(field.__class__.__name__, {"type": "string"})

        # Description from help_text
        if getattr(field, "help_text", None):
            schema["description"] = str(field.help_text)

        return schema
