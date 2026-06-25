Plugins
=======

**Type definitions for every registered plugin.**

* This returns all available plugin type definitions with their properties and schemas
* Plugin definitions include the plugin type identifier, human-readable title, and property definitions
* This endpoint is useful for understanding what plugins are available and their configuration options
* It is particularly useful for creating type-safe schemas for your frontend application
* Schema definitions are based on the ``ModelSerializer`` as a default or a ``CustomSerializer`` defined in your plugin

.. hint::
    You can automatically generate type-safe schemas for your typescript frontend application using tools like `QuickType <https://quicktype.io/typescript>`_.


How-to
------
- :doc:`Serialize plugins (default and custom) <../how-to/serialize-plugins>`

CMS Reference
-------------

- `How to create plugins <https://docs.django-cms.org/en/latest/how_to/09-custom_plugins.html#how-to-create-plugins>`_

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

    GET /api/plugins/

**Example Response:**

Returns a JSON **array** with one definition per registered plugin:

.. code-block:: json

    [
      {
        "plugin_type": "TextPlugin",
        "title": "Text",
        "type": "object",
        "properties": {
          "body": {
            "type": "string"
          }
        }
      }
    ]

.. note::
    Definitions are derived from each plugin's serializer fields. Declaring a custom
    ``serializer_class`` yields precise, fully typed properties (types, formats, help
    text) — see :doc:`../how-to/serialize-plugins` and
    :doc:`../explanation/plugin-serialization`.
