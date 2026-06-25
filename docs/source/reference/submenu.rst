Submenu
=======

**Submenus relative to the current page, mirroring django CMS's** ``{% show_sub_menu %}``.

Submenu endpoints return the part of the navigation tree below a given node — ideal for
dropdowns, sidebar and contextual menus. The response is a **JSON array of navigation
nodes** with exactly the shape documented under :ref:`navigation-node`.

Parameters
----------

All submenu endpoints accept the language prefix and the ``preview`` query parameter (see
:doc:`conventions`). The path segments are optional and map onto ``{% show_sub_menu %}``
arguments:

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Segment
     - Default
     - Meaning
   * - ``levels``
     - ``100``
     - How many levels deep to descend
   * - ``root_level``
     - –
     - Level at which the submenu root is fixed
   * - ``nephews``
     - ``100``
     - How many levels of "nephew" nodes to include
   * - ``path``
     - current
     - Page path the submenu is relative to

Endpoints
---------

The template equivalent of the root form is ``{% show_sub_menu 1 %}``.

.. list-table::
   :header-rows: 1
   :widths: 100

   * - Path
   * - ``/api/{language}/submenu/``
   * - ``/api/{language}/submenu/{levels}/``
   * - ``/api/{language}/submenu/{levels}/{path}/``
   * - ``/api/{language}/submenu/{levels}/{root_level}/``
   * - ``/api/{language}/submenu/{levels}/{root_level}/{path}/``
   * - ``/api/{language}/submenu/{levels}/{root_level}/{nephews}/``
   * - ``/api/{language}/submenu/{levels}/{root_level}/{nephews}/{path}/``
   * - ``/api/{language}/submenu/{path}/``

**Example request**

.. code-block:: bash

    GET /api/en/submenu/2/about/

**Example response**

.. code-block:: json

    [
      {
        "namespace": null,
        "title": "About Us",
        "url": "http://localhost:8080/en/about/",
        "api_endpoint": "http://localhost:8080/api/en/pages/about/",
        "visible": true,
        "selected": true,
        "attr": { "path": "about" },
        "level": 1,
        "children": []
      }
    ]

.. seealso::

   :doc:`menu` for the full node-field reference and the navigation concepts.
