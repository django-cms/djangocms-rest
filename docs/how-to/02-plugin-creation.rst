Plugin Creation & Serialization
================================

DjangoCMS REST provides basic support for all CMS plugins. This means that all plugins are automatically serialized into JSON data, without the need for any additional configuration.

For most simple use cases, this is all you need. However, when used in relation to other models, you might want to create a custom serializer.

.. note::
    This guide assumes you have a running Django CMS project and a basic understanding of Django CMS plugins. If you are not familiar with them, please refer to the `Django CMS documentation <https://docs.django-cms.org/en/latest/how_to/09-custom_plugins.html>`_.

Automatic Serialization
-----------------------

You can use the ``GenericPluginSerializer`` whenever no further application relationship is required. No additional configuration is required — simply create Django CMS plugins according to the documentation.

**Requirements:**

- No model fields needed
- Fields are directly available as model fields
- Fields are standard Django model fields

**Limitations:**

- Foreign keys are automatically resolved but not serialized.


Use Cases
~~~~~~~~~

- Layout plugins like Grid, Row, Column, etc.
- Content plugins like Text, Image, Video, etc.
- Content-Group plugins like Hero, CTAs, etc.

You can also nest plugins inside other plugins as you would normally do in Django CMS.

Example "Hello World"
~~~~~~~~~~~~~~~~~~~~~~

Create your plugin as you would normally do in Django CMS.

Even though we finally will render the plugin decoupled in the frontend, likely using json data in combination with a frontend framework (Vue.js, React, etc.). 
We still define a template for the plugin. This allows us to display the plugin in the django CMS backend for editing purposes and also to pass rendered HTML to the frontend.

Place your plugins in ``cms_plugins.py.`` For our example, include the following code:

.. code-block:: python

    # A simple example of a plugin that renders a static template.
    # No additional configuration is required for serialization.

    from cms.plugin_base import CMSPluginBase
    from cms.plugin_pool import plugin_pool
    from cms.models.pluginmodel import CMSPlugin
    from django.utils.translation import gettext_lazy as _

    @plugin_pool.register_plugin
    class HelloPlugin(CMSPluginBase):
        model = CMSPlugin
        render_template = "hello_world.html" # Adjust the path to your template.
..

Add the following into the root template directory in a file called ``hello_world.html``:

.. code-block:: html+django

    <h1>Hello World!</h1>
    <p>This is a simple example of a plugin that renders a static template.</p>
.. 

Now add this plugin to a placeholder in a page. 

Depending on your projects configuration, you might have to configure placeholders in the ``CMS_PLACEHOLDER_CONF`` setting. See the `Django CMS documentation <https://docs.django-cms.org/en/latest/reference/configuration.html#cms-placeholders>`_ for more information.

After adding the plugin to a placeholder, you can retrieve the content of the placeholder using the :doc:`Pages <../reference/pages>` and :doc:`Placeholders <../reference/placeholders>` endpoints.

.. note::
    First, we have to retrieve the page object, and then the associated placeholder objects. This is necessary because Django CMS placeholders are linked to, but not part of, the page object. This enables us to use preview mode and versioning.


.. code-block:: bash

    # Get page details for a specific page
    #replace language code and the path with your page path.
    curl -X GET "http://localhost:8080/api/en/pages/my-page-with-hello-world-plugin/" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
..

**Response from the pages endpoint:**

.. code-block:: json

    "...",
    "placeholders": [
    {
        "content_type_id": 5,
        "object_id": 9,
        "slot": "content",
        "details": "http://localhost:8080/api/en/placeholders/5/9/content/"
    }
    ],
    "...",
..

.. code-block:: bash

    # Get placeholder content for a specific placeholder
    # replace query with parameters from the response of the pages endpoint.
    curl -X GET "http://localhost:8080/api/en/placeholders/5/9/content/?html=1" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
..

.. note::
    ?html=1 will render plugins as HTML.


**Response from the placeholders endpoint:**

.. code-block:: json

    {
        "slot": "content",
        "label": "Content",
        "language": "en",
        "content": [
            {
                "plugin_type": "HelloPlugin"
            }
        ],
        "html": "<h1>Hello World!</h1>\n<p>This is a simple example of a plugin that renders a static template.</p>"
    }

..

As you can see, the content is serialized as a list of plugins. Each plugin has a ``plugin_type`` that helps identify and render the plugin correctly on the frontend.

In the above example, we would simply render the HTML in the frontend.

You can retrieve all plugin details using the :doc:`Plugins <../reference/plugins>` endpoint.

.. hint::
    You can setup a vue.js frontend application to handle the rendering of json data. Follow the guide `Setup Vue.js Project <01-use-multi-site.html#setup-vue-js-project>`_ to get started.

Example "Basic Serialization"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The previous example had no data to serialize, beside the generic plugin properties. Now we will create a plugin that has some actual data to serialize.

Create a new model ``HeroPluginModel`` in ``models.py``, which will be used to store the data for the plugin.

In this example we will create a plugin that displays a hero image with a title, description and a link to an existing django CMS page.

.. code-block:: python

    # models.py
    from cms.models.fields import PageField
    from django.db import models
    from cms.models import CMSPlugin

    class HeroPluginModel(CMSPlugin):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='hero_images')
    link = PageField(blank=True, null=True)
    link_text = models.CharField(max_length=200, blank=True, null=True)

    def __unicode__(self):
        return self.title
..

We now have to run migrations when creating new models.

.. code-block:: bash

    # using app name is optional, but recommended.
    python manage.py makemigrations <your_app_name> 
    python manage.py migrate <your_app_name>
..

We now need to configure the plugin in ``cms_plugins.py``.

.. code-block:: python

    # cms_plugins.py
    @plugin_pool.register_plugin
    class HeroPlugin(CMSPluginBase):
        model = HeroPluginModel
        render_template = "my_app/hero_plugin.html"
        name = _("Hero Plugin")

..
    
To be sure changes are applied, you can restart the development server.

.. code-block:: bash

    python manage.py runserver 8080
..

Add the plugin to a placeholder in a page.

Fetch the content of the placeholder using the :doc:`Placeholders <../reference/placeholders>` endpoint. See `Example "Hello World" <02-plugin-creation.html#example-hello-world>`_.

**Response from the placeholders endpoint:**

.. code-block:: json

    {
        "slot": "content",
        "label": "Content",
        "language": "en",
        "content": [
            {
                "plugin_type": "HeroPlugin",
                "title": "A custom page hero",
                "description": "We can add some important teaser content.",
                "image": "http://localhost:8080/media/hero_images/demo.png",
                "link_text": "Read more",
                "link": "http://localhost:8080/api/en/pages/unterseite/"
            }
        ],
        "html": ""
    }

You have received the serialized data for the plugin. You can now render the plugin in the front end, likely using a matching component for the HeroPlugin that references the set properties.

.. hint::
    If you want to use the actual frontend URL, you can either create a custom serializer or create a utility function in your frontend to generate the required URL.

Type Definitions
~~~~~~~~~~~~~~~~

Type definitions are used to define the structure of the data that is returned by the API. They are used to validate the data in the frontend application.

You can retrieve the type definition for the plugin using the :doc:`Plugins <../reference/plugins>` endpoint.

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/plugins/" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
..

**Response from the plugins endpoint:**

.. code-block:: json

    {
        "plugin_type": "HeroPlugin",
        "title": "Hero Plugin",
        "type": "object",
        "properties": {
            "plugin_type": {
                "type": "string"
            },
            "title": {
                "type": "string"
            },
            "description": {
                "type": "string"
            },
            "image": {
                "type": "string",
                "format": "uri"
            },
            "link_text": {
                "type": "string"
            },
            "link": {
                "type": "integer"
            }
        }
    }

..

.. hint::
    You can automatically generate type-safe schemas for your typescript frontend application using tools like `QuickType <https://quicktype.io/typescript>`_ or `heyapi.dev <https://heyapi.dev/>`_ which integrates with `Zod <https://zod.dev/>`_ schema validation.


Custom Serialization
---------------------

...coming soon...

