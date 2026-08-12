"""Path-mirrored mounting of apphook REST urls.

django CMS apphooks mount an HTML urlconf at the page path chosen by the editor
(see ``cms.appresolver.get_app_patterns``). This module does the same for the
headless API: any apphook that *duck-types* a ``get_rest_urls()`` method gets its
REST urls mounted under ``/<lang>/<localized-page-path>/`` below the API root.

Unlike the core resolver, the headless API carries the language as an explicit
``<slug:language>`` path segment rather than via ``i18n_patterns``. We mount the
apphook urls below a language-capturing prefix and the localized
``PageUrl.path``, so consumer views receive ``language`` as a regular URL kwarg,
exactly like every other endpoint in the API, and the request locale is
irrelevant.
"""

import re

from django.contrib.sites.models import Site
from django.core.exceptions import ImproperlyConfigured
from django.db.utils import OperationalError, ProgrammingError

from cms.apphook_pool import apphook_pool
from cms.appresolver import get_app_urls, recurse_patterns

#: Regex for the ``<slug:language>`` path converter used across the API.
LANGUAGE_PREFIX = r"(?P<language>[-\w]+)/"


def _rest_apphook(application_urls):
    """Return the apphook for ``application_urls`` iff it offers REST urls."""
    if not application_urls:
        return None
    app = apphook_pool.get_apphook(application_urls)
    if app and hasattr(app, "get_rest_urls"):
        return app
    return None


def _get_rest_app_patterns(site):
    from cms.models import PageUrl

    page_urls = PageUrl.objects.get_for_site(site) if site else PageUrl.objects.all()
    page_urls = (
        page_urls.exclude(page__application_urls=None)
        .exclude(page__application_urls="")
        .order_by("-page__path")
        .select_related("page")
    )

    patterns = []
    seen = set()
    for page_url in page_urls:
        app = _rest_apphook(page_url.page.application_urls)
        if app is None:
            continue

        # One mount per localized path; language is captured, not bound.
        key = (page_url.path, page_url.page.application_urls)
        if key in seen:
            continue
        seen.add(key)

        # ``<slug:language>/<localized-page-path>/`` -- path-mirrored mount with
        # the language captured explicitly, as everywhere else in the API.
        path = page_url.path
        prefix = f"{LANGUAGE_PREFIX}{re.escape(path)}/" if path else LANGUAGE_PREFIX

        url_lists = app.get_rest_urls(page_url.page, page_url.language)
        for pattern_list in get_app_urls(url_lists):
            patterns += recurse_patterns(prefix, pattern_list, page_url.page_id)
    return patterns


def get_rest_app_patterns():
    """All apphook REST patterns for the current site, path-mirrored.

    Called at urlconf build time in ``djangocms_rest.urls`` so the patterns are
    rebuilt on the same urlconf reload django CMS already triggers when an
    apphook page changes.
    """
    try:
        try:
            return _get_rest_app_patterns(Site.objects.get_current())
        except ImproperlyConfigured:
            # No SITE_ID configured -- fall back to site-independent mode.
            return _get_rest_app_patterns(None)
    except (OperationalError, ProgrammingError):
        # DB not ready (e.g. during migrations).
        return []
