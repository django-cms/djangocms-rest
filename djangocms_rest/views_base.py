from django.contrib.sites.shortcuts import get_current_site
from django.utils.functional import cached_property
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView


class BaseAPIView(APIView):
    """
    This is a base class for all API views. It sets the allowed methods to GET and OPTIONS.
    """

    http_method_names = ("get", "options")

    @cached_property
    def site(self):
        """
        Fetch and cache the current site and make it available to all views.
        """
        return get_current_site(self.request)


class BaseListAPIView(ListAPIView):
    """
    This is a base class for all list API views. It supports default pagination and sets the allowed methods to GET and OPTIONS.
    """

    @cached_property
    def site(self):
        """
        Fetch and cache the current site and make it available to all views.
        """
        return get_current_site(self.request)
