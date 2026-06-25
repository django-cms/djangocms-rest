Serve multiple sites from one instance
======================================

django CMS can host several sites (via the Django *sites* framework) in a single project.
In a classic setup the web server routes each domain to the right site. A decoupled
frontend has no such routing, so djangocms-rest lets the client pick the site explicitly
with an ``X-Site-ID`` request header, resolved by ``SiteContextMiddleware``.

For the trade-offs between this single-instance approach and running one instance per
site, see :doc:`../explanation/multi-site`.

Steps
-----

1. Enable the sites framework and set a default site:

   .. code-block:: python

       # settings.py
       INSTALLED_APPS = [
           # ...
           "django.contrib.sites",
       ]

       SITE_ID = 1

2. Add ``SiteContextMiddleware``. Place it *after* ``CorsMiddleware`` but before
   middleware that depends on the resolved site:

   .. code-block:: python

       MIDDLEWARE = [
           "corsheaders.middleware.CorsMiddleware",
           "djangocms_rest.middleware.SiteContextMiddleware",
           # ... the rest of your middleware
       ]

   The middleware reads ``X-Site-ID`` from the request. If the header is absent it falls
   back to the current site; an invalid value returns ``400`` and an unknown site ``404``.

3. Allow the header through CORS so browsers may send it (see :doc:`configure-cors`):

   .. code-block:: python

       from corsheaders.defaults import default_headers

       CORS_ALLOW_HEADERS = (*default_headers, "X-Site-ID")

4. Create your sites in **Django admin → Sites**, giving each a domain and name. Note each
   site's ID (visible in the admin URL while editing) — that is the value clients send.

Verify
------

Request the same endpoint for two different sites and confirm you get different content:

.. code-block:: bash

    curl -H "X-Site-ID: 1" http://localhost:8080/api/en/pages-tree/
    curl -H "X-Site-ID: 2" http://localhost:8080/api/en/pages-tree/

Each response is scoped to that site: pages, menus and languages are all filtered by it.

Consume it from a frontend
--------------------------

Send the header with every request. A minimal Vue example that switches between sites:

.. code-block:: vue

    <script setup lang="ts">
    import { ref } from "vue";

    const siteId = ref("1");
    const data = ref(null);

    async function fetchTree() {
        const res = await fetch("http://localhost:8080/api/en/pages-tree/", {
            headers: { "X-Site-ID": siteId.value },
        });
        data.value = res.ok ? await res.json() : { error: res.status };
    }
    </script>

    <template>
      <select v-model="siteId" @change="fetchTree">
        <option value="1">Site 1</option>
        <option value="2">Site 2</option>
      </select>
      <button @click="fetchTree">Fetch page tree</button>
      <pre v-if="data">{{ data }}</pre>
    </template>

If the request fails in the browser but works from ``curl``, the cause is almost always
CORS — confirm both the origin and the ``X-Site-ID`` header are allowed.

.. seealso::

   * :doc:`../explanation/multi-site` — single-instance vs. multi-instance, and the trade-offs.
   * `Django — the sites framework
     <https://docs.djangoproject.com/en/stable/ref/contrib/sites/>`_
