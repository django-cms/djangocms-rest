Menu
====

**Navigation menus, mirroring the django CMS menu system.**

The menu endpoints return the same structure that django CMS's ``{% show_menu %}``
template tag produces, as JSON. Use them to build primary navigation, sitemaps and nested
menus in a decoupled frontend.

.. _navigation-node:

Navigation node
---------------

Every menu, :doc:`submenu <submenu>` and :doc:`breadcrumb <breadcrumbs>` endpoint returns
a **JSON array** of *navigation nodes*. Each node has the same shape:

* ``namespace`` — application namespace, or ``null``
* ``title`` — menu title of the page
* ``url`` — absolute frontend URL of the page, or ``null``
* ``api_endpoint`` — absolute API URL to fetch the page (carries ``preview`` when in
  preview mode), or ``null``
* ``visible`` — whether the node is shown in navigation
* ``selected`` — whether the node matches the requested ``path``
* ``attr`` — extra attributes (django CMS stores e.g. the page ``path`` here)
* ``level`` — depth in the menu tree (0-based)
* ``children`` — array of child navigation nodes (same shape, recursive)

.. note::

   Responses are **arrays**, even when a single root node is returned. Nested levels
   appear under each node's ``children``.

Parameters
----------

All menu endpoints accept the standard language prefix and the ``preview`` query parameter
(see :doc:`conventions`). The level/active controls map directly onto ``{% show_menu %}``
arguments and are optional — omitting a path segment uses its default.

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Segment
     - Default
     - Meaning
   * - ``from_level``
     - ``0``
     - First menu level to include
   * - ``to_level``
     - ``100``
     - Last menu level to include
   * - ``extra_inactive``
     - ``0``
     - Levels of inactive children to show
   * - ``extra_active``
     - ``1000``
     - Levels of active children to show
   * - ``root_id``
     - –
     - ``reverse_id`` of a page to use as the menu root
   * - ``path``
     - current
     - Page path used to determine the active/selected node

Endpoints
---------

The template equivalent of the full form is ``{% show_menu 0 100 100 100 %}``.

.. list-table::
   :header-rows: 1
   :widths: 60 40

   * - Path
     - Equivalent
   * - ``/api/{language}/menu/``
     - defaults for all controls
   * - ``/api/{language}/menu/{from_level}/{to_level}/{extra_inactive}/{extra_active}/``
     - explicit level controls
   * - ``/api/{language}/menu/{from_level}/{to_level}/{extra_inactive}/{extra_active}/{path}/``
     - level controls + active path
   * - ``/api/{language}/menu/{root_id}/{from_level}/{to_level}/{extra_inactive}/{extra_active}/``
     - rooted at ``root_id``
   * - ``/api/{language}/menu/{root_id}/{from_level}/{to_level}/{extra_inactive}/{extra_active}/{path}/``
     - rooted at ``root_id`` + active path

**Example request**

.. code-block:: bash

    GET /api/en/menu/

**Example response**

.. code-block:: json

    [
      {
        "namespace": null,
        "title": "Home",
        "url": "http://localhost:8080/en/",
        "api_endpoint": "http://localhost:8080/api/en/pages/",
        "visible": true,
        "selected": false,
        "attr": { "path": "" },
        "level": 0,
        "children": [
          {
            "namespace": null,
            "title": "About Us",
            "url": "http://localhost:8080/en/about/",
            "api_endpoint": "http://localhost:8080/api/en/pages/about/",
            "visible": true,
            "selected": false,
            "attr": { "path": "about" },
            "level": 1,
            "children": []
          }
        ]
      }
    ]

.. seealso::

   * :doc:`submenu` and :doc:`breadcrumbs` — same node shape, different scope.
   * `django CMS — navigation <https://docs.django-cms.org/en/latest/reference/navigation.html>`_
