Pages
=====

**Pages and their content.**

* This returns all pages available for the specified language with their metadata and placeholder information
* Page information includes titles, URLs, navigation settings, and template configurations
* This endpoint is essential for page meta information, SEO and building page listings
* Pages can be retrieved as a nested tree structure or a list of pages with pagination support

.. note::
    The single-page endpoints (``/pages/`` and ``/pages/{path}/``) embed each placeholder
    together with its serialized ``content``. The list and tree endpoints
    (``/pages-list/`` and ``/pages-tree/``) return page meta information only; use the
    :doc:`Placeholders <placeholders>` endpoint to retrieve their content.

.. warning::
    Fetching a deeply nested tree of pages can be very slow for large page sets. Use the :ref:`Pages List API <list-pages-paginated>` instead.


CMS Reference
-------------

- `Page configuration <https://docs.django-cms.org/en/latest/reference/configuration.html#cms-templates>`_
- `Page templates <https://docs.django-cms.org/en/latest/how_to/templates.html>`_

Endpoints
---------

Retrieve Home Page
~~~~~~~~~~~~~~~~~~

**GET** ``/api/{language}/pages/``

Retrieve the home (root) page for the specified language. The response is a single page
object that includes its placeholders together with their serialized content.

**Response Attributes:**

* ``title``: Page title
* ``page_title``: SEO page title
* ``menu_title``: Navigation menu title
* ``meta_description``: SEO meta description
* ``redirect``: Redirect URL
* ``in_navigation``: Whether the page appears in navigation
* ``soft_root``: Whether this is a soft root page
* ``template``: Page template name
* ``xframe_options``: X-Frame-Options setting
* ``limit_visibility_in_menu``: Whether to limit visibility in menu
* ``language``: Language code
* ``path``: URL path
* ``absolute_url``: Complete URL to the page
* ``is_home``: Whether this is the home page
* ``login_required``: Whether login is required to view the page
* ``languages``: Array of available language codes
* ``is_preview``: Whether this is a preview
* ``application_namespace``: Application namespace
* ``creation_date``: Page creation date (ISO format)
* ``changed_date``: Last modification date (ISO format)
* ``details``: Page details/description
* ``placeholders``: Array of placeholders, each with ``slot``, ``label``, ``language``, ``content`` (serialized plugin tree), ``details`` (link to the placeholder endpoint), and ``html`` (empty unless ``?html=1`` is set)

.. note::
    You can use the `application_namespace` identifier to render your django app in a decoupled frontend application.
    Similar to how you would render a django app using `app_hooks`.



**Path Parameters:**

* ``language`` (string, required): Language code (e.g., "en", "de")

**Query Parameters:**

* ``preview`` (boolean, optional): Set to true to preview unpublished content (admin access required)

**Example Request:**

.. code-block:: bash

    GET /api/en/pages/?preview=true

**Example Response:**

.. code-block:: json

    {
        "title": "test",
        "page_title": "test",
        "menu_title": "test",
        "meta_description": "",
        "redirect": "",
        "in_navigation": true,
        "soft_root": false,
        "template": "INHERIT",
        "xframe_options": "",
        "limit_visibility_in_menu": false,
        "language": "en",
        "path": "",
        "absolute_url": "http://localhost:8080/",
        "is_home": true,
        "login_required": false,
        "languages": [
            "de",
            "en"
        ],
        "is_preview": false,
        "application_namespace": "",
        "creation_date": "2025-05-22T19:30:49.343177Z",
        "changed_date": "2025-05-22T19:30:49.343248Z",
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
            },
            {
                "slot": "cta",
                "label": "CTA",
                "language": "en",
                "content": [],
                "details": "http://localhost:8080/api/en/placeholders/5/11/cta/",
                "html": ""
            }
        ]
    }

Retrieve Page by Path
~~~~~~~~~~~~~~~~~~~~~

**GET** ``/api/{language}/pages/{path}/``

Retrieve a specific page by its path.

**Path Parameters:**

* ``language`` (string, required): Language code (e.g., "en", "de")
* ``path`` (string, required): Page path (e.g., "about", "contact")

**Query Parameters:**

* ``preview`` (boolean, optional): Set to true to preview unpublished content (admin access required)

**Example Request:**

.. code-block:: bash

    GET /api/en/pages/about/?preview=true

**Example Response:**

.. code-block:: json

    {
        "title": "About Us",
        "page_title": "About Us - Our Company",
        "menu_title": "About",
        "meta_description": "Learn more about our company",
        "redirect": "",
        "in_navigation": true,
        "soft_root": false,
        "template": "INHERIT",
        "xframe_options": "",
        "limit_visibility_in_menu": false,
        "language": "en",
        "path": "/en/about/",
        "absolute_url": "http://localhost:8080/en/about/",
        "is_home": false,
        "login_required": false,
        "languages": [
            "de",
            "en"
        ],
        "is_preview": false,
        "application_namespace": "",
        "creation_date": "2025-05-22T19:30:49.343177Z",
        "changed_date": "2025-05-22T19:30:49.343248Z",
        "details": "http://localhost:8080/api/en/pages/about/",
        "placeholders": [
            {
                "slot": "content",
                "label": "Content",
                "language": "en",
                "content": [
                    {
                        "plugin_type": "TextPlugin",
                        "body": "<p>About us.</p>"
                    }
                ],
                "details": "http://localhost:8080/api/en/placeholders/5/12/content/",
                "html": ""
            }
        ]
    }

.. note::

   Both single-page endpoints (``/pages/`` and ``/pages/{path}/``) embed each placeholder
   together with its serialized ``content``. The list and tree endpoints below return page
   metadata only, with a ``details`` link per placeholder. See
   :doc:`../explanation/content-model`.

.. _pages-list:
.. _list-pages-paginated:

List Pages (Paginated)
~~~~~~~~~~~~~~~~~~~~~~

**GET** ``/api/{language}/pages-list/``

Retrieve a paginated list of pages for the specified language. Each entry contains the
same page meta fields as a single page (without ``placeholders``).

**Path Parameters:**

* ``language`` (string, required): Language code (e.g., "en", "de")

**Query Parameters:**

* ``limit`` (integer, optional): Number of items to return
* ``offset`` (integer, optional): Number of items to skip
* ``preview`` (boolean, optional): Set to true to preview unpublished content (admin access required)

**Example Request:**

.. code-block:: bash

    GET /api/en/pages-list/?limit=10&offset=0&preview=true

**Example Response:**

.. code-block:: json

    {
        "count": 25,
        "next": "http://localhost:8080/api/en/pages-list/?limit=10&offset=10",
        "previous": null,
        "results": [
            {
                "title": "Home",
                "page_title": "Home",
                "menu_title": "Home",
                "meta_description": "",
                "redirect": "",
                "in_navigation": true,
                "soft_root": false,
                "template": "INHERIT",
                "xframe_options": "",
                "limit_visibility_in_menu": false,
                "language": "en",
                "path": "/en/",
                "absolute_url": "http://localhost:8080/en/",
                "is_home": true,
                "login_required": false,
                "languages": ["de", "en"],
                "is_preview": false,
                "application_namespace": "",
                "creation_date": "2025-05-22T19:30:49.343177Z",
                "changed_date": "2025-05-22T19:30:49.343248Z",
                "details": "http://localhost:8080/api/en/pages/"
            },
            {
                "title": "About Us",
                "page_title": "About Us - Our Company",
                "menu_title": "About",
                "meta_description": "Learn more about our company",
                "redirect": "",
                "in_navigation": true,
                "soft_root": false,
                "template": "INHERIT",
                "xframe_options": "",
                "limit_visibility_in_menu": false,
                "language": "en",
                "path": "/en/about/",
                "absolute_url": "http://localhost:8080/en/about/",
                "is_home": false,
                "login_required": false,
                "languages": ["de", "en"],
                "is_preview": false,
                "application_namespace": "",
                "creation_date": "2025-05-22T19:30:49.343177Z",
                "changed_date": "2025-05-22T19:30:49.343248Z",
                "details": "http://localhost:8080/api/en/pages/about/"
            }
        ]
    }

.. _pages-search:

Search Pages
~~~~~~~~~~~~

**GET** ``/api/{language}/page_search/``

Search for pages matching a search term. Returns the same paginated structure as the
:ref:`Pages List API <list-pages-paginated>`.

**Path Parameters:**

* ``language`` (string, required): Language code (e.g., "en", "de")

**Query Parameters:**

* ``q`` (string, optional): Search term used to find matching pages
* ``limit`` (integer, optional): Number of items to return
* ``offset`` (integer, optional): Number of items to skip
* ``preview`` (boolean, optional): Set to true to preview unpublished content (admin access required)

.. note::
    Without a ``q`` parameter the search returns an empty result set.

**Example Request:**

.. code-block:: bash

    GET /api/en/page_search/?q=about

**Example Response:**

.. code-block:: json

    {
        "count": 1,
        "next": null,
        "previous": null,
        "results": [
            {
                "title": "About Us",
                "page_title": "About Us - Our Company",
                "menu_title": "About",
                "meta_description": "Learn more about our company",
                "redirect": "",
                "in_navigation": true,
                "soft_root": false,
                "template": "INHERIT",
                "xframe_options": "",
                "limit_visibility_in_menu": false,
                "language": "en",
                "path": "/en/about/",
                "absolute_url": "http://localhost:8080/en/about/",
                "is_home": false,
                "login_required": false,
                "languages": ["de", "en"],
                "is_preview": false,
                "application_namespace": "",
                "creation_date": "2025-05-22T19:30:49.343177Z",
                "changed_date": "2025-05-22T19:30:49.343248Z",
                "details": "http://localhost:8080/api/en/pages/about/"
            }
        ]
    }

Pages Tree
~~~~~~~~~~

**GET** ``/api/{language}/pages-tree/``

Retrieve pages in a hierarchical tree structure. The response is an array of root page
nodes; each node carries the full page meta fields plus a ``children`` array of the same
shape.

**Path Parameters:**

* ``language`` (string, required): Language code (e.g., "en", "de")

**Query Parameters:**

* ``preview`` (boolean, optional): Set to true to preview unpublished content (admin access required)

**Example Request:**

.. code-block:: bash

    GET /api/en/pages-tree/?preview=true

**Example Response:**

.. code-block:: json

    [
        {
            "title": "Home",
            "page_title": "Home",
            "menu_title": "Home",
            "meta_description": "",
            "redirect": "",
            "in_navigation": true,
            "soft_root": false,
            "template": "INHERIT",
            "xframe_options": "",
            "limit_visibility_in_menu": false,
            "language": "en",
            "path": "/en/",
            "absolute_url": "http://localhost:8080/en/",
            "is_home": true,
            "login_required": false,
            "languages": ["de", "en"],
            "is_preview": false,
            "application_namespace": "",
            "creation_date": "2025-05-22T19:30:49.343177Z",
            "changed_date": "2025-05-22T19:30:49.343248Z",
            "details": "http://localhost:8080/api/en/pages/",
            "children": [
                {
                    "title": "About Us",
                    "page_title": "About Us - Our Company",
                    "menu_title": "About",
                    "meta_description": "Learn more about our company",
                    "redirect": "",
                    "in_navigation": true,
                    "soft_root": false,
                    "template": "INHERIT",
                    "xframe_options": "",
                    "limit_visibility_in_menu": false,
                    "language": "en",
                    "path": "/en/about/",
                    "absolute_url": "http://localhost:8080/en/about/",
                    "is_home": false,
                    "login_required": false,
                    "languages": ["de", "en"],
                    "is_preview": false,
                    "application_namespace": "",
                    "creation_date": "2025-05-22T19:30:49.343177Z",
                    "changed_date": "2025-05-22T19:30:49.343248Z",
                    "details": "http://localhost:8080/api/en/pages/about/",
                    "children": []
                }
            ]
        }
    ]