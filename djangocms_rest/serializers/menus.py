from rest_framework import serializers

from menus.base import NavigationNode

from djangocms_rest.utils import get_absolute_frontend_url


class NavigationNodeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    namespace = serializers.CharField(allow_null=True)
    title = serializers.CharField()
    url = serializers.URLField(allow_null=True)
    api_endpoint = serializers.URLField(allow_null=True)
    visible = serializers.BooleanField()
    selected = serializers.BooleanField()
    attr = serializers.DictField(allow_null=True)
    level = serializers.IntegerField()
    children = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = self.context.get("request")

    def get_children(self, obj: NavigationNode) -> list[dict]:
        # Assuming obj.children is a list of NavigationNode-like objects
        serializer = NavigationNodeSerializer(
            obj.children or [], many=True, context=self.context
        )
        return serializer.data

    def to_representation(self, obj: NavigationNode) -> dict:
        """Customize the base representation of the NavigationNode."""
        return {
            "id": obj.id,
            "title": obj.title,
            "url": get_absolute_frontend_url(self.request, obj.url),
            "api_endpoint": get_absolute_frontend_url(self.request, obj.api_endpoint),
            "visible": obj.visible,
            "selected": obj.selected
            or obj.attr.get("is_home", False)
            and getattr(self.request, "is_home", False),
            "attr": obj.attr,
            "level": obj.level,
            "children": self.get_children(obj),
        }


class NavigationNodeListSerializer(serializers.ListSerializer):
    child = NavigationNodeSerializer()
