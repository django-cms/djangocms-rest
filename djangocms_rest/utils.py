from cms.models import Page, PageUrl
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import FieldError
from django.db.models import QuerySet
from django.http import Http404
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

    if path.startswith("/"):
        raise ValueError(f"Path should not start with '/': {path}")

    site = get_current_site(request) if request else Site.objects.get(id=1)
    domain = site.domain.rstrip("/")
    protocol = getattr(request, "scheme", "http")

    return f"{protocol}://{domain}/{path}"
