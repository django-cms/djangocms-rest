Enable CORS for a decoupled frontend
====================================

A headless frontend usually runs on a different origin (domain or port) than django CMS.
Browsers block such cross-origin requests unless the server sends the right CORS headers.
This guide configures `django-cors-headers
<https://github.com/adamchainz/django-cors-headers>`_ so your frontend can call the API.

.. note::

   CORS only matters for requests made by a browser. Server-side fetches (a Node/Nuxt
   server, a static-site build, ``curl``) are not subject to it.

Steps
-----

1. Install the package:

   .. code-block:: bash

       pip install django-cors-headers

2. Add it to ``INSTALLED_APPS`` and put its middleware high in the stack — before any
   middleware that generates a response (and, if you use it, before
   :doc:`SiteContextMiddleware <serve-multiple-sites>`):

   .. code-block:: python

       INSTALLED_APPS = [
           # ...
           "corsheaders",
       ]

       MIDDLEWARE = [
           "corsheaders.middleware.CorsMiddleware",
           # ... the rest of your middleware
       ]

3. List the frontend origins that may call the API. Never use a wildcard in production:

   .. code-block:: python

       CORS_ALLOWED_ORIGINS = [
           "https://example.com",     # your production frontend
           "http://localhost:3000",   # e.g. a Next.js dev server
           "http://localhost:5173",   # e.g. a Vite/Vue dev server
       ]

Verify
------

Trigger a request from your frontend (or simulate the preflight) and confirm the response
carries an ``Access-Control-Allow-Origin`` header for your origin:

.. code-block:: bash

    curl -I -H "Origin: http://localhost:5173" \
        http://localhost:8080/api/en/pages/

Going further
-------------

* **Custom headers.** If you serve :doc:`multiple sites from one instance
  <serve-multiple-sites>`, the browser must be allowed to send the ``X-Site-ID`` header:

  .. code-block:: python

      from corsheaders.defaults import default_headers

      CORS_ALLOW_HEADERS = (*default_headers, "X-Site-ID")

* **Credentials.** Session-authenticated requests (used for
  :doc:`draft previews <access-preview-content>`) additionally need
  ``CORS_ALLOW_CREDENTIALS = True`` and matching cookie settings.

.. seealso::

   `django-cors-headers documentation <https://github.com/adamchainz/django-cors-headers>`_
