Configure languages
====================

The API serves content per language. Every content endpoint is prefixed with a language
code (``/api/<language>/…``) and the ``/api/languages/`` endpoint reports what is
available. This guide configures django CMS so those endpoints behave the way you expect.

djangocms-rest does not add language settings of its own — it reads django CMS's
``CMS_LANGUAGES``. Configuring languages here means configuring django CMS.

Goal
----

Expose two languages (English and German), make German non-public, and have requests for
a missing translation fall back to English.

Steps
-----

1. Enable Django i18n and declare the languages:

   .. code-block:: python

       # settings.py
       from django.utils.translation import gettext_lazy as _

       USE_I18N = True
       LANGUAGE_CODE = "en"

       LANGUAGES = [
           ("en", _("English")),
           ("de", _("German")),
       ]

2. Configure ``CMS_LANGUAGES``. The per-language keys map directly onto the fields of the
   ``/api/languages/`` endpoint:

   .. code-block:: python

       CMS_LANGUAGES = {
           1: [  # keyed by SITE_ID
               {
                   "code": "en",
                   "name": _("English"),
                   "public": True,
               },
               {
                   "code": "de",
                   "name": _("German"),
                   "public": False,          # hidden from the public API
                   "hide_untranslated": True,
               },
           ],
           "default": {
               "fallbacks": ["en"],
               "redirect_on_fallback": True,
               "public": True,
               "hide_untranslated": False,
           },
       }

Verify
------

.. code-block:: bash

    curl http://localhost:8080/api/languages/

The endpoint lists only **public** languages for the current site. With the configuration
above, an anonymous request returns English only; ``de`` appears once it is marked
``public`` or when you request it as an authenticated editor.

How it behaves
--------------

* Requesting a non-public or unconfigured language code on any content endpoint returns
  ``404 Not Found`` rather than leaking that the language exists.
* When a page has no translation for the requested language, django CMS's ``fallbacks``
  apply: the API returns the fallback translation. Set ``hide_untranslated: True`` to
  return ``404`` instead of falling back.

.. seealso::

   * :doc:`../reference/index` — the endpoint catalogue (response fields live in the OpenAPI schema).
   * `django CMS — Internationalisation and Localisation
     <https://docs.django-cms.org/en/latest/explanation/i18n.html>`_
   * `django CMS — Language configuration
     <https://docs.django-cms.org/en/latest/reference/configuration.html#std-setting-CMS_LANGUAGES>`_
