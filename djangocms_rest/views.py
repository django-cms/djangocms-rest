from cms.models import Page, PageContent, Placeholder
from cms.utils.conf import get_languages
from cms.utils.page_permissions import user_can_view_page
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.exceptions import NotFound
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response

from djangocms_rest.permissions import (
    CanViewPage,
    CanViewPageContent,
    IsAllowedLanguage,
    IsAllowedPublicLanguage,
)
from djangocms_rest.serializers.languages import LanguageSerializer
from djangocms_rest.serializers.pages import (
    PageContentSerializer,
    PageListSerializer,
    PageMetaSerializer,
    PreviewPageContentSerializer,
)
from djangocms_rest.serializers.placeholders import PlaceholderSerializer
from djangocms_rest.serializers.plugins import (
    PLUGIN_DEFINITIONS,
    PluginDefinitionSerializer,
)
from djangocms_rest.utils import get_object
from djangocms_rest.views_base import BaseAPIView, BaseListAPIView

try:
    from drf_spectacular.types import OpenApiTypes  # noqa: F401
    from drf_spectacular.utils import OpenApiParameter, extend_schema  # noqa: F401

    extend_placeholder_schema = extend_schema(
        parameters=[
            OpenApiParameter(
                name='html',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Set to 1 to include HTML rendering in response',
                required=False,
                enum=[1]
            )
        ]
    )
except ImportError:
    def extend_placeholder_schema(func):
        return func



class LanguageListView(BaseAPIView):
    serializer_class = LanguageSerializer

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
        language = self.kwargs['language']
        site = self.site
        qs = Page.objects.filter(node__site=site)

        #Filter out pages which require login
        if self.request.user.is_anonymous:
            qs = qs.filter(login_required=False)

        try:
            pages = [
                page.get_content_obj(language, fallback=True)
                for page in qs
                if user_can_view_page(self.request.user, page) and page.get_content_obj(language, fallback=True)
            ]

            return pages
        except PageContent.DoesNotExist:
            raise NotFound()

class PageTreeListView(BaseAPIView):
    permission_classes = [IsAllowedPublicLanguage]
    serializer_class = PageMetaSerializer

    def get(self, request, language):
        """List of all pages on this site for a given language."""
        site = self.site
        qs = Page.objects.filter(node__site=site)

        #Filter out pages which require login
        if self.request.user.is_anonymous:
            qs = qs.filter(login_required=False)

        try:
            pages = [
                page.get_content_obj(language, fallback=True)
                for page in qs
                if user_can_view_page(self.request.user, page) and page.get_content_obj(language, fallback=True)
            ]

            if not any(pages):
                raise PageContent.DoesNotExist()
        except PageContent.DoesNotExist:
            raise NotFound()

        serializer = self.serializer_class(pages, many=True, read_only=True)
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
            page_content = page.get_content_obj(language, fallback=True)
            if page_content is None:
                raise PageContent.DoesNotExist()
            serializer = self.serializer_class(page_content, read_only=True)
            return Response(serializer.data)
        except PageContent.DoesNotExist:
            raise NotFound()


class PlaceholderDetailView(BaseAPIView):
    permission_classes = [IsAllowedPublicLanguage, CanViewPageContent]
    serializer_class = PlaceholderSerializer

    @extend_placeholder_schema

    def get(self, request: Request, language: str, content_type_id: int, object_id: int, slot: str) -> Response:
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

        source = placeholder.content_type.model_class().objects.filter(pk=placeholder.object_id).first()
        if source is None:
            raise NotFound()

        self.check_object_permissions(request, source)

        serializer = self.serializer_class(
            instance=placeholder,
            request=request,
            language=language,
            read_only=True
        )
        return Response(serializer.data)

#NOTE: This is working, but might need refactoring
class PreviewPlaceholderDetailView(BaseAPIView):
    serializer_class = PlaceholderSerializer
    permission_classes = [IsAdminUser, CanViewPage]

    @extend_placeholder_schema

    def get(self, request: Request, language: str, content_type_id: int, object_id: int, slot: str) -> Response:
        """Placeholder contain the dynamic content. This view retrieves the content as a
        structured nested object.
        """
        try:
            placeholder = Placeholder.objects.get(
                content_type_id=content_type_id, object_id=object_id, slot=slot
            )
        except Placeholder.DoesNotExist:
            raise NotFound()

        serializer = self.serializer_class(
            instance=placeholder,
            request=request,
            language=language,
            read_only=True
        )
        return Response(serializer.data)


class PluginDefinitionView(BaseAPIView):
    """
    API view for retrieving plugin definitions
    """
    serializer_class = PluginDefinitionSerializer

    def get(self, request: Request) -> Response:
        """Get all plugin definitions"""
        definitions = [
            {
                "plugin_type": plugin_type,
                "title": definition["title"],
                "type": definition["type"],
                "properties": definition["properties"]
            }
            for plugin_type, definition in PLUGIN_DEFINITIONS.items()
        ]
        return Response(definitions)

#NOTE: This is working, but might need refactoring
class PreviewPageView(BaseAPIView):
    """View for previewing unpublished page content"""
    permission_classes = [IsAdminUser, CanViewPage]
    serializer_class = PreviewPageContentSerializer

    def get(self, request: Request, language: str, path: str = "") -> Response:
        """Retrieve a draft/preview version of a page instance."""
        site = self.site
        page = get_object(site, path)
        self.check_object_permissions(request, page)

        try:
            # Get all draft versions for this page and language
            page_content = PageContent.admin_manager.filter(
                page=page,
                language=language
            ).order_by('-creation_date').first()

            if page_content is None:
                raise PageContent.DoesNotExist()
        except PageContent.DoesNotExist:
            raise NotFound()

        serializer = self.serializer_class(page_content, read_only=True)
        return Response(serializer.data)

#NOTE: This is working, but might need refactoring
class PreviewPageTreeListView(BaseAPIView):
    permission_classes = [IsAdminUser, IsAllowedLanguage]
    serializer_class = PageMetaSerializer

    def get(self, request, language):
        """List of all draft/preview pages on this site for a given language."""
        site = self.site
        qs = Page.objects.filter(node__site=site)

        try:
            # Create a generator similar to PageTreeListView but using admin_manager
            pages = [
                PageContent.admin_manager.filter(
                    page=page,
                    language=language
                ).order_by('-creation_date').first() or page.get_content_obj(language, fallback=True)
                for page in qs
                if user_can_view_page(self.request.user, page)
            ]

            if not any(pages):
                raise PageContent.DoesNotExist()
        except PageContent.DoesNotExist:
            raise NotFound()

        serializer = self.serializer_class(pages, many=True, read_only=True)
        return Response(serializer.data)

class PreviewPageListView(BaseListAPIView):
    permission_classes = [IsAdminUser, IsAllowedLanguage]
    serializer_class = PageListSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        """Get queryset of draft/preview pages for the given language."""
        language = self.kwargs['language']
        site = self.site
        qs = Page.objects.filter(node__site=site)

        try:
            pages = [
                PageContent.admin_manager.filter(
                    page=page,
                    language=language
                ).order_by('-creation_date').first() or page.get_content_obj(language, fallback=True)
                for page in qs
                if user_can_view_page(self.request.user, page)
            ]

            if not any(pages):
                raise PageContent.DoesNotExist()
        except PageContent.DoesNotExist:
            raise NotFound()

        return pages
