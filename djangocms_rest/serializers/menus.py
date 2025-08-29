from rest_framework import serializers


class NavigationNodeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    namespace = serializers.CharField(allow_null=True)
    title = serializers.CharField()
    url = serializers.CharField()
    parent_id = serializers.IntegerField(allow_null=True)
    visible = serializers.BooleanField()
    selected = serializers.BooleanField()
    attr = serializers.DictField(allow_null=True)
    level = serializers.IntegerField()

    def get_children(self, obj):
        # Assuming obj.children is a list of NavigationNode-like objects
        serializer = NavigationNodeSerializer(obj.children or [], many=True)
        return serializer.data


class NavigationNodeListSerializer(serializers.ListSerializer):
    child = NavigationNodeSerializer()
