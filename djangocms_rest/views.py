from __future__ import annotations

from typing import Any
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.functional import lazy

from cms.models import Page, PageContent, Placeholder
from cms.utils.conf import get_languages
from cms.utils.page_permissions import user_can_view_page
from menus.templatetags.menu_tags import ShowBreadcrumb, ShowMenu, ShowSubMenu


from rest_framework.exceptions import NotFound
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.request import Request
from rest_framework.response import Response

from djangocms_rest.permissions import CanViewPage, IsAllowedPublicLanguage
from djangocms_rest.serializers.languages import LanguageSerializer
from djangocms_rest.serializers.menus import NavigationNodeSerializer
from djangocms_rest.serializers.pages import (
    PageContentSerializer,
    PageListSerializer,
    PageMetaSerializer,
)
from djangocms_rest.serializers.placeholders import PlaceholderSerializer
from djangocms_rest.serializers.plugins import PluginDefinitionSerializer
from djangocms_rest.utils import (
    get_object,
    get_site_filtered_queryset,
)
from djangocms_rest.views_base import BaseAPIView, BaseListAPIView


try:
    from drf_spectacular.types import OpenApiTypes  # noqa: F401
    from drf_spectacular.utils import OpenApiParameter, extend_schema  # noqa: F401

    extend_placeholder_schema = extend_schema(
        parameters=[
            OpenApiParameter(
                name="html",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Set to 1 to include HTML rendering in response",
                required=False,
                enum=[1],
            )
        ]
    )
except ImportError:

    def extend_placeholder_schema(func):
        return func


# Generate the plugin definitions once at module load time
# This avoids the need to import the plugin definitions in every view
# and keeps the code cleaner.
# Attn: Dynamic changes to the plugin pool will not be reflected in the
# plugin definitions.
# If you need to update the plugin definitions, you need reassign the variable.
PLUGIN_DEFINITIONS = lazy(
    PluginDefinitionSerializer.generate_plugin_definitions, dict
)()


class LanguageListView(BaseAPIView):
    serializer_class = LanguageSerializer
    queryset = Page.objects.none()  # Dummy queryset to satisfy DRF

    def get(self, request: Request | None) -> Response:
        """List of languages available for the site."""
        languages = get_languages().get(get_current_site(request).id, None)
        if languages is None:
            raise NotFound()

        serializer = self.serializer_class(languages, many=True, read_only=True)
        return Response(serializer.data)


class PageListView(BaseListAPIView):
    permission_classes = [IsAllowedPublicLanguage]
    serializer_class = PageListSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        """Get queryset of pages for the given language."""
        language = self.kwargs["language"]
        qs = get_site_filtered_queryset(self.site)

        # Filter out pages which require login
        if self.request.user.is_anonymous:
            qs = qs.filter(login_required=False)

        try:
            pages = [
                getattr(page, self.content_getter)(language, fallback=True)
                for page in qs
                if user_can_view_page(self.request.user, page)
                and getattr(page, self.content_getter)(language, fallback=True)
            ]

            return pages
        except PageContent.DoesNotExist:
            raise NotFound()


class PageTreeListView(BaseAPIView):
    permission_classes = [IsAllowedPublicLanguage]
    serializer_class = PageMetaSerializer

    def get(self, request, language):
        """List of all pages on this site for a given language."""
        qs = get_site_filtered_queryset(self.site)

        # Filter out pages which require login
        if self.request.user.is_anonymous:
            qs = qs.filter(login_required=False)

        try:
            pages = [
                getattr(page, self.content_getter)(language, fallback=True)
                for page in qs
                if user_can_view_page(self.request.user, page)
                and getattr(page, self.content_getter)(language, fallback=True)
            ]

            if not any(pages):
                raise PageContent.DoesNotExist()
        except PageContent.DoesNotExist:
            raise NotFound()

        serializer = self.serializer_class(
            pages, many=True, read_only=True, context={"request": request}
        )
        return Response(serializer.data)


class PageDetailView(BaseAPIView):
    permission_classes = [IsAllowedPublicLanguage, CanViewPage]
    serializer_class = PageContentSerializer

    def get(self, request: Request, language: str, path: str = "") -> Response:
        """Retrieve a page instance. The page instance includes the placeholders and
        their links to retrieve dynamic content."""
        site = self.site
        page = get_object(site, path)
        self.check_object_permissions(request, page)

        try:
            page_content = getattr(page, self.content_getter)(language, fallback=True)
            if page_content is None:
                raise PageContent.DoesNotExist()
            serializer = self.serializer_class(
                page_content, read_only=True, context={"request": request}
            )
            return Response(serializer.data)
        except PageContent.DoesNotExist:
            raise NotFound()


class PlaceholderDetailView(BaseAPIView):
    permission_classes = [IsAllowedPublicLanguage]
    serializer_class = PlaceholderSerializer

    @extend_placeholder_schema
    def get(
        self,
        request: Request,
        language: str,
        content_type_id: int,
        object_id: int,
        slot: str,
    ) -> Response:
        """Placeholder contain the dynamic content. This view retrieves the content as a
        structured nested object.

        Attributes:
        - "slot": The slot name of the placeholder.
        - "content": The content of the placeholder as a nested JSON tree
        - "language": The language of the content
        - "label": The verbose label of the placeholder

        Optional (if the get parameter `?html=1` is added to the API url):
        - "html": The content rendered as html. Sekizai blocks such as "js" or "css" will be added
          as separate attributes"""
        try:
            placeholder = Placeholder.objects.get(
                content_type_id=content_type_id, object_id=object_id, slot=slot
            )
        except Placeholder.DoesNotExist:
            raise NotFound()

        source_model = placeholder.content_type.model_class()
        source = (
            getattr(source_model, self.content_getter, source_model.objects)
            .filter(pk=placeholder.object_id)
            .first()
        )

        if source is None:
            raise NotFound()
        else:
            # TODO: Here should be a check for the source model's visibility
            # For now, we only check pages
            if isinstance(source, PageContent):
                # If the object is a PageContent, check the page view permission
                if not user_can_view_page(request.user, source.page):
                    raise NotFound()

        self.check_object_permissions(request, placeholder)

        serializer = self.serializer_class(
            instance=placeholder, request=request, language=language, read_only=True
        )
        return Response(serializer.data)


class PluginDefinitionView(BaseAPIView):
    """
    API view for retrieving plugin definitions
    """

    serializer_class = PluginDefinitionSerializer
    queryset = Page.objects.none()  # Dummy queryset to satisfy DRF

    def get(self, request: Request) -> Response:
        """Get all plugin definitions"""
        definitions = [
            {
                "plugin_type": plugin_type,
                "title": definition["title"],
                "type": definition["type"],
                "properties": definition["properties"],
            }
            for plugin_type, definition in PLUGIN_DEFINITIONS.items()
        ]
        return Response(definitions)


class MenuView(BaseAPIView):
    permission_classes = [IsAllowedPublicLanguage]
    serializer_class = NavigationNodeSerializer

    tag = ShowMenu
    return_key = "children"

    def get(
        self,
        request: Request,
        language: str,
        path: str = "",  # for menu-root endpoint
        **kwargs: dict[str, Any],
    ) -> Response:
        """Get the menu structure for a specific language and path."""
        self.populate_defaults(kwargs)
        menu = self.get_menu_structure(request, language, path, **kwargs)
        serializer = self.serializer_class(
            menu, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def populate_defaults(self, kwargs: dict[str, Any]) -> None:
        """Set default values for menu view parameters."""
        kwargs.setdefault("from_level", 0)
        kwargs.setdefault("to_level", 100)
        kwargs.setdefault("extra_inactive", 0)
        kwargs.setdefault("extra_active", 1000)
        kwargs.setdefault("root_id", None)
        kwargs.setdefault("namespace", None)
        kwargs.setdefault("next_page", None)

    def get_menu_structure(
        self,
        request: Request,
        language: str,
        path: str,
        **kwargs: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """Get the menu structure for a specific language and path."""
        # Implement the logic to retrieve the menu structure

        # Create tag instance without calling __init__
        tag_instance = self.tag.__new__(self.tag)

        # Initialize minimal necessary attributes
        tag_instance.kwargs = {}
        tag_instance.blocks = {}

        if path == "":
            api_endpoint = reverse("page-root", kwargs={"language": language})
        else:
            api_endpoint = reverse(
                "page-detail", kwargs={"language": language, "path": path}
            )

        request.api_endpoint = api_endpoint
        request.LANGUAGE_CODE = language
        request.current_page = get_object(self.site, path)
        self.check_object_permissions(request, request.current_page)
        context = {"request": request}

        context = tag_instance.get_context(
            context=context,
            **kwargs,
            template=None,
        )
        return context.get(self.return_key, [])


class SubMenuView(MenuView):
    tag = ShowSubMenu

    def populate_defaults(self, kwargs: dict[str, Any]) -> None:
        kwargs.setdefault("levels", 100)
        kwargs.setdefault("root_level", None)
        kwargs.setdefault("nephews", 100)


class BreadcrumbView(MenuView):
    tag = ShowBreadcrumb
    return_key = "ancestors"

    def populate_defaults(self, kwargs: dict[str, Any]) -> None:
        kwargs.setdefault("start_level", 0)
        kwargs.setdefault("only_visible", True)
