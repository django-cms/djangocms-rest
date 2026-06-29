Preview and versioning
======================

The API serves published content to the public, but editors need to see work in progress.
This page explains the published/draft split, how a preview request switches between them,
and how access is controlled.

Published vs. draft content
---------------------------

When ``djangocms-versioning`` is in use, each ``PageContent`` can exist in more than one
state — typically a published version and a newer draft. django CMS exposes these through
two managers on the content model:

* the default (``content``) manager, which yields **published** content;
* an ``admin_manager``, which can yield **draft** content for editors.

djangocms-rest chooses between them per request. Normal requests read published content;
preview requests read draft content via the admin manager. This is also why placeholders
are decoupled from the page object (see :doc:`content-model`): the same placeholder slot
can resolve to different content depending on the version being viewed.

What a preview request does
---------------------------

A request is treated as preview when it carries a ``preview`` query parameter whose value
is anything other than ``0`` or ``false`` (so ``?preview``, ``?preview=true`` and
``?preview=1`` all enable it). When preview is active:

#. **Admin access is required.** An ``IsAdminUser`` check is applied first, so anonymous
   and non-staff users are rejected before any content is read.
#. **Per-object permissions still apply.** Even for staff, django CMS's
   ``user_can_view_page()`` decides whether *this* user may see *this* page. A failing
   check returns ``404`` — the API does not reveal the existence of content you cannot see.
#. **Draft content is read** through the admin manager instead of the published manager.

Preview propagates through links
--------------------------------

Preview is sticky across the links the API hands you. When you request a page in preview
mode, the ``details`` links to its placeholders and the ``api_endpoint`` links in menus
and breadcrumbs carry ``preview`` forward, so following them stays in draft context rather
than silently dropping back to published content.

Why session authentication
--------------------------

Preview authorisation reuses the editor's existing django CMS admin session rather than
introducing API tokens. The user who is allowed to edit in the admin is exactly the user
allowed to preview through the API, governed by the same permission rules — there is no
second, parallel access model to keep in sync. The practical consequence is that a
cross-origin frontend must send the session cookie, which is what the
:doc:`../how-to/access-preview-content` guide configures.

Placeholders already in draft
-----------------------------

When you fetch a placeholder that belongs to a draft object directly, the draft content is
already what is being queried, so adding ``?preview`` makes no further difference at that
step. Preview matters at the point where the API decides *which version* of a page's
content to resolve.

.. seealso::

   * :doc:`../how-to/access-preview-content` — the settings that make cross-origin preview work.
   * :doc:`content-model` — the page/placeholder decoupling that versioning relies on.
