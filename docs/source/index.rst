djangocms-rest
==============

.. image:: https://img.shields.io/pypi/v/djangocms-rest.svg?style=flat-square
   :target: https://pypi.python.org/pypi/djangocms-rest
   :alt: Latest PyPI version

.. image:: https://codecov.io/gh/django-cms/djangocms-rest/graph/badge.svg?token=RKQJL8L8BT
   :target: https://codecov.io/gh/django-cms/djangocms-rest
   :alt: Test coverage

.. image:: https://img.shields.io/pypi/pyversions/djangocms-rest.svg?style=flat-square
   :target: https://pypi.python.org/pypi/djangocms-rest
   :alt: Python versions

.. image:: https://img.shields.io/pypi/frameworkversions/django/djangocms-rest.svg?style=flat-square
   :target: https://pypi.python.org/pypi/djangocms-rest
   :alt: Django versions

.. image:: https://img.shields.io/pypi/frameworkversions/django-cms/djangocms-rest.svg?style=flat-square
   :target: https://pypi.python.org/pypi/djangocms-rest
   :alt: django CMS versions

.. image:: https://img.shields.io/github/license/django-cms/djangocms-rest.svg?style=flat-square
   :target: https://opensource.org/licenses/BSD-3-Clause
   :alt: License

*Headless content delivery for django CMS — serve your content as a typed, read-only REST API.*

**djangocms-rest** turns an existing `django CMS <https://www.django-cms.org/>`_ project
into a headless backend: editors keep the django CMS editing interface, while your frontend
consumes content as read-only JSON.

Key features
------------

**Zero-config**
    Every django CMS plugin serializes to JSON automatically — no API code to write.

**Editing stays put**
    Editors keep the full django CMS interface; the API is read-only.

**Complete content model**
    Pages, placeholders, plugins, menus, breadcrumbs and search — all over the API.

**Typed & standards-based**
    Optional `drf-spectacular <https://drf-spectacular.readthedocs.io/>`_ emits an OpenAPI 3
    schema and browsable docs for fully typed clients (React, Vue, Svelte, Astro, …).

**Multi-language & multi-site**
    Per-language endpoints and per-site content resolution out of the box.

**Built on DRF**
    Extend it with your own `Django REST framework <https://www.django-rest-framework.org/>`_
    serializers and permissions.

Where to start
--------------

:doc:`🚀 Tutorial <tutorial/index>`
    Start here. A single hands-on lesson that takes you from an empty project to fetching
    real page content over the API.

:doc:`🔧 How-to guides <how-to/index>`
    Goal-oriented recipes: enable CORS, serve multiple sites, access draft content,
    generate the OpenAPI schema, and serialize custom plugins.

:doc:`📖 Reference <reference/index>`
    Exact endpoint descriptions — paths, parameters, response fields and examples for
    every endpoint.

:doc:`💡 Explanation <explanation/index>`
    The concepts behind the API: the content model, preview & versioning, plugin
    serialization, multi-site, and caching.

.. note::

   New to headless django CMS? Read :doc:`explanation/headless` first to understand what
   you are building and why, then follow the :doc:`tutorial/index`.

.. toctree::
   :maxdepth: 2
   :hidden:

   tutorial/index
   how-to/index
   reference/index
   explanation/index
   contributing
   changelog
