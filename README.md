[![Latest PyPI version](https://img.shields.io/pypi/v/djangocms-rest.svg?style=flat-square)](https://pypi.python.org/pypi/djangocms-rest)
[![Test coverage](https://codecov.io/gh/django-cms/djangocms-rest/graph/badge.svg?token=RKQJL8L8BT)](https://codecov.io/gh/django-cms/djangocms-rest)
[![Django versions](https://img.shields.io/pypi/frameworkversions/django/djangocms-rest.svg?style=flat-square)](https://pypi.python.org/pypi/djangocms-rest)
[![django CMS versions](https://img.shields.io/pypi/frameworkversions/django-cms/djangocms-rest.svg?style=flat-square)](https://pypi.python.org/pypi/djangocms-rest)
[![License](https://img.shields.io/github/license/django-cms/djangocms-rest.svg?style=flat-square)](https://pypi.python.org/pypi/djangocms-rest)

# djangocms-rest

djangocms-rest enables frontend projects to consume django CMS content through a browsable,
read-only REST/JSON API. Built on Django REST Framework (DRF) with OpenAPI 3 schema generation
via drf-spectacular.

## Key Features

- **Easy integration** – Integrates effortlessly into existing Django CMS projects
- **REST API** – DRF-based API exposing Django CMS content for SPAs, static sites, and mobile apps
- **Typed Endpoints** – Auto-generate OpenAPI schemas for page data and plugin content
- **Plugin Serialization** – Basic support for all CMS plugins, easily extendable for custom needs
- **Multi-Site Support** – Serve multiple websites from a single instance with isolated API responses
- **Multi-language Content** – Use the robust i18n integration of Django CMS in your frontend
- **Preview & Draft Access** – Fetch unpublished or draft content in your frontend for editing previews
- **Permissions & Authentication** – Uses DRF and Django permissions for secure access control
- **Menus & Breadcrumbs** – Exposes the built-in navigation handlers from Django CMS
- **Caching & Performance** – Works with Django cache backends like Redis and Memcached

## Requirements

- Python >= 3.10, < 3.14
- Django >= 4.2, < 6.1
- Django CMS >= 4.1, < 5.1

## Installation

Install using pip:

```bash
pip install djangocms-rest
```

Update your `INSTALLED_APPS` setting:

```python
INSTALLED_APPS = [
    ...
    "djangocms_rest",
    ...
]
```

> `rest_framework` is installed as a dependency. Add it to `INSTALLED_APPS` if you want to use the browsable API UI or create additional DRF endpoints beyond djangocms-rest.

Add the API endpoints to your project's `urls.py`:

```python
from django.urls import path, include

urlpatterns = [
    ...
    path('api/', include('djangocms_rest.urls')),
    ...
]
```
> Using `api/cms/` as the path helps separate djangocms-rest endpoints in API documentation and frontend implementation.


### Usage

Make sure you have existing pages. If `rest_framework` is in `INSTALLED_APPS`, you can navigate to Django REST Framework's browsable API at `http://localhost:8000/api/`.

## Documentation

- **Getting Started** – Quick start guide and installation instructions
- **OpenAPI Support** – Schema generation and API documentation setup
- **How-to Guides** – Multi-site configuration, plugin creation, and serialization
- **API Reference** – Complete endpoint documentation

See the [full documentation](https://djangocms-rest.readthedocs.io/en/latest/index.html) for details.

## Headless Mode

### What is headless mode?

A Headless CMS (Content Management System) is a backend-only content management system that provides
content through APIs, making it decoupled from the frontend presentation layer. This allows
developers to deliver content to any device or platform, such as websites, mobile apps, or IoT
devices, using any technology stack. By separating content management from content presentation,
a Headless CMS offers greater flexibility and scalability in delivering content.

Used with `drf-spectacular`, djangocms-rest generates complete OpenAPI schemas for both DRF
endpoints and Django CMS content plugins. This allows seamless, typed integration with
TypeScript-friendly frameworks.

### Benefits

- Decouple frontend and backend development—use any frontend framework (React, Vue, Angular, Next.js, Nuxt, SvelteKit, Remix, Astro, etc.)
- Serve content to multiple platforms (web, mobile, IoT) via REST/JSON APIs
- Improved performance through optimized frontend rendering
- Content updates propagate across all platforms without frontend deployments
- Easier integration with modern frameworks and third-party services

### Considerations

- Inline editing and content preview are available as JSON views on both edit and preview mode. Turn
  JSON rendering on and off using the `REST_JSON_RENDERING` setting.
- Use `Structure Mode` in CMS to directly edit content in the frontend when the decoupled view is embedded as an iframe.
- The API focuses on fetching plugin content and page structure as JSON data. Apphook logic must be
  implemented using custom logic.
- Website rendering is entirely decoupled and must be implemented in the frontend framework.

## FAQ

### Are there JavaScript packages for drop-in support of frontend editing in the JavaScript framework of my choice?

The good news first: django CMS headless mode is fully backend supported and works independently
of the javascript framework. It is fully compatible with the javascript framework of your choosing.

### How can I implement a plugin for headless mode?

It's pretty much the same as for a traditional django CMS project, see
[here for instructions on how to create django CMS plugins](https://docs.django-cms.org/en/latest/how_to/09-custom_plugins.html).

Let's have an example. Here is a simple plugin with two fields to render a custom header. Please
note that the template included is just a simple visual helper to support editors to manage
content in the django CMS backend. Also, backend developers can now toy around and test their
django CMS code independently of a frontend project.

After setting up djangocms-rest and creating such a plugin you can now run the project and see a
REST/JSON representation of your content in your browser, ready for consumption by a decoupled
frontend.

`cms_plugins.py`:
```
# -*- coding: utf-8 -*-
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from . import models


class CustomHeadingPlugin(CMSPluginBase):
    model = models.CustomHeadingPluginModel
    module = 'Layout Helpers'
    name = "My Custom Heading"

    # this is just a simple, unstyled helper rendering so editors can manage content
    render_template = 'custom_heading_plugin/plugins/custom-heading.html'

    allow_children = False


plugin_pool.register_plugin(CustomHeadingPlugin)
```

`models.py`:
```
from cms.models.pluginmodel import CMSPlugin
from django.db import models


class CustomHeadingPluginModel(CMSPlugin):

    heading_text = models.CharField(
        max_length=256,
    )

    size = models.PositiveIntegerField(default=1)
```

`templates/custom_heading_plugin/plugins/custom-heading.html`:
```
<h{{ instance.size }} class="custom-header">{{ instance.heading_text }}</h{{ instance.size }}>
```


### Do default plugins support headless mode out of the box?

Yes, djangocms-rest provides out of the box support for any and all django CMS plugins whose content
can be serialized.

Custom DRF serializers can be declared for custom plugins by setting its `serializer_class` property.

### Does the TextPlugin (Rich Text Editor, RTE) provide a JSON representation of the rich text?

Yes, djangocms-text has both HTML blob and structured JSON support for rich text.

URLs to other Django model objects are dynamic and resolved to API endpoints if possible. If the referenced model
provides a `get_api_endpoint()` method, it is used for resolution. If not, djangocms-rest tries to reverse `<model-name>-detail`.
If resolution fails dynamic objects are returned in the form of `<app-name>.<object-name>:<uid>`, for example
`cms.page:2`. The frontend can then use this to resolve the object and create the appropriate URLs
to the object's frontend representation.

### I don't need pages, I just have a fixed number of content areas in my frontend application for which I need CMS support.

Absolutely, you can use the djangocms-aliases package. It allows you to define custom _placeholders_
that are not linked to any pages. djangocms-rest will then make a list of those aliases and their
content available via the REST API.

## OpenAPI 3 Support

djangocms-rest supports OpenAPI 3 schema generation for Django REST framework and type generation
for all endpoints and installed plugins using `drf-spectacular`.

## API Endpoints

The following endpoints are available:

### Public API

| Endpoints | Description |
|:----------|:------------|
| `/api/languages/` | Fetch available languages for the site |
| `/api/plugins/` | Fetch plugin type definitions for frontend type checks |
| `/api/{language}/pages/` | Fetch the root page for a given language |
| `/api/{language}/pages-tree/` | Fetch complete page tree (suitable for smaller projects) |
| `/api/{language}/pages-list/` | Fetch paginated page list with `limit` and `offset` support |
| `/api/{language}/pages/{path}/` | Fetch page details by path |
| `/api/{language}/page_search/` | Search pages by query term |
| `/api/{language}/placeholders/{content_type_id}/{object_id}/{slot}/` | Fetch placeholder content (supports `?html=1` for rendered HTML) |
| `/api/{language}/menu/...` | Fetch menu navigation (supports optional `{from_level}/{to_level}/{extra_inactive}/{extra_active}`, `{root_id}`, and `{path}` parameters) |
| `/api/{language}/submenu/...` | Fetch submenu navigation (supports optional `{levels}`, `{root_level}`, `{nephews}`, and `{path}` parameters) |
| `/api/{language}/breadcrumbs/...` | Fetch breadcrumb navigation (supports optional `{start_level}` and `{path}` parameters) |

> **Documentation**  
> For complete endpoint documentation, request/response schemas, and authentication details, see the [API Reference](https://djangocms-rest.readthedocs.io/en/latest/reference/index.html).

### Private API (Preview)

For all page related endpoints draft content can be fetched, if the user has the permission to view
preview content.
To determine permissions `user_can_view_page()` from djangocms is used, usually editors with
`is_staff` are allowed to view draft content.

Just add the `?preview` GET parameter to the above page, page-tree, or page-list endpoints.

### Sample API-Response: api/{en}/pages/{sub}/

> GET CONTENT using `/api/{language}/placeholders/{content_type_id}/{object_id}/{slot}/`
```json

{
    "title": "sub",
    "page_title": "sub",
    "menu_title": "sub",
    "meta_description": "",
    "redirect": null,
    "in_navigation": true,
    "soft_root": false,
    "template": "home.html",
    "xframe_options": "",
    "limit_visibility_in_menu": false,
    "language": "en",
    "path": "sub",
    "absolute_url": "/sub/",
    "is_home": false,
    "login_required": false,
    "languages": [
        "en"
    ],
    "is_preview": false,
    "application_namespace": null,
    "creation_date": "2025-02-27T16:49:01.180050Z",
    "changed_date": "2025-02-27T16:49:01.180214Z",
    "placeholders": [
        {
            "content_type_id": 5,
            "object_id": 6,
            "slot": "content"
        },
        {
            "content_type_id": 5,
            "object_id": 6,
            "slot": "cta"
        }
    ]
}
```

### Sample API-Response: api/{en}/placeholders/{5}/{6}/{content}/[?html=1]

> Rendered HTML with an optional flag ?html=1

```json
{
    "slot": "content",
    "label": "Content",
    "language": "en",
    "content": [
        {
            "plugin_type": "TextPlugin",
            "body": "<p>Test Content</p>",
            "json": { ... },
            "rte": "tiptap"
        }
    ],
    "html": "<p>Test Content</p>"
}
```

### OpenAPI Type Generation

Use the provided schema to quickly generate generate clients, SDKs, validators, and more.

**TypeScript** : https://github.com/hey-api/openapi-ts
## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would
like to change.

## License

[BSD-3](https://github.com/django-cms/djangocms-rest/blob/main/LICENSE)
