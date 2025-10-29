Quick Start
===========

Get up and running with djangocms-rest in minutes.

Prerequisites
-------------

.. note::
    A running Django CMS project is required. Follow the `Installing Django CMS by hand <https://docs.django-cms.org/en/latest/introduction/01-install.html#installing-django-cms-by-hand>`_ guide to get started.

Installation
------------

.. code-block:: bash

    # Install djangocms-rest
    poetry add djangocms-rest

Configuration
------------

.. code-block:: python

    # Add to INSTALLED_APPS in your project's settings.py
    INSTALLED_APPS = [
        # ... other apps
        'djangocms_rest',
    ]

.. code-block:: python

    # Include URLs in your project's urls.py
    urlpatterns = [
        # ... other URLs
        path('api/', include('djangocms_rest.urls')),
    ]

Start Server
------------

.. code-block:: bash

    # Start the Django development server
    python manage.py runserver 8080

Test API
--------

Visit `http://localhost:8080/api/languages/ <http://localhost:8080/api/languages/>`_ to test the API endpoints.

.. code-block:: bash

    # Test the API endpoints
    curl -X 'GET' \
      'http://localhost:8080/api/languages/' \
      -H 'accept: application/json'

If you see a response like this, you're good to go:

.. code-block:: json

    [
      {
        "code": "en",
        "name": "English",
        "public": true,
        "fallbacks": [
          "en"
        ],
        "redirect_on_fallback": true,
        "hide_untranslated": false
      },
      {
        "code": "de",
        "name": "Deutsch",
        "public": false,
        "fallbacks": [
          "en"
        ],
        "redirect_on_fallback": true,
        "hide_untranslated": true
      }
    ]

See the :doc:`../reference/languages` reference for more information.

Next Steps
----------

- Follow the :doc:`02-installation` guide for advanced features like multi-site support, languages, and OpenAPI documentation
- Explore the :doc:`../reference/index` for detailed API documentation
- Check out :doc:`../how-to/index` for implementation guides
