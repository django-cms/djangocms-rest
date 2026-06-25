Placeholders
============

**The serialized plugin content of a single placeholder.**

A placeholder holds the actual content of a page region as a list of serialized plugins
(a nested JSON tree). You normally reach this endpoint by following the ``details`` link
returned for a placeholder by the :doc:`pages <pages>` listing endpoints — see
:doc:`../explanation/content-model` for why content is fetched in two steps.

Add ``?html=1`` to additionally receive the placeholder rendered as HTML using your django
CMS plugin templates (see :doc:`conventions`).

.. seealso::

   * :doc:`../explanation/plugin-serialization` — how plugin content becomes JSON.
   * `django CMS — CMS_PLACEHOLDER_CONF
     <https://docs.django-cms.org/en/latest/reference/configuration.html#std-setting-CMS_PLACEHOLDER_CONF>`_

Endpoints
---------

Retrieve Placeholder
~~~~~~~~~~~~~~~~~~~~~

**GET** ``/api/{language}/placeholders/{content_type_id}/{object_id}/{slot}/``

Retrieves the content of one placeholder as a structured object. The ``content_type_id``,
``object_id`` and ``slot`` come from the ``details`` link in a :doc:`page <pages>` response.

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
        "details": "http://localhost:8080/api/en/placeholders/5/9/content/?html=1",
        "html": "<p>Hello World!</p>"
    }
