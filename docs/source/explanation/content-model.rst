The content model
==================

Almost every endpoint in djangocms-rest is shaped by django CMS's underlying content
model. Understanding the four objects below — and the two-step fetch they imply — makes
the whole API predictable.

Pages, page content, placeholders, plugins
------------------------------------------

``Page``
    The structural node in the page tree. It is **language-neutral**: it holds the
    position in the hierarchy, the site, and flags like ``login_required``. A page on its
    own has no title — those live in its translations.

``PageContent``
    The translation of a page into one language. The title, menu title, meta description,
    template and navigation flags you see in a page response come from the ``PageContent``
    for the requested language. This is why every page endpoint is language-prefixed: you
    are really requesting a ``PageContent``.

``Placeholder``
    A named content region declared by the page's template (``content``, ``sidebar`` …).
    A placeholder is *linked to* a content object but is not part of it — which is what
    makes versioning and preview possible.

``Plugin``
    An item of content inside a placeholder (a text block, an image, a grid). Plugins form
    a tree: a plugin may contain child plugins.

A page response therefore exposes its placeholders, and each placeholder exposes a list of
serialized plugins.

Why content is fetched in two steps
-----------------------------------

Placeholders are deliberately decoupled from the page object. The API mirrors this with
two access patterns, chosen for performance:

* **Single-page endpoints** (:doc:`../reference/pages`, ``/pages/`` and ``/pages/{path}/``)
  embed each placeholder together with its fully serialized ``content``. One request gives
  you a page ready to render.
* **List and tree endpoints** (``/pages-list/``, ``/pages-tree/``) return page *metadata
  only*. Each placeholder is represented by a ``details`` link instead of its content, so
  building a navigation listing does not pay the cost of serializing every plugin on every
  page.

To get the content of a placeholder from a listing, you follow its ``details`` link to the
:doc:`placeholder endpoint <../reference/placeholders>`. This is the
*languages → page → placeholder content* loop from the :doc:`../tutorial/01-quickstart`.

Placeholder order is meaningful
-------------------------------

Placeholders are returned in the order they are **declared in the template**, not the
order they happen to exist in the database. A frontend can rely on that order to lay out a
page consistently.

Absolute URLs and the frontend
------------------------------

URLs in responses (``absolute_url``, ``details``, plugin links, menu ``api_endpoint``\ s)
are absolute, built from the current request's scheme and host. This keeps responses
usable directly by a frontend without URL reassembly. Two fields serve different needs:

* ``absolute_url`` — where the page lives for the end user (the frontend/site URL).
* ``details`` / ``api_endpoint`` — where to fetch that object's data from the API.

Identifying apphooked pages
---------------------------

A page attached to a Django application via an apphook reports a non-empty
``application_namespace``. The frontend can use it the way server-side django CMS uses
apphooks: to recognise that a subtree is owned by an application and route it accordingly.

.. seealso::

   * :doc:`../reference/pages` and :doc:`../reference/placeholders` — the exact fields.
   * :doc:`preview-and-versioning` — how the published/draft split rides on this model.
