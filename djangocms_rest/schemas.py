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
            """Override to use URL name stored in view as operation_id.

            Derives a path prefix from the URL (via _tokenize_path) so that
            the operation_id reflects the mount point chosen by the project
            (e.g. ``cms_menu_retrieve`` when mounted under ``/api/cms/``).
            """
            try:
                url_name = getattr(self.view, "_url_name", None)
                if not url_name and hasattr(self.view, "__class__"):
                    url_name = getattr(self.view.__class__, "_url_name", None)

                if url_name:
                    prefix = []
                    try:
                        tokenized_path = self._tokenize_path()
                        first_name_token = url_name.split("-")[0].replace("-", "_")
                        for token in tokenized_path:
                            normalized = token.replace("-", "_")
                            if normalized == first_name_token:
                                break
                            prefix.append(normalized)
                    except (AttributeError, TypeError):
                        # _tokenize_path requires path/path_prefix attributes
                        # that may be absent outside drf-spectacular's request cycle.
                        pass
                    parts = prefix + [url_name.replace("-", "_"), "retrieve"]
                    return "_".join(parts)

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

    extend_page_detail_schema = extend_schema(
        parameters=[
            OpenApiParameter(
                name="content",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="ID of a specific page content version to retrieve (requires preview)",
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
                description="Search for an exact match of the search term to find pages",
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

    def extend_page_detail_schema(func):
        """No-op when drf-spectacular is not available."""
        return func

    def extend_page_search_schema(func):
        """No-op when drf-spectacular is not available."""
        return func
