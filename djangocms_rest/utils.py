from django.contrib.sites.models import Site
from django.core.exceptions import FieldError
from django.db.models import QuerySet
from django.http import Http404

from cms.models import Page, PageUrl

from rest_framework.request import Request


def get_site_filtered_queryset(site: Site) -> QuerySet:
    """
    Returns a queryset filtered by the given site.
    This is useful for models that have a foreign key to Site.
    """
    try:
        return Page.objects.filter(site=site)
    except FieldError:
        # Can be removed once django CMS 4.1 is no longer supported
        return Page.objects.filter(node__site=site)


def get_object(site: Site, path: str) -> Page:
    page_urls = (
        PageUrl.objects.get_for_site(site).filter(path=path).select_related("page")
    )
    page_urls = list(page_urls)
    try:
        page = page_urls[0].page
    except IndexError:
        raise Http404
    else:
        page.urls_cache = {url.language: url for url in page_urls}
    return page


def get_absolute_frontend_url(request: Request, path: str) -> str:
    """
    Creates an absolute URL for a given relative path using the current site's domain and protocol.

    Args:
        request: The HTTP request object
        path: The relative path to the page

    Returns:
        An absolute URL formatted as a string.
    """
    if path is None:
        return None
    protocol = getattr(request, "scheme", "http")
    domain = getattr(
        request, "get_host", lambda: Site.objects.get_current(request).domain
    )()
    if not path.startswith("/"):
        path = f"/{path}"
    return f"{protocol}://{domain}{path}"
