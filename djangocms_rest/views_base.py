from typing import ParamSpec, TypeVar

from django.contrib.sites.shortcuts import get_current_site
from django.utils.functional import cached_property

from cms.toolbar.toolbar import CMSToolbar

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView

P = ParamSpec("P")
T = TypeVar("T")

try:
    from drf_spectacular.types import OpenApiTypes
    from drf_spectacular.utils import OpenApiParameter, extend_schema

    preview_schema = extend_schema(
        parameters=[
            OpenApiParameter(
                name="preview",
                type=OpenApiTypes.BOOL,
                location="query",
                description="Set to true to preview unpublished content (admin access required)",
                required=False,
            )
        ]
    )
except ImportError:  # pragma: no cover

    class OpenApiTypes:
        BOOL = "boolean"

    class OpenApiParameter:  # pragma: no cover
        QUERY = "query"
        PATH = "path"
        HEADER = "header"
        COOKIE = "cookie"

        def __init__(self, *args, **kwargs):
            pass

    def extend_schema(*_args, **_kwargs):  # pragma: no cover
        def _decorator(obj: T) -> T:
            return obj

        return _decorator

    def preview_schema(obj: T) -> T:  # pragma: no cover
        return obj


@preview_schema
class BaseAPIMixin:
    """
    This mixin provides common functionality for all API views.
    """

    http_method_names = ("get", "options")

    @cached_property
    def site(self):
        """
        Fetch and cache the current site and make it available to all views.
        """
        site = getattr(self.request, "site", None)
        return site if site is not None else get_current_site(self.request)

    def _preview_requested(self):
        if not hasattr(self.request, "_preview_mode"):
            # Cache to not re-generate toolbar object for preview requests
            self.request._preview_mode = "preview" in self.request.GET and self.request.GET.get(
                "preview", ""
            ).lower() not in (
                "0",
                "false",
            )
            if self.request._preview_mode:
                if not hasattr(self.request, "toolbar"):  # Create toolbar if not present to mark preview mode
                    self.request.toolbar = CMSToolbar(self.request)
                self.request.toolbar.preview_mode_active = True
        return self.request._preview_mode

    @property
    def content_getter(self):
        if self._preview_requested():
            return "get_admin_content"
        return "get_content_obj"

    def get_permissions(self):
        permissions = super().get_permissions()
        if self._preview_requested():
            # Require admin access for preview as first check
            permissions.insert(0, IsAdminUser())
        return permissions


class BaseAPIView(BaseAPIMixin, APIView):
    """
    This is a base class for all API views. It sets the allowed methods to GET and OPTIONS.
    """

    pass


class BaseListAPIView(BaseAPIMixin, ListAPIView):
    """
    This is a base class for all list API views. It supports default pagination and sets the allowed methods to GET and OPTIONS.
    """

    pass
