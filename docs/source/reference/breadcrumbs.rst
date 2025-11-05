Breadcrumbs Endpoints
====================

**The Breadcrumbs endpoints provide breadcrumb navigation structures in django CMS.**


.. code-block:: bash

    GET /api/en/breadcrumbs/

* This returns breadcrumb navigation structures for the specified language
* Breadcrumb information includes page titles, URLs, visibility settings, and hierarchical relationships
* This endpoint is essential for building breadcrumb navigation, page context, and site structure indicators
* Advanced endpoints allow filtering by start level and specific paths

CMS Reference
-------------

- `Menu configuration <https://docs.django-cms.org/en/latest/reference/configuration.html#cms-menus>`_
- `Navigation and menus <https://docs.django-cms.org/en/latest/how_to/menus.html>`_

Endpoints
---------

List Breadcrumbs
~~~~~~~~~~~~~~~~

**GET** ``/api/{language}/breadcrumbs/``

Get the complete breadcrumb structure for a specific language.

**Response Attributes:**

* ``namespace``: Application namespace (nullable)
* ``title``: Menu item title
* ``url``: Complete URL to the page (nullable)
* ``api_endpoint``: API endpoint URL for the page (nullable)
* ``visible``: Whether the menu item is visible
* ``selected``: Whether the menu item is currently selected
* ``attr``: Additional attributes (nullable)
* ``level``: Menu level/depth (nullable)
* ``children``: Array of child menu items

**Path Parameters:**

* ``language`` (string, required): Language code (e.g., "en", "de")

**Query Parameters:**

* ``preview`` (boolean, optional): Set to true to preview unpublished content (admin access required)

**Example Request:**

.. code-block:: bash

    GET /api/en/breadcrumbs/?preview=true

**Example Response:**

.. code-block:: json

    {
        "namespace": null,
        "title": "Home",
        "url": "http://localhost:8080/en/",
        "api_endpoint": "http://localhost:8080/api/en/pages/",
        "visible": true,
        "selected": false,
        "attr": null,
        "level": 0,
        "children": [
            {
                "namespace": null,
                "title": "About Us",
                "url": "http://localhost:8080/en/about/",
                "api_endpoint": "http://localhost:8080/api/en/pages/about/",
                "visible": true,
                "selected": true,
                "attr": null,
                "level": 1,
                "children": []
            }
        ]
    }

List Breadcrumbs by Path
~~~~~~~~~~~~~~~~~~~~~~~~

**GET** ``/api/{language}/breadcrumbs/{path}/``

Get the breadcrumb structure filtered by specific path.

**Path Parameters:**

* ``language`` (string, required): Language code (e.g., "en", "de")
* ``path`` (string, required): Path as starting node for the breadcrumbs

**Query Parameters:**

* ``preview`` (boolean, optional): Set to true to preview unpublished content (admin access required)

**Example Request:**

.. code-block:: bash

    GET /api/en/breadcrumbs/about/?preview=true

**Example Response:**

.. code-block:: json

    {
        "namespace": null,
        "title": "Home",
        "url": "http://localhost:8080/en/",
        "api_endpoint": "http://localhost:8080/api/en/pages/",
        "visible": true,
        "selected": false,
        "attr": null,
        "level": 0,
        "children": [
            {
                "namespace": null,
                "title": "About Us",
                "url": "http://localhost:8080/en/about/",
                "api_endpoint": "http://localhost:8080/api/en/pages/about/",
                "visible": true,
                "selected": true,
                "attr": null,
                "level": 1,
                "children": []
            }
        ]
    }

List Breadcrumbs by Start Level
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**GET** ``/api/{language}/breadcrumbs/{start_level}/``

Get the breadcrumb structure filtered by start level.

**Path Parameters:**

* ``language`` (string, required): Language code (e.g., "en", "de")
* ``start_level`` (integer, required): Starting level for breadcrumb items

**Query Parameters:**

* ``preview`` (boolean, optional): Set to true to preview unpublished content (admin access required)

**Example Request:**

.. code-block:: bash

    GET /api/en/breadcrumbs/1/?preview=true

**Example Response:**

.. code-block:: json

    {
        "namespace": null,
        "title": "About Us",
        "url": "http://localhost:8080/en/about/",
        "api_endpoint": "http://localhost:8080/api/en/pages/about/",
        "visible": true,
        "selected": true,
        "attr": null,
        "level": 1,
        "children": []
    }

List Breadcrumbs by Start Level and Path
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**GET** ``/api/{language}/breadcrumbs/{start_level}/{path}/``

Get the breadcrumb structure filtered by start level and specific path.

**Path Parameters:**

* ``language`` (string, required): Language code (e.g., "en", "de")
* ``start_level`` (integer, required): Starting level for breadcrumb items
* ``path`` (string, required): Path as starting node for the breadcrumbs

**Query Parameters:**

* ``preview`` (boolean, optional): Set to true to preview unpublished content (admin access required)

**Example Request:**

.. code-block:: bash

    GET /api/en/breadcrumbs/1/about/?preview=true

**Example Response:**

.. code-block:: json

    {
        "namespace": null,
        "title": "About Us",
        "url": "http://localhost:8080/en/about/",
        "api_endpoint": "http://localhost:8080/api/en/pages/about/",
        "visible": true,
        "selected": true,
        "attr": null,
        "level": 1,
        "children": []
    }
