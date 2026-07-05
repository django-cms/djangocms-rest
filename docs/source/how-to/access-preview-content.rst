Access draft (preview) content
==============================

By default the API serves only **published** content. Editors often need to preview
unpublished or draft changes in the frontend before they go live. This guide enables
authenticated preview access.

How preview works
-----------------

Add ``?preview=true`` (any value except ``0`` or ``false`` counts as enabled) to a page,
page-list, page-tree, placeholder, or menu request. When preview is requested:

* the request must come from an **authenticated admin user** (``is_staff``) — anonymous or
  non-staff preview requests are rejected;
* per-object visibility is still enforced through django CMS's ``user_can_view_page()``;
* the API reads draft content instead of published content.

.. code-block:: bash

    # Fails for anonymous users; returns draft content for a logged-in editor
    curl "http://localhost:8080/api/en/pages/?preview=true"

Authentication
--------------

djangocms-rest relies on Django's standard **session authentication**: the user logs in
through the django CMS admin, and the session cookie authorises preview requests. There is
no token endpoint.

For a frontend on a *different* origin to send that cookie, you must configure CORS, CSRF
and the cookies to work cross-site.

Steps
-----

1. Set up :doc:`CORS <configure-cors>` first, then allow credentialed requests:

   .. code-block:: python

       # settings.py
       CORS_ALLOW_CREDENTIALS = True

2. Trust your frontend origin for CSRF:

   .. code-block:: python

       CSRF_TRUSTED_ORIGINS = [
           "https://example.com",
           "http://localhost:5173",
       ]

3. Allow the session and CSRF cookies to travel cross-site. ``SameSite=None`` *requires*
   ``Secure``, so these settings imply HTTPS in production:

   .. code-block:: python

       SESSION_COOKIE_SAMESITE = "None"
       CSRF_COOKIE_SAMESITE = "None"
       SESSION_COOKIE_SECURE = True
       CSRF_COOKIE_SECURE = True

4. In the frontend, send credentials with each request:

   .. code-block:: javascript

       fetch("https://cms.example.com/api/en/pages/?preview=true", {
           credentials: "include",
       });

Verify
------

1. Log in to the django CMS admin at ``/admin/``.
2. Edit a page (e.g. change its title) but **do not publish**.
3. Request the page with ``?preview=true`` while authenticated — you should see the draft
   change; without it you see the published version.

.. note::

   When you fetch a placeholder that belongs to a draft object, ``?preview`` has no extra
   effect — the draft content is already what is being queried.

.. seealso::

   * :doc:`../explanation/preview-and-versioning` — published vs. draft, and how the
     permission check works.
   * `django CMS — authentication and permissions
     <https://docs.django-cms.org/en/latest/reference/configuration.html#cms-permission>`_
