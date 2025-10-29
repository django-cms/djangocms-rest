Menu Endpoints
==============

**The Menu endpoints provide navigation nodes using the same structure as the django CMS menu system.**

.. note::

    The endpoints follow the same structure as the menu in a template. Please refer to the documentation for more details.
    
    ``{% show_menu 0 100 100 100 %}``

    ``GET /api/{language}/menu/0/100/100/100/``

    

* Menu endpoints are essential for building navigation menus and sitemaps
* Menu information includes page meta information, state, URLs, visibility settings, and hierarchical relationships
* Retrieve menu nodes and filter by:
* * by level ranges
* * by root ID
* * by level range  
* * active/inactive states, 
* * specific paths


CMS Reference
-------------

- `User site navigation <https://docs.django-cms.org/en/stable/reference/navigation.html>`_
- `Customizing the Menu <https://docs.django-cms.org/en/latest/how_to/14-menus.html#>`_
- `Menu Developer Reference <https://docs.django-cms.org/en/latest/reference/navigation.html#cms-menus>`_

Endpoints
---------

List Menu
~~~~~~~~~

**GET** ``/api/{language}/menu/``

Get the complete menu structure for a specific language.

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

    GET /api/en/menu/?preview=true

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
                "selected": false,
                "attr": null,
                "level": 1,
                "children": []
            }
        ]
    }

List Menu by Level Range
~~~~~~~~~~~~~~~~~~~~~~~~

**GET** ``/api/{language}/menu/{from_level}/{to_level}/{extra_inactive}/{extra_active}/``

Get the menu structure filtered by level range and active/inactive states.

**Path Parameters:**

* ``language`` (string, required): Language code (e.g., "en", "de")
* ``from_level`` (integer, required): Starting level for menu items
* ``to_level`` (integer, required): Ending level for menu items
* ``extra_inactive`` (integer, required): Number of extra inactive items to include
* ``extra_active`` (integer, required): Number of extra active items to include

**Query Parameters:**

* ``preview`` (boolean, optional): Set to true to preview unpublished content (admin access required)

**Example Request:**

.. code-block:: bash

    GET /api/en/menu/0/2/1/1/?preview=true

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
                "selected": false,
                "attr": null,
                "level": 1,
                "children": []
            }
        ]
    }

List Menu by Level Range and Path
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**GET** ``/api/{language}/menu/{from_level}/{to_level}/{extra_inactive}/{extra_active}/{path}/``

Get the menu structure filtered by level range, active/inactive states, and specific path.

**Path Parameters:**

* ``language`` (string, required): Language code (e.g., "en", "de")
* ``from_level`` (integer, required): Starting level for menu items
* ``to_level`` (integer, required): Ending level for menu items
* ``extra_inactive`` (integer, required): Number of extra inactive items to include
* ``extra_active`` (integer, required): Number of extra active items to include
* ``path`` (string, required): Path as starting node for the menu

**Query Parameters:**

* ``preview`` (boolean, optional): Set to true to preview unpublished content (admin access required)

**Example Request:**

.. code-block:: bash

    GET /api/en/menu/0/2/1/1/about/?preview=true

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

List Menu by Root ID and Level Range
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**GET** ``/api/{language}/menu/{root_id}/{from_level}/{to_level}/{extra_inactive}/{extra_active}/{path}/``

Get the menu structure filtered by root ID, level range, active/inactive states, and specific path.

**Path Parameters:**

* ``language`` (string, required): Language code (e.g., "en", "de")
* ``root_id`` (string, required): Root ID to start the menu from
* ``from_level`` (integer, required): Starting level for menu items
* ``to_level`` (integer, required): Ending level for menu items
* ``extra_inactive`` (integer, required): Number of extra inactive items to include
* ``extra_active`` (integer, required): Number of extra active items to include
* ``path`` (string, required): Path as starting node for the menu

**Query Parameters:**

* ``preview`` (boolean, optional): Set to true to preview unpublished content (admin access required)

**Example Request:**

.. code-block:: bash

    GET /api/en/menu/1/0/2/1/1/about/?preview=true

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