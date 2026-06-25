Plugin serialization
=====================

Plugins are where django CMS content actually lives, and turning an arbitrary plugin into
clean JSON is the most subtle part of the API. This page explains how serialization works,
how references to other objects are resolved, and how the typed plugin definitions are
produced.

The default: a generic model serializer
---------------------------------------

When a plugin does not declare its own serializer, djangocms-rest builds one on the fly: a
DRF ``ModelSerializer`` over the plugin's model. This is why "every plugin just works" — a
new plugin needs no API code at all.

The generated serializer excludes django CMS's internal bookkeeping fields so they don't
clutter the payload: ``placeholder``, ``language``, ``position``, ``creation_date``,
``changed_date`` and ``parent``. Everything else on the model is serialized by name. A
``parent_plugin_type`` field is added so the frontend can reason about nesting context.

A plugin can override this entirely by setting a ``serializer_class`` — see the how-to on
:doc:`../how-to/serialize-plugins`. The same class is used both to serialize live content
and to describe the plugin's type (below), so a custom serializer improves the payload and
the generated client types together.

Resolving references to other objects
--------------------------------------

A plugin field rarely wants to expose a raw database id. When a plugin field references
another model (a foreign key, or a "soft" reference embedded in rich text), djangocms-rest
tries to turn it into something the frontend can use, in this order:

#. **``get_api_endpoint()``** — if the related model defines this method, its result is
   used. django CMS ``Page`` objects get one automatically (resolving to the page's API
   URL), and ``filer`` files get one that returns the file URL when the file is public.
#. **A DRF detail route** — otherwise the API tries to reverse ``<model_name>-detail`` for
   the object's primary key, picking up any DRF endpoint you have registered for that model.
#. **A stable fallback string** — if neither works, the reference is returned as
   ``"<app_label>.<model_name>:<pk>"`` (for example ``"cms.page:2"``). The frontend can
   parse this to resolve the object itself.

This layered approach means links degrade gracefully: a frontend always receives
*something* it can act on, and you can improve resolution later by adding a
``get_api_endpoint()`` or a DRF route without changing plugin code.

Soft references inside rich content
-----------------------------------

Rich text and link plugins embed references that aren't plain model fields — links to
pages, links to files, and inline ``data-cms-href`` attributes. The serializer walks JSON
field values recursively and rewrites these soft references using the same resolution
rules above, so a link to a CMS page inside a block of rich text comes out as a usable API
endpoint rather than an internal identifier.

Rich text: HTML and structured JSON
-----------------------------------

With ``djangocms-text`` installed, a text plugin exposes **both** representations: an HTML
``body`` and a structured ``json`` document (plus an ``rte`` marker identifying the
editor, e.g. ``tiptap``). A frontend can render the HTML directly or consume the
structured JSON to build its own components — and any links inside are resolved as
described above.

Nested plugins
--------------

Because plugins form a tree, serialization is recursive. A plugin that has children
carries them under a ``children`` array, mirroring the structure board. This lets layout
plugins (grids, rows, columns) and content-group plugins (heroes, cards) serialize their
contents in place.

The plugin definitions endpoint
--------------------------------

Plugin payloads are dynamic, so their detailed shape cannot be fully captured by the
static OpenAPI schema. The ``/api/plugins/`` endpoint fills this gap: for every
registered plugin it returns a JSON-schema-style description derived from the plugin's
serializer fields — mapping DRF field types to JSON types and formats (``CharField`` →
``string``, ``ImageField`` → ``string``/``uri``, choices → ``enum``, and so on).

This is what makes fully typed frontends possible: client generators read these
definitions to produce accurate plugin types. The richer the serializer (especially a
custom ``serializer_class`` with explicit fields and help text), the richer the generated
types.

Limits to be aware of
---------------------

* The automatic serializer resolves foreign keys but does not expand them into nested
  objects — you get a link or identifier, not the full related record. Use a custom
  ``serializer_class`` if you need an embedded object.
* Plugins whose models can't be introspected cleanly are skipped in the definitions
  endpoint rather than producing a broken schema. Declaring a ``serializer_class`` is the
  way to guarantee a precise definition.

.. seealso::

   * :doc:`../how-to/serialize-plugins` — the practical recipes.
   * :doc:`../reference/index` — the endpoint catalogue (and the live schema it points to).
