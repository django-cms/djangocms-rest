=========
Changelog
=========

.. changelog::
   :towncrier: ../

0.8.1 (2025-08-29)
==================

Bugfixes
--------

* fix: Package data not included in wheel (#48)

0.8.0 (2025-08-28)
==================

Features
--------

* feat: Add comprehensive documentation for django CMS REST
* feat: Add menu endpoints (#49)
* feat: Add RESTRenderer (#42)
* feat: frontend URL handling with absolute URL generation. (#36)
* feat: extend page serializer with additional page fields (#35)
* feat: add public language support (#27)
* feat: update code to support Django CMS 5 (#29)
* feat: Refactoring for improved Open API & typing support (allows: automatic schema generation) (#20)

Bugfixes
--------

* fix: Enable caching for placeholder serialization and rendering. (#31)
* fix: open api schema validation (#34)
* fix: Update test requirements (#25)
* fix: Update github actions and readme (#12)

Documentation
-------------

* docs: Update documentation references from "django CMS REST" to "djangocms-rest"
* docs: Update readme (#39)
* docs: update docs (#26)
* docs: initial project outline

0.1.0 (2024-05-24)
==================

Features
--------

* Initial commit with basic functionality for placeholders
* Restructure api
* Optionally include HTML in placeholder responses
* Respect page viewing permissions
* Add first test
* Code refactoring
* Fix: page detail by path
* View naming convention cms-model-list/detail
* Update language list url name
* Update rendering test

Bugfixes
--------

* Fix: Language endpoint offers pages list
* Fix test actions
* Fix ruff issues
* Update action to upload codecov
* Update .coveragerc

Documentation
-------------

* Docs
* Update readme
* Update README.md

Development
-----------

* Bump codecov/codecov-action from 4.0.1 to 4.4.1
* Bump codecov/codecov-action from 4.4.1 to 4.5.0
* Bump codecov/codecov-action from 4.5.0 to 4.6.0
* Bump codecov/codecov-action from 4.6.0 to 5.0.2
* Bump codecov/codecov-action from 5.0.2 to 5.3.1
* Bump codecov/codecov-action from 5.3.1 to 5.4.0
* Bump codecov/codecov-action from 5.4.0 to 5.4.2
* Bump codecov/codecov-action from 5.4.2 to 5.4.3
* Bump codecov/codecov-action from 5.4.3 to 5.5.0
* Bump codecov/codecov-action from 5.5.0 to 5.5.1
* change supported version of `django-cms` (#22)
* fix: remove Node.js setup and frontend build from workflow (#28)
* chore: Add django CMS 4.1 support, simplify preview views/ruff format (#40)
* chore(deps): bump actions/checkout from 4 to 5 (#43)
* chore(deps): bump actions/setup-python from 5 to 6 (#52)
* chore(deps): bump codecov/codecov-action from 5.5.0 to 5.5.1 (#51)
* chore: Update documentation configuration and checks
* chore: Bump version from 0.1.0a to 0.8.0 (#46)
* chore: Update readme (#47)
* fix: pyproject.toml
* update pyproj.toml
* Upodate version number
* Update test.yml

Recent Development (2025-10-18)
==============================

Documentation
-------------

* docs: revise contributing guidelines to emphasize community involvement and streamline setup instructions
* docs: refine multi-site guide and installation documentation, enhance language endpoint descriptions, and add planned guides section
* docs: enhance multi-site and quickstart guides with CORS clarification and updated API testing instructions
* docs: update endpoint headings for consistency and enhance multi-site installation instructions
* docs: standardize API section headings and update endpoint descriptions for clarity
* docs: update API documentation to reflect port change to 8080 for local testing
* docs: update documentation structure and content, including new quick start guide and plugin creation instructions
* docs: update multi-site guide with detailed setup instructions and Vue.js example
* docs: enhance multi-site usage guide with Vue.js example and additional resources
* docs: update API endpoint URLs in documentation to use port 8080
* docs: imrove api references
* docs: fix typo in installation instructions
* docs: simplify installation instructions
* docs: improved installation instructions, and minor doc fixes
* docs: Enhance index documentation with motivation and key features
* docs: Update and expand API documentation for various endpoints
* docs: Add `preview` query parameter to API documentation for pages and languages
* docs: Refactor API documentation for languages and pages endpoints

Features
--------

* feat: add OpenAPI support for "preview" query parameter (#53)
* feat: add OpenAPI schema decorator for `MenuView` and include `namespace` in `NavigationNodeSerializer`
* feat: add site middleware (#50)

Bugfixes
--------

* fix: update `child` field in `NavigationNodeListSerializer` to accept multiple instances
* fix: wrap menu serializer data with return_key in `MenuView` response
* fix: exclude method_schema_decorator from test coverage
* fix: mark method_schema_decorator and related lines as uncovered