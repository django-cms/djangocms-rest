Multi-Site setup with single CMS instance
=========================================

In this short guide, we will show you how to use the multi-site functionality in your frontend app.

We will use ``vue.js``  to fetch data from a single django CMS instance with multiple sites. This implementation
guide can easily be adapted to other frontend frameworks.

.. warning::
    This guide assumes you have a running Django CMS project with multiple sites.
    If you haven't configured django CMS for multi-site yet, please follow the `Multi-Site Support <../tutorial/02-installation.html#multi-site-support>`_ guide.



Setup Django CMS for Multi-Site
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


1. Start your django CMS project

.. code-block:: bash

    python manage.py runserver localhost:8080


2. Adjust the primary site details in django admin for site A (Site ID 1)
3. Create a new site in django admin for site B (Site ID 2)
4. Create a nested pages structure for site A and site B using django CMS page tree admin.
5. Before building the frontend we want to make sure the page tree is working and returned as expected.


.. code-block:: bash

    # Fetch the page tree for site A
    curl -v -H "X-Site-ID: 1" \
        -H "Content-Type: application/json" \
        -H "Accept: application/json" \
        http://localhost:8080/api/en/pages-tree/

**Response**

You should get your page tree for each site as a response described in the :doc:`../reference/pages` reference.


.. hint::
    Alternatively you can use swagger (see :doc:`../tutorial/02-installation`) to test the API endpoints or a app like `Bruno <https://www.usebruno.com/>`_


CMS Reference
~~~~~~~~~~~~~

- `Django CMS User Docs - Pages <https://user-guide.django-cms.org/en/latest/tutorial/05-pagetree.html>`_



Enable CORS
~~~~~~~~~~~

This works fine from console, but for browser requests we have to ensure that ``CORS`` (Cross-Origin Resource Sharing) is configured correctly.
See the `CORS Support <../tutorial/02-installation.html#cors-support>`_ guide for more information.





Setup Vue.js Project
~~~~~~~~~~~~~~~~~~~~

Before continuing, you should set up a basic Vue.js project.

- `Vue.js Quick Start <https://vuejs.org/guide/quick-start>`_

.. note::

    We use TypeScript for this example. Make sure to enable it in your Vue.js project.

    ✔ Add TypeScript? … **Yes**


Now we will create a simple Vue.js project to fetch the page tree using the ``X-Site-ID`` request header:

Replace the content of ``App.vue`` with the following code:

.. code-block:: vue

    <script setup lang="ts">
    import { ref } from 'vue';

    const siteId = ref('1');
    const data = ref(null);
    const error = ref(null);
    const errorCode = ref(null);

    async function fetchData() {
        error.value = null;
        errorCode.value = null;
        try {
            const response = await fetch('http://localhost:8080/api/en/pages-tree/', {
                headers: { 'X-Site-ID': siteId.value }
            });
            if (!response.ok) {
                error.value = `HTTP error: ${response.statusText}`;
                errorCode.value = response.status;
                data.value = null;
                return;
            }
            data.value = await response.json();
        } catch (err) {
            error.value = err.message || 'Unknown error';
            errorCode.value = err.code || null;
            data.value = null;
        }
    }
    </script>

    <template>
    <select v-model="siteId" @change="fetchData">
        <option value="1">Site 1</option>
        <option value="2">Site 2</option>
    </select>
    <button @click="fetchData">Fetch Page Tree</button>
    <pre v-if="data">{{ data }}</pre>
    <div v-if="error" style="color: red;">
        Error: {{ error }}<br>
        <span v-if="errorCode">Error Code: {{ errorCode }}</span>
    </div>
    </template>


Testing
~~~~~~~

Run your Vue.js project:

.. code-block:: bash

    npm run dev


Visit `http://localhost:5173/ <http://localhost:5173/>`_ in your browser, assuming you are using the default port for Vue.js.

You can now click the ``"Fetch Page Tree"`` button to fetch the page tree for the selected site.

.. admonition:: Success

    You should see the page tree for the selected site in the browser.
    See the :doc:`../reference/pages` documentation for the expected response.


.. error::

    if you get error you likely forgot to set the ``X-Site-ID`` header as allowed in the CORS settings or the domain or port is not allowed in the CORS settings.
    See the :doc:`../tutorial/02-installation` guide for more information.

Start Building
~~~~~~~~~~~~~~

When you are able to fetch the page tree for each site you can start building your frontend app.

- Configure Django CMS templates with varous placeholders options
- Define and customize plugins according to your needs
- Add authentication to your frontend app, which allows content preview in the frontend app
