Reference
=========

The **authoritative, per-endpoint reference is the live OpenAPI schema** generated from
the running code by ``drf-spectacular``. It always matches your installed version —
exact paths, parameters, response fields and examples — which a hand-written page cannot
guarantee. Set it up once (see :doc:`../how-to/generate-openapi-schema`) and browse:

* **Swagger UI** — ``/api/docs/``
* **ReDoc** — ``/api/redoc/``
* **Raw schema** — ``/api/schema/`` (or ``/api/schema-json/``)

This section documents what the schema *cannot* express on its own:

* :doc:`conventions` — the cross-cutting behavioural rules (language prefix, ``preview``,
  ``html``, ``X-Site-ID``, pagination, permissions and errors).
* :doc:`settings` — the settings that change how the API behaves.

The rest of this page is a **map** of the available endpoints. Treat the paths as stable
but defer to the live schema for the precise parameters and response of your version.

.. toctree::
   :hidden:

   conventions
   settings

Endpoint catalogue
------------------

Content
~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - Endpoint
     - Returns
   * - ``GET /api/languages/``
     - Configured (public) languages for the site. Not language-prefixed.
   * - ``GET /api/{language}/pages/``
     - The home page, with placeholder content embedded.
   * - ``GET /api/{language}/pages/{path}/``
     - A page by path, with placeholder content embedded.
   * - ``GET /api/{language}/pages-list/``
     - Paginated list of page metadata (no embedded content).
   * - ``GET /api/{language}/pages-tree/``
     - The full page tree as metadata (no embedded content).
   * - ``GET /api/{language}/page_search/?q=``
     - Pages matching a search term (paginated).
   * - ``GET /api/{language}/placeholders/{content_type_id}/{object_id}/{slot}/``
     - The serialized plugin content of one placeholder. ``?html=1`` adds rendered HTML.
   * - ``GET /api/plugins/``
     - Type definitions for every registered plugin. Not language-prefixed.

Why some endpoints embed content and others return links — and how plugin content is
shaped — is explained in :doc:`../explanation/content-model` and
:doc:`../explanation/plugin-serialization`.

Navigation
~~~~~~~~~~

The navigation endpoints mirror the django CMS template tags and **return JSON arrays of
navigation nodes**. Trailing path segments are optional; omitting one uses its default.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Endpoint family
     - Mirrors / notes
   * - ``GET /api/{language}/menu/…``
     - ``{% show_menu %}``. Optional segments
       ``{from_level}/{to_level}/{extra_inactive}/{extra_active}`` (defaults
       ``0/100/0/1000``), optional leading ``{root_id}`` and trailing ``{path}``.
   * - ``GET /api/{language}/submenu/…``
     - ``{% show_sub_menu %}``. Optional ``{levels}/{root_level}/{nephews}`` (defaults
       ``100/–/100``) and trailing ``{path}``.
   * - ``GET /api/{language}/breadcrumbs/…``
     - ``{% show_breadcrumb %}``. Optional ``{start_level}`` (default ``0``) and trailing
       ``{path}``. The trail is a flat array of ancestors, not nested.

See `django CMS — navigation
<https://docs.django-cms.org/en/latest/reference/navigation.html>`_ for the underlying
tags.

Operations
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - Endpoint
     - Returns
   * - ``GET /api/healthcheck/``
     - ``{"status": "ok"}`` for uptime monitoring. Not language-prefixed.
