Caching and performance
=======================

Serializing a placeholder means walking its whole plugin tree, resolving references and
(optionally) rendering HTML. djangocms-rest caches that work so repeat requests are cheap.
This page explains what is cached, when, and how it stays correct.

What gets cached
----------------

The unit of caching is the **serialized placeholder**: the JSON content of one placeholder
in one language for one site. This is the expensive part of a page response, and it is
exactly what the placeholder endpoint (``/placeholders/…``) returns and what single-page
endpoints embed.

The cache reuses django CMS's own placeholder cache machinery — the same keys, versioning
and expiration logic — under a distinct ``:rest`` namespace, so the JSON cache lives
alongside (and never collides with) the HTML placeholder cache. It is stored in whatever
`Django cache backend <https://docs.djangoproject.com/en/stable/topics/cache/>`_ you have
configured: locmem in development, Redis or Memcached in production.

When the cache is used
----------------------

Caching applies only when it is both safe and enabled:

* the placeholder must opt in to caching (``cache_placeholder``);
* django CMS placeholder caching must be enabled in settings;
* the request must **not** be a preview request.

The last point matters: preview reads draft, in-progress content (see
:doc:`preview-and-versioning`), so caching it would risk serving stale drafts to editors.
Preview responses are always generated fresh.

How freshness is maintained
---------------------------

Each cache entry has a version and an expiration. The expiration is the smaller of django
CMS's configured content cache duration and the placeholder's own computed expiration, so
plugins that declare a shorter lifetime are respected. When content changes, the
underlying cache version moves on and stale entries are no longer served — you do not
invalidate the REST cache manually.

Implications for your design
----------------------------

* **Listings stay light by design.** List and tree endpoints return placeholder *links*
  rather than embedded content (see :doc:`content-model`), so a large navigation tree
  never triggers plugin serialization. Fetch placeholder content only for the pages you
  actually render.
* **Deep trees are the expensive case.** ``/pages-tree/`` over a large site builds the
  whole hierarchy in one response; prefer the paginated ``/pages-list/`` when you don't
  need the nesting.
* **A shared cache backend amplifies the win.** With Redis or Memcached, placeholder JSON
  serialized for one visitor is reused for the next — across processes and, for a
  single-instance multi-site deployment, correctly partitioned per site.

.. seealso::

   * :doc:`content-model` — why listings omit content.
   * `django CMS — caching <https://docs.django-cms.org/en/latest/topics/caching.html>`_
