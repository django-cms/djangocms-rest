Multi-site models
==================

django CMS can serve several sites from one project using the Django *sites* framework.
Headless delivery offers two ways to do that, with different trade-offs. This page compares
them so you can choose; the :doc:`../how-to/serve-multiple-sites` guide covers the setup.

The two approaches
------------------

**Multi-instance** — one deployment per site.
    Each site runs on its own domain, and the web server routes the domain to the right
    site, exactly as in a classic django CMS deployment. The API on each instance serves
    only that site's content.

    .. code-block:: text

        foo.example.com/api/pages/   →  Foo site content
        bar.example.com/api/pages/   →  Bar site content

**Single-instance** — one deployment, site chosen per request.
    One django CMS instance serves all sites. Because a decoupled frontend doesn't go
    through per-domain web-server routing, the client states which site it wants with an
    ``X-Site-ID`` request header, which ``SiteContextMiddleware`` resolves to a site.

    .. code-block:: text

        cms.example.com/api/pages/   X-Site-ID: 1  →  Foo site content
        cms.example.com/api/pages/   X-Site-ID: 2  →  Bar site content

How site scoping works
----------------------

Once the site is determined — from the domain (multi-instance) or the ``X-Site-ID`` header
(single-instance) — it scopes everything: page querysets are filtered by site, and the
languages endpoint reports the languages configured for *that* site. Sites therefore stay
isolated from each other in the API response regardless of which model you choose.

Choosing between them
---------------------

Single-instance is convenient when:

* the sites share content, plugins, editors and a release cadence;
* you want one deployment, one cache and one schema to operate;
* the frontend can reasonably decide and send a site id.

Multi-instance fits better when:

* sites must be strongly isolated (separate databases, scaling or release schedules);
* you prefer the familiar one-domain-one-site operational model;
* you don't want clients to be responsible for selecting a site.

A practical consequence of single-instance: because the site is a request header rather
than the origin, the browser must be allowed to send that header. That makes correct CORS
configuration part of the design, not an afterthought (see
:doc:`../how-to/configure-cors`).

.. seealso::

   * :doc:`../how-to/serve-multiple-sites` — configuring the single-instance model.
   * `Django — the sites framework
     <https://docs.djangoproject.com/en/stable/ref/contrib/sites/>`_
