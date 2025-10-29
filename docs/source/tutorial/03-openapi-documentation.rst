OpenAPI Documentation
====================

Set up automatic API documentation and schema generation for your djangocms-rest API.

.. note::
    Recommended for development. It enables interactive API documentation with typed responses.

Prerequisites
-------------

- Completed :doc:`02-installation` guide

Overview
--------

djangocms-rest is fully typed and supports OpenAPI 3 schema generation using `drf-spectacular <https://drf-spectacular.readthedocs.io/en/latest/>`_.
Swagger UI and Redoc are also supported and highly recommended for development.

Benefits
--------

* **Interactive API Documentation** - Browse and test endpoints directly in your browser
* **Automatic Schema Generation** - Generate OpenAPI schemas for all endpoints and plugins
* **Type Safety** - Use schema to generate type-safe client libraries for your frontend

Installation
-----------

.. code-block:: bash

    poetry add drf-spectacular

Configuration
-------------

Add to your Django settings:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'drf_spectacular',
        ...
    ]

    # Add REST Framework settings
    REST_FRAMEWORK = {
        'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
        ... # other settings
    }

    # Recommended settings (optional)
    SPECTACULAR_SETTINGS = {
        'TITLE': 'Your Project API',
        'DESCRIPTION': 'Your project description',
        'VERSION': '1.0.0',
        'SERVE_INCLUDE_SCHEMA': False,
        # other settings
    }

URL Configuration
-----------------

Add the OpenAPI endpoints to your URL configuration:

.. code-block:: python

    from drf_spectacular.views import (
        SpectacularAPIView,
        SpectacularJSONAPIView,
        SpectacularSwaggerView,
        SpectacularRedocView,
    )

    urlpatterns = [
        ...
        # OpenAPI schema and documentation
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
        path("api/schema-json/", SpectacularJSONAPIView.as_view(), name="schema-json"),
        path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
        ...
    ]

Testing
-------

You can now access:

- **Interactive API Documentation**: `http://localhost:8080/api/docs/ <http://localhost:8080/api/docs/>`_
- **OpenAPI JSON Schema**: `http://localhost:8080/api/schema-json/ <http://localhost:8080/api/schema-json/>`_

Client SDK Generation
--------------------

.. note::
    Using `heyapi.dev <https://heyapi.dev/>`_ you can generate a client SDK for your frontend app.

When you autocreate clients and types from OpenAPI specification with tools like `heyapi.dev <https://heyapi.dev/>`_, this will also affect the naming of those components and types, eg.
``RetrieveLanguages`` will become ``CmsRetrieveLanguages`` in the client SDK.

Next Steps
----------

- Explore the :doc:`../reference/index` for detailed API documentation
- Check out :doc:`../how-to/index` for implementation guides
