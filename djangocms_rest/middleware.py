from typing import Callable

from django.contrib.sites.shortcuts import get_current_site
from django.contrib.sites.models import Site
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotFound,
)


class SiteContextMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """
        Process the request to determine the site context.
        Sets the site object on the request based on the site ID provided in
        the request headers or falls back to the current site.

        Args:
            request: The HTTP request object

        Returns:
            Optional[HttpResponse]: Either an HTTP error response if site identification
                           fails, or None to continue down the middleware chain
        """
        site_id = request.headers.get("X-Site-ID")

        if site_id:
            try:
                site_id = int(site_id)
                # Using _get_site_by_id directly as it leverages Django's internal site caching
                site = Site.objects._get_site_by_id(site_id)
                request.site = site
            except ValueError:
                return HttpResponseBadRequest("Invalid site ID format.")
            except Site.DoesNotExist:
                return HttpResponseNotFound("The requested site could not be found.")

        else:
            request.site = get_current_site(request)
        return self.get_response(request)
