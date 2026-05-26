from typing import Any

from djangocms_alias.models import AliasPlugin
from rest_framework import serializers

from djangocms_rest.serializers.plugins import GenericPluginSerializer, base_exclude


class AliasInlineSerializer(GenericPluginSerializer):
    content = serializers.SerializerMethodField()

    class Meta:
        model = AliasPlugin
        exclude = tuple(base_exclude)

    def get_content(self, instance: AliasPlugin) -> list[dict[str, Any]]:
        request = self.request
        language = getattr(instance, "language", None)
        if not request or not language:  # pragma: no cover
            return []

        alias_stack = getattr(request, "_rest_alias_stack", None)
        if alias_stack is None:
            alias_stack = []
            request._rest_alias_stack = alias_stack

        if instance.alias_id in alias_stack:
            return []

        alias_stack.append(instance.alias_id)
        try:
            placeholder = instance.alias.get_placeholder(
                language=language,
                show_draft_content=bool(getattr(request, "_preview_mode", False)),
            )
            if not placeholder:  # pragma: no cover
                return []

            from djangocms_rest.plugin_rendering import RESTRenderer

            renderer = RESTRenderer(request=request)
            return renderer.serialize_plugins(
                placeholder=placeholder,
                language=language,
                context=self.context,
            )
        finally:
            alias_stack.pop()
