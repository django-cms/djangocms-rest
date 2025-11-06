from urllib.parse import urlencode

from django.template import Context
from django.urls import reverse

from rest_framework import serializers

from djangocms_rest.serializers.utils.render import render_html
from djangocms_rest.utils import get_absolute_frontend_url

try:
    from drf_spectacular.utils import extend_schema_field

    HAS_SPECTACULAR = True
except ImportError:
    HAS_SPECTACULAR = False

    def extend_schema_field(field_schema):
        def decorator(field):
            return field

        return decorator


class PlaceholderSerializer(serializers.Serializer):
    slot = serializers.CharField()
    label = serializers.CharField()
    language = serializers.CharField()

    # Annotate the content field for OpenAPI schema generation
    @extend_schema_field(
        {
            "type": "array",
            "items": {"type": "object"},
            "description": "List of serialized plugin data for this placeholder",
        }
    )
    class ContentField(serializers.ListSerializer):
        child = serializers.JSONField()

    content = ContentField(allow_empty=True, required=False)
    details = serializers.URLField()
    html = serializers.CharField(default="", required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        self.language = kwargs.pop("language", None)
        self.render_plugins = kwargs.pop("render_plugins", True)
        super().__init__(*args, **kwargs)
        if self.request is None:
            self.request = self.context.get("request")

    def to_representation(self, instance):
        instance.label = instance.get_label()
        instance.language = self.language
        instance.details = self.get_details(instance)
        if instance and self.request and self.language:
            if self.render_plugins:
                from djangocms_rest.plugin_rendering import RESTRenderer

                renderer = RESTRenderer(self.request)
                instance.content = renderer.serialize_placeholder(
                    instance,
                    context=Context({"request": self.request}),
                    language=self.language,
                    use_cache=True,
                )
            if self.request.GET.get("html", False):
                html = render_html(self.request, instance, self.language)
                for key, value in html.items():
                    if not hasattr(instance, key):
                        setattr(instance, key, value)

        return super().to_representation(instance)

    def get_details(self, instance):
        url = get_absolute_frontend_url(
            self.request,
            reverse(
                "placeholder-detail",
                args=[
                    self.language,
                    instance.content_type_id,
                    instance.object_id,
                    instance.slot,
                ],
            ),
        )
        get_params = {key: self.request.GET[key] for key in ("html", "preview") if key in self.request.GET}
        if get_params:
            url += "?" + urlencode(get_params)
        return url
