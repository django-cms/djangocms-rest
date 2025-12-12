=========
Changelog
=========

1.0.0
=====

* feat: Add site middleware by @metaforx in https://github.com/django-cms/djangocms-rest/pull/50
* feat: Add menu endpoints by @fsbraun in https://github.com/django-cms/djangocms-rest/pull/49
* feat: add OpenAPI support for "preview" query parameter by @metaforx in https://github.com/django-cms/djangocms-rest/pull/53
* feat: Add `path` field to menu endpoints by @fsbraun in https://github.com/django-cms/djangocms-rest/pull/65
* feat: Add Django 6.0 support to CI by @vinitkumar in https://github.com/django-cms/djangocms-rest/pull/72
* feat: Add readthedocs support by @fsbraun in https://github.com/django-cms/djangocms-rest/pull/75
* feat: Remove PlaceholderRelationSerializer and add Placeholder content instead by @fsbraun in https://github.com/django-cms/djangocms-rest/pull/73
* feat: add package data configuration for static and template files by @metaforx in https://github.com/django-cms/djangocms-rest/pull/81
* feat: Add page search endpoint by @fsbraun in https://github.com/django-cms/djangocms-rest/pull/64
* feat: Preserve placeholder order by @metaforx in https://github.com/django-cms/djangocms-rest/pull/83
* refactor: add distinct operationId in openapi schema for menu endpoin… by @metaforx in https://github.com/django-cms/djangocms-rest/pull/80
* fix: OpenAPI schema for nested navigation by @metaforx in https://github.com/django-cms/djangocms-rest/pull/58
* fix: Page serializer returned null for empty meta_description by @fsbraun in https://github.com/django-cms/djangocms-rest/pull/56
* fix: Add menu endpoint with root_id for the root page by @fsbraun in https://github.com/django-cms/djangocms-rest/pull/57
* fix: Respect ?preview for menu views by @fsbraun in https://github.com/django-cms/djangocms-rest/pull/70
* fix: Check for toolbar attribute before setting preview mode on `?preview=1` request by @fsbraun in https://github.com/django-cms/djangocms-rest/pull/71
* fix: try to fix the issue with coverage files not uploading by @vinitkumar in https://github.com/django-cms/djangocms-rest/pull/74
* fix: readthedoc build by @fsbraun in https://github.com/django-cms/djangocms-rest/pull/76
* fix: Add page path to node attributes by @fsbraun in https://github.com/django-cms/djangocms-rest/pull/78
* fix: Add tests to verify caching behavior by @fsbraun in https://github.com/django-cms/djangocms-rest/pull/85


0.8.1
=====
* fix: Package data was missing from wheel

0.8.0
=====
* fix: Update github actions and readme by @fsbraun in https://github.com/django-cms/djangocms-rest/pull/12
* fix: Update test requirements by @fsbraun in https://github.com/django-cms/djangocms-rest/pull/25
* feat: Refactoring for improved Open API & typing support (allows: automatic schema generation) by @metaforx in https://github.com/django-cms/djangocms-rest/pull/20
* docs: update docs by @metaforx in https://github.com/django-cms/djangocms-rest/pull/26
* feat: add public language support by @metaforx in https://github.com/django-cms/djangocms-rest/pull/27
* feat: update code to support Django CMS 5 by @metaforx in https://github.com/django-cms/djangocms-rest/pull/29
* fix: Enable caching for placeholder serialization and rendering. by @metaforx in https://github.com/django-cms/djangocms-rest/pull/31
* fix: open api schema validation by @metaforx in https://github.com/django-cms/djangocms-rest/pull/34
* feat: extend page serializer with additional page fields by @metaforx in https://github.com/django-cms/djangocms-rest/pull/35
* feat: frontend URL handling with absolute URL generation. by @metaforx in https://github.com/django-cms/djangocms-rest/pull/36
* docs: Update readme by @fsbraun in https://github.com/django-cms/djangocms-rest/pull/39
* feat: Add RESTRenderer by @fsbraun in https://github.com/django-cms/djangocms-rest/pull/42

**New Contributors**
* @PeterW-LWL made their first contribution in https://github.com/django-cms/djangocms-rest/pull/22

**Full Changelog**: https://github.com/django-cms/djangocms-rest/commits/0.8.0

0.1.0
=====

* Basic functionality for placeholders
