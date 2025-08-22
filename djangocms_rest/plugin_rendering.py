import json
from typing import Any, Iterable, Optional, TypeVar

from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import models
from django.utils.html import escape, mark_safe

from cms.models import Placeholder
from cms.plugin_rendering import ContentRenderer
from cms.utils.plugins import get_plugins

from djangocms_rest.serializers.placeholders import PlaceholderSerializer
from djangocms_rest.serializers.plugins import GenericPluginSerializer, base_exclude
from djangocms_rest.serializers.utils.cache import (
    get_placeholder_rest_cache,
    set_placeholder_rest_cache,
)


ModelType = TypeVar("ModelType", bound=models.Model)


def get_auto_model_serializer(model_class: type[ModelType]) -> type:
    """
    Build (once) a generic ModelSerializer subclass that excludes
    common CMS bookkeeping fields.
    """

    opts = model_class._meta
    real_fields = {f.name for f in opts.get_fields()}
    exclude = tuple(base_exclude & real_fields)

    meta_class = type(
        "Meta",
        (),
        {
            "model": model_class,
            "exclude": exclude,
        },
    )
    return type(
        f"{model_class.__name__}AutoSerializer",
        (GenericPluginSerializer,),
        {
            "Meta": meta_class,
        },
    )


def serialize_cms_plugin(
    instance: Optional[Any], context: dict[str, Any]
) -> Optional[dict[str, Any]]:
    if not instance or not hasattr(instance, "get_plugin_instance"):
        return None
    plugin_instance, plugin = instance.get_plugin_instance()

    model_cls = plugin_instance.__class__
    serializer_cls = getattr(plugin, "serializer_class", None)
    serializer_cls = serializer_cls or get_auto_model_serializer(model_cls)
    plugin.__class__.serializer_class = serializer_cls

    return serializer_cls(plugin_instance, context=context).data


# Template for a collapsable key-value pair
DETAILS_TEMPLATE = (
    '<details open><summary><span class="key">"{key}"</span>: {open}</summary>'
    '<div class="indent">{value}</div></details>{close}'
)

# Template for a collapsable object/list
OBJ_TEMPLATE = (
    "<details open><summary>{open}</summary>"
    '<div class="indent">{value}</div></details>{close}'
)

# Tempalte for a non-collasable object/list
FIXED_TEMPLATE = '{open}<div class="indent">{value}</div>{close}'

# Tempalte for a single line key-value pair
SIMPLE_TEMPLATE = '<span class="key">"{key}"</span>: {value}'


def escapestr(s: str) -> str:
    """
    Escape a string for safe HTML rendering.
    """
    return escape(json.dumps(s)[1:-1])  # Remove quotes added by json.dumps


def is_valid_url(url):
    validator = URLValidator()
    try:
        validator(url)
        return True
    except ValidationError:
        return False


def highlight_data(json_data: Any, drop_frame: bool = False) -> str:
    """
    Highlight single JSON data element.
    """
    if isinstance(json_data, str):
        classes = "str"
        if len(json_data) > 60:
            classes = "str ellipsis"

        if is_valid_url(json_data):
            return f'<span class="{ classes }">"<a href="{ json_data }">{escapestr(json_data)}</a>"</span>'
        return f'<span class="{ classes }">"{escapestr(json_data)}"</span>'
    if isinstance(json_data, bool):
        return f'<span class="bool">{str(json_data).lower()}</span>'
    if isinstance(json_data, (int, float)):
        return f'<span class="num">{json_data}</span>'
    if json_data is None:
        return '<span class="null">null</span>'
    if isinstance(json_data, dict):
        if drop_frame:
            return highlight_json(json_data)["value"] if json_data else "{}"
        return OBJ_TEMPLATE.format(**highlight_json(json_data)) if json_data else "{}"
    if isinstance(json_data, list):
        if drop_frame:
            return highlight_list(json_data)["value"] if json_data else "[]"
        return OBJ_TEMPLATE.format(**highlight_list(json_data)) if json_data else "[]"

    return f'<span class="obj">{json_data}</span>'


def highlight_list(json_data: list) -> dict[str, str]:
    """
    Transforms a list of JSON data items into a dictionary containing HTML-formatted string representations.
    Args:
        json_data (list): A list of JSON-compatible data items to be highlighted.
    Returns:
        dict[str, str]: A dictionary with keys 'open', 'close', and 'value', where 'value' is a string of highlighted items separated by ',<br>'.
    """

    items = [highlight_data(item) for item in json_data]
    return {
        "open": "[",
        "close": "]",
        "value": ",<br>".join(items),
    }


def highlight_json(
    json_data: dict[str, Any],
    children: Iterable | None = None,
    marker: str = "",
    field: str = "children",
) -> dict[str, str]:
    """
    Highlights and formats a JSON-like dictionary for display, optionally including child elements.

    Args:
        json_data (dict[str, Any]): The JSON data to be highlighted and formatted.
        children (Iterable | None, optional): An iterable of child elements to include under the specified field. Defaults to None.
        marker (str, optional): A string marker to append after the children. Defaults to "".
        field (str, optional): The key under which children are added. Defaults to "children".

    Returns:
        dict[str, str]: A dictionary containing the formatted representation with keys 'open', 'close', and 'value'.
    """
    has_children = children is not None
    if field in json_data:
        del json_data[field]

    items = [
        DETAILS_TEMPLATE.format(
            key=escape(key),
            value=highlight_data(value, drop_frame=True),
            open="{" if isinstance(value, dict) else "[",
            close="}" if isinstance(value, dict) else "]",
        )
        if isinstance(value, (dict, list)) and value
        else SIMPLE_TEMPLATE.format(
            key=escape(key),
            value=highlight_data(value),
        )
        for key, value in json_data.items()
    ]
    if has_children:
        items.append(
            DETAILS_TEMPLATE.format(
                key=escape(field),
                value=",".join(children) + marker,
                open="[",
                close="]",
            )
        )
    return {
        "open": "{",
        "close": "}",
        "value": ",<br>".join(items),
    }


class RESTRenderer(ContentRenderer):
    """
    A custom renderer that uses the serialize_cms_plugin function to render
    CMS plugins in a RESTful way.
    """

    placeholder_edit_template = "{content}{plugin_js}{placeholder_js}"

    def render_plugin(
        self, instance, context, placeholder=None, editable: bool = False
    ):
        """
        Render a CMS plugin instance using the serialize_cms_plugin function.
        """
        data = serialize_cms_plugin(instance, context) or {}
        children = [
            self.render_plugin(
                child, context, placeholder=placeholder, editable=editable
            )
            for child in getattr(instance, "child_plugin_instances", [])
        ] or None
        content = OBJ_TEMPLATE.format(**highlight_json(data, children=children))

        if editable:
            content = self.plugin_edit_template.format(
                pk=instance.pk,
                placeholder=instance.placeholder_id,
                content=content,
                position=instance.position,
            )
            placeholder_cache = self._rendered_plugins_by_placeholder.setdefault(
                placeholder.pk, {}
            )
            placeholder_cache.setdefault("plugins", []).append(instance)
        return mark_safe(content)

    def render_plugins(
        self, placeholder, language, context, editable=False, template=None
    ):
        yield "<div class='rest-placeholder' data-placeholder='{placeholder}' data-language='{language}'>".format(
            placeholder=placeholder.slot,
            language=language,
        )
        placeholder_data = PlaceholderSerializer(
            instance=placeholder,
            language=language,
            request=context["request"],
            render_plugins=False,
        ).data

        yield FIXED_TEMPLATE.format(
            placeholder_id=placeholder.pk,
            **highlight_json(
                placeholder_data,
                children=self.get_plugins_and_placeholder_lot(
                    placeholder, language, context, editable=editable, template=template
                ),
                marker=f'<div class="cms-placeholder cms-placeholder-{placeholder.pk}"></div>',
                field="content",
            ),
        )
        yield "</div>"

    def get_plugins_and_placeholder_lot(
        self, placeholder, language, context, editable=False, template=None
    ) -> Iterable[str]:
        yield from super().render_plugins(
            placeholder, language, context, editable=editable, template=template
        )

    def serialize_placeholder(self, placeholder, context, language, use_cache=True):
        context.update({"request": self.request})
        if use_cache and placeholder.cache_placeholder:
            use_cache = self.placeholder_cache_is_enabled()
        else:
            use_cache = False

        if use_cache:
            cached_value = get_placeholder_rest_cache(
                placeholder,
                lang=language,
                site_id=get_current_site(self.request).pk,
                request=self.request,
            )
        else:
            cached_value = None

        if cached_value is not None:
            # User has opted to use the cache
            # and there is something in the cache
            return cached_value["content"]

        plugin_content = self.serialize_plugins(
            placeholder,
            language=language,
            context=context,
        )

        if use_cache:
            set_placeholder_rest_cache(
                placeholder,
                lang=language,
                site_id=get_current_site(self.request).pk,
                content=plugin_content,
                request=self.request,
            )

        if placeholder.pk not in self._rendered_placeholders:
            # First time this placeholder is rendered
            self._rendered_placeholders[placeholder.pk] = plugin_content

        return plugin_content

    def serialize_plugins(
        self, placeholder: Placeholder, language: str, context: dict
    ) -> list:
        plugins = get_plugins(
            self.request,
            placeholder=placeholder,
            lang=language,
            template=None,
        )

        def serialize_children(child_plugins):
            children_list = []
            for child_plugin in child_plugins:
                child_content = serialize_cms_plugin(child_plugin, context)
                if getattr(child_plugin, "child_plugin_instances", None):
                    child_content["children"] = serialize_children(
                        child_plugin.child_plugin_instances
                    )
                if child_content:
                    children_list.append(child_content)
            return children_list

        results = []
        for plugin in plugins:
            plugin_content = serialize_cms_plugin(plugin, context)
            if getattr(plugin, "child_plugin_instances", None):
                plugin_content["children"] = serialize_children(
                    plugin.child_plugin_instances
                )
            if plugin_content:
                results.append(plugin_content)
        return results

