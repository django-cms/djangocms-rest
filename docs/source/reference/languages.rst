Languages Endpoints
===================

**The Languages endpoints provide language information in django CMS.**

* This returns all the languages that are configured for the site.
* Language information includes language codes, names and configuration settings.
* This information is useful for building a language switcher and handling language fallbacks in decoupled front-end applications.


CMS Reference
-------------

- `Internationalisation and Localisation <https://docs.django-cms.org/en/latest/explanation/i18n.html>`_
- `Language configuration <https://docs.django-cms.org/en/latest/reference/configuration.html#internationalisation-and-localisation-i18n-and-l10n>`_


Endpoints
---------

List Languages
~~~~~~~~~~~~~~

**GET** ``/api/languages/``

List of languages available for the site.

**Response Attributes:**

* ``code``: Language code (e.g., "en", "de", "fr")
* ``name``: Human readable language name
* ``public``: Whether the language is publicly available
* ``fallbacks``: Array of fallback language codes
* ``redirect_on_fallback``: Whether to redirect when fallback is used
* ``hide_untranslated``: Whether to hide untranslated content

**Query Parameters:**

* ``preview`` (boolean, optional): Has currently no effect on this endpoint

**Example Request:**

.. code-block:: bash

    GET /api/languages/

**Example Response:**

.. code-block:: json

    {
        "code": "en",
        "name": "English",
        "public": true,
        "fallbacks": ["en"],
        "redirect_on_fallback": true,
        "hide_untranslated": true
    }