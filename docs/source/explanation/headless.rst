Headless django CMS
===================

This page explains what "headless" means for django CMS, what djangocms-rest does and
does not take responsibility for, and the consequences of decoupling the frontend.

What headless means here
------------------------

A traditional django CMS project renders HTML on the server using templates. *Headless*
means the CMS becomes a backend-only content service: it exposes content through an API,
and a separate frontend — built with any framework — fetches that content and decides how
to present it.

djangocms-rest is the API layer. It does **not** replace django CMS; it sits on top of an
ordinary django CMS installation:

* Editors keep the full django CMS editing experience — the page tree, placeholders,
  plugins, versioning and permissions are all unchanged.
* The frontend consumes pages, placeholders, plugins, menus and breadcrumbs as JSON.
* The API is **read-only**. Content is created and edited in django CMS, not through the
  API.

Why decouple
------------

* Use any frontend stack — React, Vue, Svelte, Angular, Next.js, Nuxt, Astro, and so on.
* Deliver the same content to multiple channels (web, native apps, kiosks) from one source.
* Deploy frontend and backend independently; content changes propagate without a frontend
  redeploy.

If you already run django CMS, going headless does not mean adopting a new content
platform — it means putting an API in front of the one you have.

Where the boundary sits
-----------------------

Decoupling moves real responsibilities to the frontend. Knowing where the API stops
prevents surprises:

* **Rendering is yours.** The API returns structured content; turning a ``HeroPlugin``
  object into markup is the frontend's job. You can opt into server-rendered HTML per
  placeholder with ``?html=1`` (using your plugin templates) as a bridge, but that is a
  convenience, not the primary model.
* **Routing is yours.** The API tells you a page's ``path`` and ``absolute_url`` and gives
  menu/breadcrumb structures, but mapping URLs to frontend views is your router's job.
* **Apphooks are yours.** django CMS apphooks attach Django apps to pages. The API exposes
  a page's ``application_namespace`` so the frontend can recognise an apphooked page, but
  the application's own logic and routes must be reimplemented (or served by a separate
  API) in the frontend.

Editing and preview in a decoupled world
----------------------------------------

Even headless, django CMS's editing UI keeps working:

* Content can be rendered as JSON in both edit and preview modes. This is controlled by
  the ``REST_JSON_RENDERING`` setting, which defaults to "on" when the project has no
  classic ``CMS_TEMPLATES`` (i.e. a headless install).
* Editors can preview unpublished content through the API — see
  :doc:`preview-and-versioning` and the how-to on :doc:`../how-to/access-preview-content`.
* The decoupled frontend can be embedded back into django CMS (e.g. via an iframe) so
  editors use *Structure mode* to edit content in place.

Content without pages
----------------------

Not every project is page-shaped. If you only need a fixed set of content regions, django
CMS *aliases* (the ``djangocms-aliases`` package) let you define placeholders that are not
attached to any page; djangocms-rest exposes their content through the same placeholder
mechanism.

.. seealso::

   * :doc:`content-model` — how pages, placeholders and plugins fit together.
   * :doc:`plugin-serialization` — how plugin content becomes JSON.
