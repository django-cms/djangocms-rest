Placeholders Endpoints
======================

**The Placeholders endpoints provide placeholder content in django CMS.**

* Used to retrieve content from placeholders object linked to a specific page
* This essentially returns all plugins in a placeholder as a nested JSON tree according to the defined placeholders in `CMS_PLACEHOLDER_CONF`
* The content is rendered as HTML if the ``?html=1`` parameter is added to the API URL using Django CMS template rendering
* Serialized content is either using ``ModelSerializer`` as a default or a ``CustomSerializer`` defined in your plugins configuration

CMS Reference
-------------

- `Howto define placeholders in CMS_PLACEHOLDER_CONF <https://docs.django-cms.org/en/latest/reference/configuration.html#cms-placeholders>`_
- `Howto create plugins <https://docs.django-cms.org/en/latest/introduction/04-plugins.html#plugins>`_

Endpoints
---------

Retrieve Placeholder
~~~~~~~~~~~~~~~~~~~~

**GET** ``/api/{language}/placeholders/{content_type_id}/{object_id}/{slot}/``

Placeholder contain the dynamic content. This view retrieves the content as a structured nested object.
You can get a direct link to build the query or all attributes from the :doc:`Pages <pages>`.

**Response Attributes:**

* ``slot``: The slot name of the placeholder.
* ``label``: The verbose name of the placeholder.
* ``language``: The language of the returned content.
* ``content``: The content rendered as Serialized JSON.
* ``html``: Optional: The content rendered as HTML.

.. note::
    Use ``?html=1`` to get the content rendered as HTML.


**Path Parameters:**

* ``language`` (string, required): Language code (e.g., "en", "de")
* ``content_type_id`` (integer, required): Content type ID
* ``object_id`` (integer, required): Object ID
* ``slot`` (string, required): Placeholder slot name (e.g., "content", "sidebar")

**Query Parameters:**

* ``html`` (integer, optional): Set to 1 to include HTML rendering in response
* ``preview`` (boolean, optional): Set to true to preview unpublished content (admin access required)

.. note::
    Use ``?preview=true`` has no effect when retrieving the content of a draft page, because we already query the draft content.

**Example Request:**

.. code-block:: bash

    GET /api/en/placeholders/5/9/content/?html=1

**Example Response:**

.. code-block:: json

    {
        "slot": "content",
        "label": "Content",
        "language": "en",
        "content": [
            {
                "plugin_type": "TextPlugin",
                "body": "<p>Hello World!</p>",
                "json": {
                    "type": "doc",
                    "content": [
                        {
                            "type": "paragraph",
                            "attrs": {
                                "textAlign": "left"
                            },
                            "content": [
                                {
                                    "text": "Hello World!",
                                    "type": "text"
                                }
                            ]
                        }
                    ]
                },
                "rte": "tiptap"
            }
        ],
        "html": "<p>Hello World!</p>"
    }
