Settings
========

djangocms-rest is configured almost entirely through django CMS, Django and third-party
settings. It defines **one** setting of its own; the rest of this page lists the existing
settings that change how the API behaves, with pointers to the guides that use them.

Settings defined by djangocms-rest
----------------------------------

.. _setting-rest-json-rendering:

``REST_JSON_RENDERING``
~~~~~~~~~~~~~~~~~~~~~~~~

:Type: ``bool``
:Default: ``not CMS_TEMPLATES`` — i.e. ``True`` when no classic ``CMS_TEMPLATES`` are
          configured (a headless install), ``False`` otherwise.

Controls whether django CMS renders content as **JSON in the editing UI** (the toolbar /
structure board), using the package's ``RESTRenderer``. When enabled, djangocms-rest also
disables ``djangocms-text``'s inline editing (``TEXT_INLINE_EDITING``), since rich text is
delivered as data rather than edited in place.

.. important::

   This setting affects only what *editors* see inside django CMS. It does **not** change
   the REST API responses — content endpoints always return serialized JSON regardless of
   its value.

Set it explicitly to override the default — for example, to keep JSON rendering on in a
project that still defines ``CMS_TEMPLATES``:

.. code-block:: python

    # settings.py
    REST_JSON_RENDERING = True

See :doc:`../explanation/headless` for the editing-and-preview model this fits into.

Django CMS settings that affect the API
---------------------------------------

These are standard `django CMS settings
<https://docs.django-cms.org/en/latest/reference/configuration.html>`_; djangocms-rest
reads them rather than defining them.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Setting
     - Effect on djangocms-rest
   * - ``CMS_LANGUAGES``
     - Drives the :doc:`languages` endpoint and per-language content resolution, including
       ``public``, ``fallbacks`` and ``hide_untranslated``. See
       :doc:`../how-to/configure-languages`.
   * - ``CMS_TEMPLATES``
     - Its presence is the default basis for :ref:`REST_JSON_RENDERING <setting-rest-json-rendering>`.
   * - ``CMS_PLACEHOLDER_CONF``
     - Declares placeholder slots and constraints; reflected by the
       :doc:`placeholders` endpoint.
   * - ``CMS_CACHE_DURATIONS``
     - The ``"content"`` duration caps how long serialized placeholder content is cached.
       See :doc:`../explanation/caching`.

Django settings that affect the API
-----------------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Setting
     - Effect on djangocms-rest
   * - ``LANGUAGES`` / ``LANGUAGE_CODE`` / ``USE_I18N``
     - Standard Django i18n, configured alongside ``CMS_LANGUAGES``
       (:doc:`../how-to/configure-languages`).
   * - ``SITE_ID`` + ``django.contrib.sites``
     - The fallback site when no ``X-Site-ID`` header is sent, and the basis for
       multi-site scoping. See :doc:`../how-to/serve-multiple-sites`.
   * - ``CACHES``
     - The Django cache backend used to store serialized placeholder content
       (:doc:`../explanation/caching`).
   * - ``CSRF_TRUSTED_ORIGINS``, ``SESSION_COOKIE_SAMESITE``,
       ``SESSION_COOKIE_SECURE``, ``CSRF_COOKIE_SAMESITE``, ``CSRF_COOKIE_SECURE``
     - Required for cross-origin, session-authenticated preview requests. See
       :doc:`../how-to/access-preview-content`.

Third-party settings
---------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Setting
     - Effect on djangocms-rest
   * - ``CORS_ALLOWED_ORIGINS``, ``CORS_ALLOW_HEADERS``, ``CORS_ALLOW_CREDENTIALS``
     - From `django-cors-headers <https://github.com/adamchainz/django-cors-headers>`_;
       needed for browser frontends and for the ``X-Site-ID`` header. See
       :doc:`../how-to/configure-cors`.
   * - ``REST_FRAMEWORK``
     - Django REST framework configuration. Set ``DEFAULT_SCHEMA_CLASS`` to enable
       OpenAPI generation (:doc:`../how-to/generate-openapi-schema`).
   * - ``SPECTACULAR_SETTINGS``
     - `drf-spectacular <https://drf-spectacular.readthedocs.io/>`_ schema/documentation
       options (optional).
   * - ``TEXT_INLINE_EDITING``
     - From ``djangocms-text``. Forced to ``False`` when
       :ref:`REST_JSON_RENDERING <setting-rest-json-rendering>` is active.

Middleware
----------

``djangocms_rest.middleware.SiteContextMiddleware`` is not a setting but is added to
``MIDDLEWARE`` to resolve the ``X-Site-ID`` request header for single-instance multi-site
deployments. See :doc:`../how-to/serve-multiple-sites`.
