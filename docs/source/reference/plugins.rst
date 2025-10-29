Plugins Endpoints
=================

**The Plugins endpoints provide plugin definitions for all available plugins in django CMS.**

* This returns all available plugin type definitions with their properties and schemas
* Plugin definitions include the plugin type identifier, human-readable title, and property definitions
* This endpoint is useful for understanding what plugins are available and their configuration options
* It is particularly useful for creating type-safe schemas for your frontend application
* Schema definitions are based on the ``ModelSerializer`` as a default or a ``CustomSerializer`` defined in your plugin

.. hint::
    You can automatically generate type-safe schemas for your typescript frontend application using tools like `QuickType <https://quicktype.io/typescript>`_.


Howto
------
- :doc:`Plugin Creation & Serialization <../how-to/02-plugin-creation>`

CMS Reference
-------------

- `Howto create plugins <https://docs.django-cms.org/en/latest/how_to/09-custom_plugins.html#how-to-create-plugins>`_

Endpoints
---------

List Plugin Definitions
~~~~~~~~~~~~~~~~~~~~~~~~

**GET** ``/api/plugins/``

Get all plugin type definitions available in the CMS.

**Response Attributes:**

* ``plugin_type``: Unique identifier for the plugin type
* ``title``: Human readable name of the plugin
* ``type``: Schema type
* ``properties``: Property definitions for the plugin

**Query Parameters:**

* ``preview`` (boolean, optional): Set to true to preview unpublished content (admin access required)

**Example Request:**

.. code-block:: bash

    GET /api/plugins/?preview=true

**Example Response:**

.. code-block:: json

    {
        "plugin_type": "TextPlugin",
        "title": "Text",
        "type": "object",
        "properties": {
            "body": {
                "type": "string",
                "description": "Text content"
            }
        }
    }

.. note::
    Use custom serializers to define the properties of your plugin in detail. This also allows a fully typed API response and drastically improves the developer experience.
