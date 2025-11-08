"""OpenAPI schema generation utilities for djangocms-rest."""

try:
    from drf_spectacular.openapi import AutoSchema
    from drf_spectacular.types import OpenApiTypes
    from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema

    from djangocms_rest.serializers.menus import NavigationNodeSerializer

    class MenuSchema(AutoSchema):
        """
        Custom schema generator that sets operation_id from URL name stored in view.
        This is needed to create distinct operation_ids for each menu endpoint.
        Adds _retrieve to the operation_id to match drf-spectacular's default pattern.
        """

        def get_operation_id(self):
            """Override to use URL name stored in view as operation_id."""
            try:
                url_name = getattr(self.view, "_url_name", None)
                if not url_name and hasattr(self.view, "__class__"):
                    url_name = getattr(self.view.__class__, "_url_name", None)

                if url_name:
                    return url_name.replace("-", "_") + "_retrieve"

                # Fallback to default
                return super().get_operation_id()
            except Exception:
                return super().get_operation_id()

    def create_view_with_url_name(view_class, url_name):
        """Create a view instance with URL name stored for schema generation."""

        class ViewWithUrlName(view_class):
            _url_name = url_name

        return ViewWithUrlName.as_view()

    def menu_schema_class(view_class):
        """Decorator to apply MenuSchema to a view class."""
        view_class.schema = MenuSchema()
        return view_class

    def method_schema_decorator(method):
        """
        Decorator for adding OpenAPI schema to a method.
        Needed to force the schema to use many=True for NavigationNodeSerializer.
        """
        return extend_schema(responses=OpenApiResponse(response=NavigationNodeSerializer(many=True)))(method)

    extend_placeholder_schema = extend_schema(
        parameters=[
            OpenApiParameter(
                name="html",
                type=OpenApiTypes.INT,
                location="query",
                description="Set to 1 to include HTML rendering in response",
                required=False,
                enum=[1],
            ),
            OpenApiParameter(
                name="preview",
                type=OpenApiTypes.BOOL,
                location="query",
                description="Set to true to preview unpublished content (admin access required)",
                required=False,
            ),
        ]
    )

    extend_page_search_schema = extend_schema(
        parameters=[
            OpenApiParameter(
                name="q",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Search for an exact match of the search term to find pages by title, page_title, menu_title, or meta_description",
                required=False,
            ),
        ]
    )

except ImportError:

    def method_schema_decorator(method):
        return method

    def menu_schema_class(view_class):
        return view_class

    def create_view_with_url_name(view_class, url_name):
        """No-op when drf-spectacular is not available."""
        return view_class.as_view()

    def extend_placeholder_schema(func):
        """No-op when drf-spectacular is not available."""
        return func
