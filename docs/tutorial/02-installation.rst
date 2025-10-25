Installation
============

Requirements
------------

djangocms-rest requires:

* Python 3.9 or higher
* Django 4.2 or higher
* django CMS 4.0 or higher, including latest 5.0+ versions
* Django REST Framework 3.14 or higher

Installation
------------
.. note::
    A running Django CMS project is required. Follow the `Installing Django CMS by hand <https://docs.django-cms.org/en/latest/introduction/01-install.html#installing-django-cms-by-hand>`_ guide to get started.

Using Poetry
~~~~~~~~~~~~

We recommend using ``Poetry`` to manage your dependencies. It is used by default in this documentation.
``pip`` can be used as equivalent.

.. code-block:: bash

    poetry add djangocms-rest

Using pip
~~~~~~~~~

.. code-block:: bash

    pip install djangocms-rest


Latest from source
~~~~~~~~~~~~~~~~~~~~~~~~
For the latest features, you can install a version from the GitHub repository at your own risk:

.. code-block:: bash

    poetry add git+https://github.com/django-cms/djangocms-rest.git

.. code-block:: bash

    # install a specific branch
    poetry add git+https://github.com/django-cms/djangocms-rest.git@feat/extended-search 

Basic Configuration
--------------------

1. Add ``djangocms_rest`` to your ``INSTALLED_APPS``:

.. code-block:: python

    INSTALLED_APPS = [
        # ... other Django apps
        ...,
        
        # django CMS
        'cms',

        # djangocms-rest
        'djangocms_rest',
        ...,
    ]

2. Include the djangocms-rest URLs in your project's main URL configuration:

.. code-block:: python
    
    # demo_cms/urls.py
    from django.urls import path, include

    urlpatterns = [
        # ... other URL patterns
        path('api/', include('djangocms_rest.urls')), #api can be changed to your liking
    ]

2.1 Add optional API prefix

Alternatively, you can put the API under a specific path, like ``api/cms/``. 
This is handy if you want to have a separate API for different parts of your app.

.. code-block:: python

    from django.urls import path, include

    urlpatterns = [
        # ... other URL patterns
        path('api/', include('my_django_rest_app.urls')),
        path('api/cms/', include('djangocms_rest.urls')), 
    ]

.. note::
    When you autocreate clients and types from OpenAPI specification with tools like `heyapi.dev <https://heyapi.dev/>`_, this will also affect the naming of those components and types, e.g.
    ``RetrieveLanguages`` will become ``CmsRetrieveLanguages`` in the client sdk.

CORS Support
------------

If you want to serve the API from a different domain, you can use the ``CorsMiddleware`` to enable CORS.
This is optional, but likely needed for security reasons with decoupled frontend apps.

Docs
~~~~
- `Django CORS Headers <https://github.com/adamchainz/django-cors-headers>`_


Configuration
~~~~~~~~~~~~~

.. code-block:: bash

    poetry add django-cors-headers


.. code-block:: python

    # settings.py
    INSTALLED_APPS = [
    ...,
    "corsheaders",
    ...,
    ]

    # add the allowed origins (your frontend apps) to the CORS settings
    CORS_ALLOWED_ORIGINS = [
    ...,
    "https://example.com", # set your own domain here, likely via env variable in production
    "http://localhost:300", # common js frontend app port
    "http://localhost:5173", # vue.js from our examples
    ...,
    ]


.. code-block:: python

    MIDDLEWARE = [
        "corsheaders.middleware.CorsMiddleware",
    ]


Languages Support
-----------------

- djangocms-rest supports languages out of the box. 
- Djnago CMS needs to be configured to use languages. 
- A single language must always be set in order to use the API.

Docs
~~~~
- `Django CMS - Internationalisation and Localisation <https://docs.django-cms.org/en/stable/explanation/i18n.html>`_
- `Django CMS - Language configuration <https://docs.django-cms.org/en/stable/reference/configuration.html#internationalisation-and-localisation-i18n-and-l10n>`_
- `Django CMS - Howto - Languages <https://docs.django-cms.org/en/latest/how_to/02-languages.html>`_

Configuration
~~~~~~~~~~~~~

This is a simple configuration to get you started. Follow the Django CMS documentation to configure languages in-depth.

.. code-block:: python

    # settings.py

    # Language settings
    LANGUAGE_CODE = "en"

    USE_I18N = True

    LANGUAGES = (
        ("de", _("German")),
        ("en", _("English")),
    )

    CMS_LANGUAGES = {
        1: [
            {
                "code": "en",
                "name": "English",
                "public": True,
            },
            {
                "code": "de",
                "name": _("Deutsch"),
                "public": False,
                "hide_untranslated": True,
            },
        ],
        "default": {
            "fallbacks": ["en"],
            "redirect_on_fallback": True,
            "public": True,
            "hide_untranslated": False,
        },
    }

    MIDDLEWARE = [
        ...,
        "cms.middleware.language.LanguageCookieMiddleware",
        ...,
    ]


.. code-block:: python
    
    # urls.py
    # example configuration
    urlpatterns += i18n_patterns(
        path('admin/', include(admin.site.urls)),
        path('', include('cms.urls')),
        prefix_default_language=False,
    )


Multi-Site Support
------------------

djangocms-rest supports 2 ways to handle multi-site support:

1. **Multi-Instance Setup:** Usually multiple instances of the CMS running on different domains. This is also valid option for headless mode. See the official `Django CMS - Multi-Site installation <https://docs.django-cms.org/en/stable/how_to/03-multi-site.html#multi-site-installation>`_ documentation for more information. 
2. **Single Instance Setup:** Run Django CMS in headless mode and serve multiple sites from a single instance. Using the ``SiteContextMiddleware`` from ``djangocms-rest`` to set the site context on the request.

**Option 1:**

1. foo.example.com/api/pages/ < REQUEST > Content foo site  
2. bar.example.com/api/pages/ < REQUEST > Content bar site

**Option 2:**

1. cms.example.com/api/pages/ < REQUEST HEADERS X-Site-ID: 1 > Content foo site
2. cms.example.com/api/pages/ < REQUEST HEADERS X-Site-ID: 2 > Content bar site

If you want to serve multiple sites from a single instance, you can use the ``SiteContextMiddleware`` to set the site context on the request.
This requires ``Django Sites`` framework to be installed and configured.

You can pass the site ID in the request headers with the ``X-Site-ID`` property set to the site ID. 
The Middleware will then set the site context on the request.

Docs
~~~~
- `Django Sites <https://docs.djangoproject.com/en/5.2/ref/contrib/sites/>`_
- `Enabling Sites Framework <https://docs.djangoproject.com/en/5.2/ref/contrib/sites/#enabling-the-sites-framework>`_
- `Django CMS - Multi-Site installation <https://docs.django-cms.org/en/stable/how_to/03-multi-site.html#multi-site-installation>`_

 For Option 2, you do not need to configure the webserver to manage multiples sites as the frontend apps are decoupled and run on a different domain.

.. note::

    You need to have CORS configured correctly to allow the frontend app to access the API.
    See `CORS Support <../tutorial/02-installation.html#cors-support>`_.

Configuration
~~~~~~~~~~~~~

.. code-block:: python
    
    INSTALLED_APPS = [
        ...
        'django.contrib.sites',
        ...
    ]

    # default site id, you likely wnat to change this using env variable in production
    SITE_ID = 1

.. code-block:: python
    
    CORS_ALLOW_ALL_ORIGINS=True # development seting, disable in production
    CORS_ALLOWED_ORIGINS = [
        "https://frontend.com", # your production frontend domain
        "http://localhost:3000", # common js frontend app port
        "http://localhost:5173", # vue.js from our examples
    ]

    # we need to add the X-Site-ID header to the allowed headers
    # Only required for single instance setup
    CORS_ALLOW_HEADERS = (
        *default_headers,
        "X-Site-ID",
    )

**Manage Sites in Django Admin**

- Go to Django Admin → Sites
- Add/edit sites with domain and name

Example:

.. code-block:: json

    // Manually configured via Django Admin
    // you can seed the ID in the browser url while editing the site object
    [
      {
        "domain": "foo.example.com",
        "name": "Foo Site"
      },
      {
        "domain": "bar.example.com", 
        "name": "Bar Site"
      }
    ]

.. code-block:: python

    MIDDLEWARE = [
        # Required for cross-origin requests (frontend on different domain)
        "corsheaders.middleware.CorsMiddleware",

        #before other middleware that depends on the site context
        "djangocms_rest.middleware.SiteContextMiddleware", 

        # other django and django CMS middleware (depends on your setup)
        ...
    ]

Testing
~~~~~~~

1. Create a test home page for each site in the Django admin.
2. Publish the pages.
3. Test the API endpoints with the ``X-Site-ID`` header set to the site ID.


.. code-block:: bash

    # pages endpoint without path will return the home page for the site
    curl -H "X-Site-ID: 2" http://localhost:8080/api/cms/pages/

.. note::
    The ``X-Site-ID`` header is required to query a single CMS instance. If not set, the middleware will use the current site defined in the settings.

Implementation Guide
~~~~~~~~~~~~~~~~~~~~

If the basic configuration is working you can embed it into your frontend app.

- :doc:`../how-to/01-use-multi-site`

Authentication
--------------

djangocms-rest currently uses ``Session Authentication`` as the only authentication method. 
This means that users must be logged into the Django CMS admin using the standard admin login page to access protected API endpoints.
In order to access the API from the frontend app, you need to configure Django ``CORS`` and
``CSRF``.

- Only authenticated users can access the API using the ``preview`` query parameter.

Docs
~~~~
- `Django - Default authentication <https://docs.djangoproject.com/en/5.2/topics/auth/default/>`_
- `Django CMS - Custom User Requirements <https://docs.django-cms.org/en/latest/reference/configuration.html#custom-user-requirements>`_
- `Security Enhancements for Django CMS <https://www.django-cms.org/en/blog/2022/02/22/security-enhancements-for-django-cms/>`_

.. note::

    You need to have CORS configured correctly to allow the frontend app to access the API.
    See `CORS Support <../tutorial/02-installation.html#cors-support>`_.

Configuration
~~~~~~~~~~~~~

.. code-block:: python

    # Additional CORS configuration for session authentication
    CORS_ALLOW_CREDENTIALS = True

    # add your frontend domain(s) here
    CSRF_TRUSTED_ORIGINS = [
        "https://frontend.com",
        "http://localhost:3000",
        "http://localhost:5173",
    ]

    # allow session and csrf cookies to be sent to frontend
    # required for session authentication to work
    SESSION_COOKIE_SAMESITE = "None"
    CSRF_COOKIE_SAMESITE = "None"
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

Testing
~~~~~~~

1. Login to Django admin at `http://localhost:8080/admin/ <http://localhost:8080/admin/>`_
2. Change the home page name, but do not publish it.
3. Visit and api endpoint with the ``preview`` query parameter.  

.. code-block:: bash

    # Adjust language if necessary
    http://localhost:8080/api/en/pages/?preview=true


OpenAPI Documentation
---------------------

For interactive API documentation and client SDK generation, follow the :doc:`03-openapi-documentation` tutorial.


**OpenAPI Documentation Benefits:**

- Interactive API documentation with Swagger UI
- OpenAPI schema generation for client SDKs
- Type-safe frontend development