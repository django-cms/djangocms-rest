Extending the headless API
==========================

djangocms-rest exposes Django CMS content through a read-only REST API. Out of
the box it serves pages, placeholders, plugins, menus and breadcrumbs. Most
third-party apps, however, also want to publish **their own** data through the
same API — a reusable content library, a blog, a product catalogue.

This page explains the two contracts djangocms-rest offers for that, when to use
each, and how they map onto the Django CMS mechanisms you already know.

.. note::
    Serializing a plugin's *own* fields is a separate, already-solved concern —
    a plugin may declare a ``serializer_class``. See
    :doc:`../how-to/02-plugin-creation`. This page is about contributing
    **endpoints**, not plugin payloads.


Two shapes of extension
-----------------------

Third-party endpoints come in two shapes, and djangocms-rest deliberately keeps
them separate because they answer different questions:

.. list-table::
   :header-rows: 1
   :widths: 22 39 39

   * -
     - Independent endpoints
     - Apphook endpoints
   * - Example
     - ``djangocms-alias``
     - ``djangocms-stories``
   * - Relation to pages
     - None — content addressed by id
     - Mounted into the page tree via an apphook
   * - URL
     - Flat and global, e.g. ``/api/<lang>/aliases/<pk>/``
     - Path-driven by where the editor attached the apphook, e.g.
       ``/api/<lang>/blog/posts/``
   * - Number of mounts
     - One, global
     - Zero or many, each at its own page path
   * - Django CMS idiom
     - ``cms_config`` (``CMSAppExtension``)
     - apphook (``CMSApp``)

Pick the contract that matches how your content relates to pages. If the content
exists independently of the page tree, use the **cms_config** contract. If it is
browsed *within* the page tree — the app is hooked onto a page — use the
**apphook** contract.

In both contracts the language is always an explicit ``<slug:language>``
segment in the URL, exactly like every other endpoint in the API. Your views
receive ``language`` as an ordinary keyword argument.


Independent endpoints (cms_config)
----------------------------------

This is the right contract for content that is *not* part of the page tree —
reusable snippets, a media library, anything addressed by its own identifier.

djangocms-rest provides a ``CMSAppExtension``. Your app opts in from its own
``cms_config.py`` by setting ``djangocms_rest_enabled = True`` and declaring
``cms_rest_endpoints`` — a list of URL patterns that are mounted under the API
root. Declare the patterns exactly as you would in any ``urls.py``, **including
the** ``<slug:language>/`` **prefix** when your content is language-specific
(alias placeholders are):

.. code-block:: python

    # djangocms_alias/cms_config.py
    from django.urls import path

    from cms.app_base import CMSAppConfig

    from .rest_views import AliasContentView


    class AliasCMSConfig(CMSAppConfig):
        djangocms_rest_enabled = True
        cms_rest_endpoints = [
            path(
                "<slug:language>/aliases/<int:pk>/",
                AliasContentView.as_view(),
                name="alias-detail",
            ),
        ]

That is all. Django CMS already autodiscovers every installed app's
``cms_config.py``, so there is nothing to register in settings. djangocms-rest
collects the declared patterns and mounts them under the API root:

.. code-block:: text

    GET /api/en/aliases/42/

The views are ordinary Django REST framework views; they appear in the OpenAPI
schema automatically.

.. tip::
    A plugin that references your model — an ``AliasPlugin`` pointing at an
    ``Alias`` — is linked automatically. ``serialize_fk`` resolves any related
    model that exposes a ``get_api_endpoint()`` method (or a DRF-style
    ``<model>-detail`` route) to its API URL, so the plugin payload carries a
    link to ``/api/en/aliases/42/`` with no extra work.


Apphook endpoints (path-mirrored)
---------------------------------

This is the right contract for content that is browsed *within* the page tree.
A blog is the canonical example: the editor attaches the "Stories" apphook to a
page, and from then on the blog lives under that page's path. The headless API
mirrors this: the app's REST endpoints are mounted at **the same page path** the
editor chose.

There is no new base class and no interface to implement. djangocms-rest simply
checks whether your apphook offers an optional ``get_rest_urls()`` method,
mirroring the ``get_urls()`` it already uses for the HTML side:

.. code-block:: python

    # djangocms_stories/cms_apps.py
    from cms.app_base import CMSApp
    from cms.apphook_pool import apphook_pool


    @apphook_pool.register
    class StoriesApphook(CMSApp):
        name = "Stories"
        app_name = "stories"

        def get_urls(self, page=None, language=None, **kwargs):
            return ["djangocms_stories.urls"]        # HTML routes

        def get_rest_urls(self, page=None, language=None, **kwargs):
            return ["djangocms_stories.rest_urls"]   # REST routes (optional)

The referenced urlconf is an ordinary DRF urlconf. Do **not** add a language
prefix — djangocms-rest mounts your patterns below a language-capturing prefix
and the page path, so ``language`` arrives as a keyword argument:

.. code-block:: python

    # djangocms_stories/rest_urls.py
    from django.urls import path

    from .rest_views import PostListView, PostDetailView

    urlpatterns = [
        path("posts/", PostListView.as_view(), name="post-list"),
        path("posts/<slug:slug>/", PostDetailView.as_view(), name="post-detail"),
    ]

If the editor mounts the apphook on a page whose path is ``blog``, the endpoints
become:

.. code-block:: text

    GET /api/en/blog/posts/
    GET /api/en/blog/posts/my-first-post/

Because the mount mirrors the page path, the same apphook can be attached to
several pages, each with its own ``application_namespace``, and each gets its
own set of endpoints. Page paths are localized, so the German mount of the same
blog appears under the German path (for example ``/api/de/aktuelles/posts/``).

.. note::
    The endpoints are rebuilt whenever Django CMS reloads its URL configuration
    — the same reload it already triggers when an apphook page is added, moved
    or removed. You do not need to restart anything during editing.


Discovering an apphook from a page
----------------------------------

A frontend that fetches a page needs to know whether it is an apphook mount and,
if so, where the app's API lives. The page serializer answers this with an
``app`` block whenever the page carries a REST-capable apphook:

.. code-block:: json

    {
        "title": "Blog",
        "path": "blog",
        "application_namespace": "stories",
        "app": {
            "namespace": "stories",
            "api_endpoint": "https://example.com/api/en/blog/"
        }
    }

``api_endpoint`` is the path-mirrored root of the apphook's REST urls. The
frontend appends the sub-resources it knows about (``posts/`` and so on). Pages
without an apphook — or with an apphook that does not implement
``get_rest_urls()`` — omit the ``app`` block (it is ``null``).


Choosing between the two
------------------------

- The content is **reusable and not tied to a page** (a library, a catalogue,
  settings): use the **cms_config** contract.
- The content is **browsed inside the page tree**, mounted by an editor onto a
  page: use the **apphook** contract.

An app may use both. ``djangocms-alias`` could expose its alias library through
cms_config *and* ship an apphook for a browsable archive — the two contracts are
independent and compose freely.
