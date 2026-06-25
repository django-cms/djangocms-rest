Conventions
===========

These rules apply across the API. Individual endpoint pages assume them rather than
repeating them in full.

The API is **read-only**: every endpoint responds to ``GET`` (and ``OPTIONS``). There are
no write methods.

Language prefix
---------------

All content endpoints are prefixed with a language code, e.g. ``/api/en/pages/``. The
prefix selects the translation to return. Requesting a language that is not configured —
or not public, for anonymous users — returns ``404``. The ``/api/languages/``,
``/api/plugins/`` and ``/api/healthcheck/`` endpoints are **not** language-prefixed.

The ``preview`` parameter
-------------------------

Add ``preview`` to a page, page-list, page-tree, placeholder or menu request to read
**draft** content instead of published content. Any value other than ``0`` or ``false``
enables it (``?preview``, ``?preview=true`` and ``?preview=1`` are equivalent).

Preview requires an authenticated admin (staff) user; per-page permissions still apply.
See :doc:`../explanation/preview-and-versioning` and
:doc:`../how-to/access-preview-content`.

The ``html`` parameter
----------------------

On the placeholder endpoint (``/placeholders/…``), ``?html=1`` adds an ``html`` field containing the
placeholder rendered with your django CMS plugin templates. Sekizai blocks (such as ``js``
and ``css``) are returned as separate fields. Without it, ``html`` is an empty string.

The ``X-Site-ID`` header
------------------------

In a single-instance multi-site deployment, send an ``X-Site-ID`` request header to choose
which site to serve. A missing header falls back to the current site; a non-numeric value
returns ``400``; an unknown site returns ``404``. Requires ``SiteContextMiddleware`` — see
:doc:`../how-to/serve-multiple-sites`.

Pagination
----------

List-style endpoints (``/pages-list/`` and ``/page_search/``) use limit/offset pagination
and wrap results in an envelope:

.. code-block:: json

    {
      "count": 25,
      "next": "http://localhost:8080/api/en/pages-list/?limit=10&offset=10",
      "previous": null,
      "results": []
    }

Control it with ``limit`` (page size) and ``offset`` (items to skip).

URLs in responses
-----------------

URLs are absolute, built from the request's scheme and host. Two kinds appear:

* ``absolute_url`` — the page's address for the end user (frontend/site URL);
* ``details`` / ``api_endpoint`` — where to fetch that object's data from the API.

Authentication
--------------

The public API needs no authentication. Preview uses Django **session authentication** —
the editor's django CMS admin session — not API tokens. Cross-origin preview therefore
requires credentialed CORS and cross-site cookies (see
:doc:`../how-to/access-preview-content`).

Errors
------

* ``400 Bad Request`` — malformed ``X-Site-ID``.
* ``404 Not Found`` — unknown/forbidden language, unknown site, missing page, or content
  the current user may not view. The API returns ``404`` (not ``403``) for permission
  failures so it does not reveal that hidden content exists.
