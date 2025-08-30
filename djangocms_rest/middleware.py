from typing import Optional

from cms.utils import get_current_site
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.http import HttpRequest, HttpResponse, HttpResponseServerError
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


def get_site_cache_key(site_id) -> str:
    """
    Generate a cache key for a site ID.
    Used by the MultiSiteMiddleware and signal handlers to invalidate the cache.
    """
    return f"site:{site_id}"


class SiteContextMiddleware(MiddlewareMixin):
    @staticmethod
    def process_request(request: HttpRequest) -> Optional[HttpResponse]:
        """
        Process the request to determine the site context.
        Cache the site object based on the site ID provided in the request headers.

        Args:
            request: The HTTP request object

        Returns:
            An HTTP response if an error occurs, None otherwise
        """
        site_id = request.headers.get("X-Site-ID")

        if site_id:
            try:
                site_id = int(site_id)
                cache_key = get_site_cache_key(site_id)
                site = cache.get(cache_key)

                if site is None:
                    site = Site.objects.get(pk=site_id)
                    cache.set(cache_key, site, settings.CONTENT_CACHE_DURATION)

                request.site = site
            except (Site.DoesNotExist, ValueError):
                return HttpResponseServerError("Oops! Something went wrong.")
        else:
            request.site = get_current_site()
        return None


def clear_site_cache(sender, instance, **kwargs):
    """Clear the cache for a specific site when it's modified or deleted."""
    cache_key = get_site_cache_key(instance.pk)
    cache.delete(cache_key)


post_save.connect(clear_site_cache, sender=Site)
post_delete.connect(clear_site_cache, sender=Site)
