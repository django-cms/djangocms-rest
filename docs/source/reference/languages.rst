Languages
=========

**Reports the languages configured for the current site.**

Useful for building a language switcher and for handling fallbacks in a decoupled
frontend. The data reflects django CMS's ``CMS_LANGUAGES`` for the resolved site (see
:doc:`../how-to/configure-languages`).

This endpoint is **not** language-prefixed.

List languages
--------------

**GET** ``/api/languages/``

Returns a JSON **array** of the languages available for the site. For anonymous requests
only public languages are listed.

**Response item fields**

* ``code`` — language code (e.g. ``"en"``, ``"de"``)
* ``name`` — human-readable language name
* ``public`` — whether the language is publicly available
* ``fallbacks`` — array of fallback language codes
* ``redirect_on_fallback`` — whether django CMS redirects when a fallback is used
* ``hide_untranslated`` — whether untranslated content is hidden (vs. shown via fallback)

**Example request**

.. code-block:: bash

    GET /api/languages/

**Example response**

.. code-block:: json

    [
      {
        "code": "en",
        "name": "English",
        "public": true,
        "fallbacks": ["de"],
        "redirect_on_fallback": true,
        "hide_untranslated": false
      },
      {
        "code": "de",
        "name": "Deutsch",
        "public": true,
        "fallbacks": ["en"],
        "redirect_on_fallback": true,
        "hide_untranslated": true
      }
    ]

.. seealso::

   :doc:`../how-to/configure-languages` — configuring ``CMS_LANGUAGES`` and fallbacks.
