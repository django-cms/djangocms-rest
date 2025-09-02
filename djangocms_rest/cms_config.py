from functools import cached_property

from django.conf import settings
from django.urls import NoReverseMatch, reverse

from cms.app_base import CMSAppConfig
from cms.cms_menus import CMSMenu
from cms.models import Page, PageContent
from cms.utils.i18n import force_language, get_current_language
from menus import base


try:
    from filer.models import File
except ImportError:
    File = None


def get_page_api_endpoint(page, language=None, fallback=True):
    """Get the API endpoint for a given page in a specific language.
    If the page is a home page, return the root endpoint.
    """
    if not language:
        language = get_current_language()

    with force_language(language):
        try:
            if page.is_home:
                return reverse("page-root", kwargs={"language": language})
            path = page.get_path(language, fallback)
            return (
                reverse("page-detail", kwargs={"language": language, "path": path})
                if path
                else None
            )
        except NoReverseMatch:
            return None


def get_file_api_endpoint(file):
    """For a file reference, return the URL of the file if it is public."""
    if not file:
        return None
    return file.url if file.is_public else None


def patch_get_menu_node_for_page_content(method: callable) -> callable:
    def inner(self, page_content: PageContent, *args, **kwargs):
        node = method(self, page_content, *args, **kwargs)
        node.api_endpoint = get_page_api_endpoint(
            page_content.page,
            page_content.language,
        )
        return node

    return inner


def patch_page_menu(menu: type[CMSMenu]):
    """Patch the CMSMenu to use the REST API endpoint for pages."""
    if hasattr(menu, "get_menu_node_for_page_content"):
        menu.get_menu_node_for_page_content = patch_get_menu_node_for_page_content(
            menu.get_menu_node_for_page_content
        )


class NavigationNodeMixin:
    """Mixin to add API endpoint and selection logic to NavigationNode."""

    def get_api_endpoint(self):
        """Get the API endpoint for the navigation node."""
        return self.api_endpoint

    def is_selected(self, request):
        """Check if the navigation node is selected."""
        return (
            self.api_endpoint == request.api_endpoint
            if hasattr(request, "api_endpoint")
            else super().is_selected(request)
        )


def add_api_endpoint(navigation_node: type[base.NavigationNode]):
    """Add an API endpoint to the CMSNavigationNode."""
    if not issubclass(navigation_node, NavigationNodeMixin):
        navigation_node = type(
            f"{navigation_node.__name__}WithAPI",
            (navigation_node, NavigationNodeMixin),
            {},
        )
    return navigation_node


class RESTToolbarMixin:
    """
    Mixin to add REST rendering capabilities to the CMS toolbar.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    if getattr(
        settings, "REST_JSON_RENDERING", not getattr(settings, "CMS_TEMPLATES", False)
    ):
        try:
            from djangocms_text import settings

            settings.TEXT_INLINE_EDITING = False
        except ImportError:
            pass

        @cached_property
        def content_renderer(self):
            from .plugin_rendering import RESTRenderer

            return RESTRenderer(request=self.request)


class RESTCMSConfig(CMSAppConfig):
    cms_enabled = True
    cms_toolbar_mixin = RESTToolbarMixin

    Page.add_to_class("get_api_endpoint", get_page_api_endpoint)
    File.add_to_class("get_api_endpoint", get_file_api_endpoint) if File else None
    base.NavigationNode = add_api_endpoint(base.NavigationNode)
    patch_page_menu(CMSMenu)
