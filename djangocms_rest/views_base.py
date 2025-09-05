from django.contrib.sites.shortcuts import get_current_site
from django.utils.functional import cached_property
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView


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

    @property
    def content_getter(self):
        if "preview" in self.request.GET:
            return "get_admin_content"
        return "get_content_obj"

    def get_permissions(self):
        permissions = super().get_permissions()
        if "preview" in self.request.GET:
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
