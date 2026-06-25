Serialize plugins (default and custom)
======================================

Every django CMS plugin is serialized to JSON automatically — no configuration required.
This guide shows the default behaviour, then how to take control with a custom serializer
when you need a specific shape or fully typed output.

For *why* it works this way (foreign-key resolution, rich-text JSON, the plugin
definitions endpoint), see :doc:`../explanation/plugin-serialization`.

Default: automatic serialization
--------------------------------

Create plugins exactly as you would in any django CMS project. Their model fields are
serialized for you. A plugin with no extra fields still serializes its type:

.. code-block:: python

    # cms_plugins.py
    from cms.models.pluginmodel import CMSPlugin
    from cms.plugin_base import CMSPluginBase
    from cms.plugin_pool import plugin_pool


    @plugin_pool.register_plugin
    class HelloPlugin(CMSPluginBase):
        model = CMSPlugin
        name = "Hello"
        render_template = "hello_world.html"

The template is still useful in headless mode: it lets editors see the plugin in the
django CMS structure board and powers the optional ``?html=1`` rendering.

Add the plugin to a page, then fetch the placeholder content:

.. code-block:: bash

    curl "http://localhost:8080/api/en/placeholders/5/11/content/"

.. code-block:: json

    {
      "slot": "content",
      "content": [
        { "plugin_type": "HelloPlugin" }
      ],
      "html": ""
    }

A plugin with model fields serializes each field by name:

.. code-block:: python

    # models.py
    from cms.models import CMSPlugin
    from cms.models.fields import PageField
    from django.db import models


    class HeroPluginModel(CMSPlugin):
        title = models.CharField(max_length=200)
        description = models.TextField()
        image = models.ImageField(upload_to="hero_images")
        link = PageField(blank=True, null=True)

A new model needs migrations — create and apply them before using the plugin:

.. code-block:: bash

    python manage.py makemigrations <your_app>
    python manage.py migrate

Its serialized form:

.. code-block:: json

    {
      "plugin_type": "HeroPlugin",
      "title": "A custom page hero",
      "description": "Important teaser content.",
      "image": "http://localhost:8080/media/hero_images/demo.png",
      "link": "http://localhost:8080/api/en/pages/about/"
    }

Foreign keys are resolved to API endpoints where possible — note how ``link`` becomes the
target page's API URL. See :doc:`../explanation/plugin-serialization` for the resolution
rules.

Nested plugins
--------------

Plugins nested in the structure board (e.g. columns inside a grid) are serialized
recursively. Child plugins appear under a ``children`` array on the parent, so the JSON
mirrors the plugin tree.

Custom: define a ``serializer_class``
-------------------------------------

Set a ``serializer_class`` on the plugin to control exactly which fields appear and how
they are typed. Use this to add computed fields, hide internal ones, or shape data for the
frontend. The serializer is a standard DRF ``ModelSerializer``:

.. code-block:: python

    # serializers.py
    from rest_framework import serializers
    from .models import HeroPluginModel


    class HeroPluginSerializer(serializers.ModelSerializer):
        cta_label = serializers.SerializerMethodField()

        class Meta:
            model = HeroPluginModel
            fields = ["title", "description", "image", "link", "cta_label"]

        def get_cta_label(self, obj) -> str:
            return obj.link_text or "Read more"

.. code-block:: python

    # cms_plugins.py
    from cms.plugin_base import CMSPluginBase
    from cms.plugin_pool import plugin_pool

    from .models import HeroPluginModel
    from .serializers import HeroPluginSerializer


    @plugin_pool.register_plugin
    class HeroPlugin(CMSPluginBase):
        model = HeroPluginModel
        name = "Hero"
        render_template = "hero.html"
        serializer_class = HeroPluginSerializer

The same ``serializer_class`` drives both the runtime content payload and the typed
description returned by the ``/api/plugins/`` endpoint — so a custom
serializer also produces richer, fully typed client code.

Verify the type definition
--------------------------

.. code-block:: bash

    curl http://localhost:8080/api/plugins/

The plugin now reports its precise properties (types, formats, help text), which client
generators turn into accurate frontend types.

.. seealso::

   * :doc:`../explanation/plugin-serialization` — resolution rules, rich text, and limits.
   * :doc:`../reference/index` — the endpoint catalogue and live schema.
   * `django CMS — how to create plugins
     <https://docs.django-cms.org/en/latest/how_to/09-custom_plugins.html>`_
