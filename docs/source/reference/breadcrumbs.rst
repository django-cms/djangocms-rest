Breadcrumbs
===========

**Breadcrumb trails, mirroring django CMS's** ``{% show_breadcrumb %}``.

The breadcrumbs endpoints return the chain of ancestor pages leading to the current page —
for building breadcrumb navigation. The response is a **JSON array of navigation nodes**
(shape documented under :ref:`navigation-node`), ordered from the root down to the current
page. Unlike menus, the trail is flat: the nodes are the ancestors in order, not nested
under ``children``.

Parameters
----------

All breadcrumb endpoints accept the language prefix and the ``preview`` query parameter
(see :doc:`conventions`):

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Segment
     - Default
     - Meaning
   * - ``start_level``
     - ``0``
     - First ancestor level to include in the trail
   * - ``path``
     - current
     - Page path whose ancestor trail is returned

Only visible pages are included.

Endpoints
---------

.. list-table::
   :header-rows: 1
   :widths: 100

   * - Path
   * - ``/api/{language}/breadcrumbs/``
   * - ``/api/{language}/breadcrumbs/{path}/``
   * - ``/api/{language}/breadcrumbs/{start_level}/``
   * - ``/api/{language}/breadcrumbs/{start_level}/{path}/``

**Example request**

.. code-block:: bash

    GET /api/en/breadcrumbs/about/

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
        "children": []
      },
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
