Pages Endpoints
===============

**The Pages endpoints provide django CMS pages and their content.**

* This returns all pages available for the specified language with their metadata and placeholder information
* Page information includes titles, URLs, navigation settings, and template configurations
* This endpoint is essential for page meta information, SEO and building page listings
* Pages can be retrieved as a nested tree structure or a list of pages with pagination support

.. note::
    This does only return page meta informaiton. To retrieve the page content, you need to use the :doc:`Placeholders <placeholders>`.

.. warning::
    Fetching a deeply nested tree of pages can be very slow for large page sets. Use the :ref:`Pages List API <list-pages-paginated>` instead.


CMS Reference
-------------

- `Page configuration <https://docs.django-cms.org/en/latest/reference/configuration.html#cms-templates>`_
- `Page templates <https://docs.django-cms.org/en/latest/how_to/templates.html>`_

Endpoints
---------

List Pages
~~~~~~~~~~

**GET** ``/api/{language}/pages/``

Retrieve a list of all pages for the specified language.

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
* ``placeholders``: Array of placeholder relations with content_type_id, object_id, slot, and details

.. note::
    You can use the `application_namespace` identifer to render your django app in a decoupled frontend application.
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
                "content_type_id": 5,
                "object_id": 11,
                "slot": "content",
                "details": "http://localhost:8080/api/en/placeholders/5/11/content/"
            },
            {
                "content_type_id": 5,
                "object_id": 11,
                "slot": "cta",
                "details": "http://localhost:8080/api/en/placeholders/5/11/cta/"
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
                "content_type_id": 5,
                "object_id": 12,
                "slot": "content",
                "details": "http://localhost:8080/api/en/placeholders/5/12/content/"
            }
        ]
    }



.. _list-pages-paginated:

List Pages (Paginated)
~~~~~~~~~~~~~~~~~~~~~~

**GET** ``/api/{language}/pages-list/``

Retrieve a simplified list of pages with basic information.

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
                "absolute_url": "http://localhost:8080/en/",
                "path": "/en/",
                "is_home": true,
                "in_navigation": true
            },
            {
                "title": "About Us",
                "absolute_url": "http://localhost:8080/en/about/",
                "path": "/en/about/",
                "is_home": false,
                "in_navigation": true
            }
        ]
    }

Pages Tree
~~~~~~~~~~

**GET** ``/api/{language}/pages-tree/``

Retrieve pages in a hierarchical tree structure.

**Path Parameters:**

* ``language`` (string, required): Language code (e.g., "en", "de")

**Query Parameters:**

* ``preview`` (boolean, optional): Set to true to preview unpublished content (admin access required)

**Example Request:**

.. code-block:: bash

    GET /api/en/pages-tree/?preview=true

**Example Response:**

.. code-block:: json

    {
        "title": "Home",
        "absolute_url": "http://localhost:8080/en/",
        "path": "/en/",
        "is_home": true,
        "in_navigation": true,
        "children": [
            {
                "title": "About Us",
                "absolute_url": "http://localhost:8080/en/about/",
                "path": "/en/about/",
                "is_home": false,
                "in_navigation": true,
                "children": []
            },
            {
                "title": "Contact",
                "absolute_url": "http://localhost:8080/en/contact/",
                "path": "/en/contact/",
                "is_home": false,
                "in_navigation": true,
                "children": []
            }
        ]
    }