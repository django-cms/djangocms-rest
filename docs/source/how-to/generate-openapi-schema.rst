Generate the OpenAPI schema and a typed client
==============================================

djangocms-rest is fully typed and can emit an OpenAPI 3 schema for every endpoint —
including a JSON-schema description of each installed plugin. With `drf-spectacular
<https://drf-spectacular.readthedocs.io/>`_ you get browsable docs (Swagger UI / ReDoc)
and a schema you can feed to a client generator for a type-safe frontend.

Steps
-----

1. Install drf-spectacular:

   .. code-block:: bash

       pip install drf-spectacular

2. Register it as the schema class and add it to ``INSTALLED_APPS``:

   .. code-block:: python

       # settings.py
       INSTALLED_APPS = [
           # ...
           "drf_spectacular",
       ]

       REST_FRAMEWORK = {
           "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
       }

       SPECTACULAR_SETTINGS = {
           "TITLE": "My project API",
           "DESCRIPTION": "Headless django CMS content API",
           # Reported as `info.version` in the schema. Use *your* project's API
           # version — tying it to a constant keeps it in step with releases:
           #     from myproject import __version__
           #     "VERSION": __version__,
           "VERSION": "1.0.0",
           "SERVE_INCLUDE_SCHEMA": False,
       }

   .. note::

      ``VERSION`` is your API's version, not the djangocms-rest version. (djangocms-rest's
      own test project happens to set ``"VERSION": djangocms_rest.__version__`` — that's a
      convenient pattern for tracking a constant, not a value you should copy verbatim.)

3. Expose the schema and documentation views:

   .. code-block:: python

       # urls.py
       from drf_spectacular.views import (
           SpectacularAPIView,
           SpectacularJSONAPIView,
           SpectacularSwaggerView,
           SpectacularRedocView,
       )

       urlpatterns += [
           path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
           path("api/schema-json/", SpectacularJSONAPIView.as_view(), name="schema-json"),
           path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
           path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
       ]

Verify
------

* Browsable docs: ``http://localhost:8080/api/docs/`` (Swagger UI) and
  ``http://localhost:8080/api/redoc/`` (ReDoc).
* Raw schema: ``http://localhost:8080/api/schema-json/``.

Generate a typed client
------------------------

Point a generator at the schema URL. For TypeScript, `@hey-api/openapi-ts
<https://heyapi.dev/>`_ produces a client and types (and can integrate `Zod
<https://zod.dev/>`_ for runtime validation):

.. code-block:: bash

    npx @hey-api/openapi-ts \
        -i http://localhost:8080/api/schema-json/ \
        -o src/client

.. note::

   Operation ids — and therefore generated function/type names — follow the mount point
   you chose in ``urls.py``. If you mount the API under ``api/cms/``, ``RetrieveLanguages``
   becomes ``CmsRetrieveLanguages``. Choose the mount point before you generate clients to
   avoid churn.

Typing plugin content
----------------------

Plugin payloads are dynamic, so their detailed shape comes from the
``/api/plugins/`` endpoint rather than the static schema. To get rich,
fully typed plugin properties, declare a ``serializer_class`` on your plugins — see
:doc:`serialize-plugins`.

.. seealso::

   * :doc:`../reference/index` — the endpoints the schema describes.
   * :doc:`../explanation/plugin-serialization` — how plugin definitions are derived.
