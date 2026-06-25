Quick Start
===========

In this lesson you will add djangocms-rest to a django CMS project and walk the full
content path the API exposes: list the configured languages, fetch the home page, and
then follow the link it gives you to retrieve the actual plugin content of a placeholder.

By the end you will understand the two-step shape of the API — *pages carry placeholders,
placeholders carry content* — which is the key to everything else in these docs.

.. note::

   You need a working django CMS 5 project with at least one published page. If you do
   not have one yet, follow `Installing django CMS by hand
   <https://docs.django-cms.org/en/latest/introduction/01-install.html>`_ first.

Step 1 — Install the package
----------------------------

.. code-block:: bash

    pip install djangocms-rest

This also installs **Django REST framework**, which djangocms-rest is built on and
*requires* — you do not install it separately. The OpenAPI schema and browsable docs come
from ``drf-spectacular``, which is **optional** and covered in
:doc:`../how-to/generate-openapi-schema`.

Step 2 — Enable the apps
------------------------

Add ``rest_framework`` and ``djangocms_rest`` to ``INSTALLED_APPS``:

.. code-block:: python

    # settings.py
    INSTALLED_APPS = [
        # ... your other apps
        "cms",
        "rest_framework",
        "djangocms_rest",
    ]

.. note::

    ``rest_framework`` enables Django REST framework's browsable API in the browser. The
    JSON API itself works without it in ``INSTALLED_APPS``, but adding it is recommended.

Step 3 — Mount the URLs
-----------------------

Include the djangocms-rest URLconf in your project's ``urls.py``. The mount point is up
to you; this tutorial uses ``api/``.

.. code-block:: python

    # urls.py
    from django.urls import path, include

    urlpatterns = [
        # ... your other patterns
        path("api/", include("djangocms_rest.urls")),
    ]

Step 4 — Start the server
-------------------------

.. code-block:: bash

    python manage.py runserver 8080

Step 5 — List the languages
---------------------------

The languages endpoint is the simplest one and needs no language prefix. It reflects your
django CMS ``CMS_LANGUAGES`` configuration.

.. code-block:: bash

    curl http://localhost:8080/api/languages/

You get back a **list** of the languages configured for the current site:

.. code-block:: json

    [
      {
        "code": "en",
        "name": "English",
        "public": true,
        "fallbacks": ["de"],
        "redirect_on_fallback": true,
        "hide_untranslated": false
      }
    ]

Pick a ``code`` from the response — this tutorial uses ``en``. Every content endpoint is
prefixed with a language code.

Step 6 — Fetch the home page
----------------------------

Request the home page for your language. The path-less ``pages/`` endpoint returns the
site's root page.

.. code-block:: bash

    curl http://localhost:8080/api/en/pages/

The response is a single page object. Note the ``placeholders`` array near the bottom —
each entry describes a content region of the page and embeds its serialized ``content``:

.. code-block:: json

    {
      "title": "Home",
      "path": "",
      "absolute_url": "http://localhost:8080/en/",
      "is_home": true,
      "language": "en",
      "languages": ["en"],
      "template": "home.html",
      "details": "http://localhost:8080/api/en/pages/",
      "placeholders": [
        {
          "slot": "content",
          "label": "Content",
          "language": "en",
          "content": [
            {
              "plugin_type": "TextPlugin",
              "body": "<p>Hello World!</p>"
            }
          ],
          "details": "http://localhost:8080/api/en/placeholders/5/11/content/",
          "html": ""
        }
      ]
    }

This is the central idea of the API:

* A **page** carries metadata (title, URL, template, navigation flags …) plus its
  **placeholders**.
* Each **placeholder** carries a list of serialized **plugins** in ``content``.
* Each plugin is a flat JSON object identified by ``plugin_type``.

Step 7 — Follow the placeholder link
------------------------------------

When you list or tree-traverse many pages at once, placeholder content is *not* embedded —
only a ``details`` link is returned, so listings stay fast. You fetch a placeholder's
content directly from that link:

.. code-block:: bash

    curl "http://localhost:8080/api/en/placeholders/5/11/content/"

.. code-block:: json

    {
      "slot": "content",
      "label": "Content",
      "language": "en",
      "content": [
        {
          "plugin_type": "TextPlugin",
          "body": "<p>Hello World!</p>"
        }
      ],
      "details": "http://localhost:8080/api/en/placeholders/5/11/content/",
      "html": ""
    }

Add ``?html=1`` to also receive the placeholder rendered as HTML, using your django CMS
plugin templates — handy when you want to migrate gradually or render rich text without a
custom component:

.. code-block:: bash

    curl "http://localhost:8080/api/en/placeholders/5/11/content/?html=1"

That's the whole loop: **languages → page → placeholder content**. Everything else the
API offers (menus, breadcrumbs, search, plugin type definitions) builds on these same
pieces.

Where to go next
----------------

Now that the basics work, reach for a guide when you have a concrete goal:

* :doc:`../how-to/configure-cors` — let a frontend on another domain call the API.
* :doc:`../how-to/generate-openapi-schema` — add the browsable docs and generate a typed client.
* :doc:`../how-to/access-preview-content` — fetch unpublished/draft content for editor previews.
* :doc:`../how-to/serve-multiple-sites` — serve several sites from one instance.

To understand *why* the API is shaped this way, read :doc:`../explanation/content-model`.
For the full list of endpoints and fields, see the :doc:`../reference/index`.
