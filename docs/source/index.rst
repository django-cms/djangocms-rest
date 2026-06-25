djangocms-rest
==============

.. image:: https://img.shields.io/badge/python-3.10+-blue.svg
   :target: https://www.python.org/downloads/
   :alt: Python version

.. image:: https://img.shields.io/badge/Django-4.2+-green.svg
   :target: https://www.djangoproject.com/
   :alt: Django version

.. image:: https://img.shields.io/badge/django--cms-5.0+-orange.svg
   :target: https://www.django-cms.org/
   :alt: django CMS version

.. image:: https://img.shields.io/badge/license-BSD%203--Clause-blue.svg
   :target: https://opensource.org/licenses/BSD-3-Clause
   :alt: License

*Headless content delivery for django CMS — serve your content as a typed, read-only REST API.*

**djangocms-rest** turns an existing `django CMS <https://www.django-cms.org/>`_ project
into a headless backend. Editors keep the familiar django CMS editing interface; your
frontend consumes pages, placeholders, plugins, menus and breadcrumbs as JSON over a
read-only REST API.

It is built on the `Django REST framework <https://www.django-rest-framework.org/>`_ and,
together with `drf-spectacular <https://drf-spectacular.readthedocs.io/>`_, produces an
OpenAPI 3 schema and a browsable API — so you can generate fully typed clients for React,
Vue, Svelte, Astro, or any other framework.

Where to start
--------------

The documentation is organised along the four needs you have at different times.

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
