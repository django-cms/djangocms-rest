[![Latest PyPI version](https://img.shields.io/pypi/v/djangocms-rest.svg?style=flat-square)](https://pypi.python.org/pypi/djangocms-rest)
[![Test coverage](https://codecov.io/gh/django-cms/djangocms-rest/graph/badge.svg?token=RKQJL8L8BT)](https://codecov.io/gh/django-cms/djangocms-rest)
[![Django versions](https://img.shields.io/pypi/frameworkversions/django/djangocms-rest.svg?style=flat-square)](https://pypi.python.org/pypi/djangocms-rest)
[![django CMS versions](https://img.shields.io/pypi/frameworkversions/django-cms/djangocms-rest.svg?style=flat-square)](https://pypi.python.org/pypi/djangocms-rest)
[![License](https://img.shields.io/github/license/django-cms/djangocms-rest.svg?style=flat-square)](https://pypi.python.org/pypi/djangocms-rest)

# django CMS Headless Mode

## What is djangocms-rest?

djangocms-rest enables frontend projects to consume django CMS content through a browsable
read-only, REST/JSON API. It is based on the django rest framework (DRF) and supports OpenAPI
3 schema generation via drf-spectacular.

**✨ Key Features**

💫 **Django CMS 4 and 5 Support** – Including latest version support (5.0)<br>
🏢 **Multi-site support** – Supports Django sites<br>
🌍 **Internationalization (i18n)** – Supports available CMS languages<br>
🌲 **Structured page tree** – Fetch the full page tree with metadata<br>
📚 **Paginated page listing** – Retrieve pages as a list with pagination support<br>
🔄 **Built-in caching** - Uses django cache backend for placeholder serialization/rendering<br>
👀 **Preview support** – Access draft content using `djangocms-versioning` supporting
permissions for authenticated staff user<br>
🧬 **Typed API schema** – Auto-generate OpenAPI schemas for pages and plugins with
`drf-spectacular`

🧩 **Flexible responses** – Fetch plugin content as JSON or fully rendered HTML

> ⚠️ **Note**
>
> `djangocms-rest` is under active development. Since the API is read-only, it's safe to explore
> without risk of unintended data changes.

## What is headless mode?

A Headless CMS (Content Management System) is a backend-only content management system that provides
content through APIs, making it decoupled from the front-end presentation layer. This allows
developers to deliver content to any device or platform, such as websites, mobile apps, or IoT
devices, using any technology stack. By separating content management from content presentation,
a Headless CMS offers greater flexibility and scalability in delivering content.

Used with `drf-spectacular`, djangocms-rest generates complete OpenAPI schemas for both DRF
endpoints and Django CMS content plugins. This allows seamless, typed integration with
TypeScript-friendly frameworks.

## What are the main benefits of running a CMS in headless mode?

Running a CMS in headless mode offers several advantages, particularly for projects that require
flexibility, scalability, and multi-platform content delivery:

**Benefits of running Django CMS in headless mode:**

- Flexible content delivery to multiple platforms and devices via APIs, enabling consistent
  multi-channel experiences.
- Independent development of frontend and backend using best-suited technologies, improving
  scalability and team efficiency.
- Improved performance through optimized frontend rendering and decoupled architecture.
- Streamlined content management, allowing editors to update content across applications without
  touching the infrastructure.
- Easier integration with modern frameworks (e.g., React, Nuxt, Next.js) and third-party services.

## Are there any drawbacks to using Django CMS in headless mode?

First, consider whether the benefits of a headless system outweigh the cost of running two separate
tech stacks for frontend and backend. For larger projects or when working in teams, having a
separation of concerns across different domains can be a significant advantage. However, for smaller
projects, this is often not the case.

**Limitations and considerations in headless mode:**

- Inline editing and content preview are available as JSON views on both edit and preview mode. Turn
  JSON rendering on and off using the `REST_JSON_RENDERING` setting.
- The API focuses on fetching plugin content and page structure as JSON data.
- Website rendering is entirely decoupled and must be implemented in the frontend framework.
- Not (yet) all features of a standard Django CMS are available through the API (eg. Menu).

## Are there js packages for drop-in support of frontend editing in the javascript framework of my choice?

The good news first: django CMS headless mode is fully backend supported and works independently
of the javascript framework. It is fully compatible with the javascript framework of your choosing.

## How can I implement a plugin for headless mode?

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


## Do default plugins support headless mode out of the box?

Yes, djangocms-rest provides out of the box support for any and all django CMS plugins whose content
can be serialized.

Custom DRF serializers can be declared for custom plugins by setting its `serializer_class` property.

## Does the TextPlugin (Rich Text Editor, RTE) provide a json representation of the rich text?

Yes, djangocms-text has both HTML blob and structured JSON support for rich text.

URLs to other Django model objects are dynamic and resolved to API endpoints if possible. If the referenced model
provides a `get_api_endpoint()` method, it is used for resolution. If not, djangocms-rest tries to reverse `<model-name>-detail`.
If resolution fails dynamic objects are returned in the form of `<app-name>.<object-name>:<uid>`, for example
`cms.page:2`. The frontend can then use this to resolve the object and create the appropriate URLs
to the object's frontend representation.

## I don't need pages, I just have a fixed number of content areas in my frontend application for which I need CMS support.

Absolutely, you can use the djangocms-aliases package. It allows you to define custom _placeholders_
that are not linked to any pages. djangocms-rest will then make a list of those aliases and their
content available via the REST API.

## Requirements

- Python
- Django
- Django CMS

## Installation

Install using pip:

```bash
pip install git+https://github.com/django-cms/djangocms-rest@main
```

Update your `INSTALLED_APPS` setting:

```python
INSTALLED_APPS = [
    ...
    'djangocms_rest',
    'rest_framework',
    ...
]
```

```python
# Enabled Caching
CONTENT_CACHE_DURATION = 60  # Overwrites default from django CMS
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',  # use redis/memcached etc.
        'LOCATION': 'unique-snowflake',
        'TIMEOUT': CONTENT_CACHE_DURATION,  # change accordingly
    }
}
```

Add the API endpoints to your project's `urls.py`:

```python
from django.urls import path, include

urlpatterns = [
    ...
    path('api/', include('djangocms_rest.urls')),
    ...
]
```
## Usage

Navigate to django rest framework's browsable API at `http://localhost:8000/api/`.

## OpenAPI 3 Support

djangocms-rest supports OpenAPI 3 schema generation for Django REST framework and type generation
for all endpoints and installed plugins using `drf-spectacular`.

```bash
pip install drf-spectacular
```

Update your `INSTALLED_APPS` setting:

```python
INSTALLED_APPS = [
    ...
    'drf_spectacular',
    ...
]
```

Update your `urls.py` settings.

```python
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    ...
    # OpenAPI schema and documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    ...
```

Finally, add the schema class to the rest framework settings in `settings.py`:
```python
REST_FRAMEWORK = {
    ...,
    "DEFAULT_SCHEMA_CLASS": 'drf_spectacular.openapi.AutoSchema',
    ...,
}
```

Test endpoints and check expected response types: `http://localhost:8000/api/docs/`

Fetch api schema as json/xml: `http://localhost:8000/api/schema/`

Fur further instructions visit drf_spectacular documentation:
https://drf-spectacular.readthedocs.io/en/latest/index.html

### Response schema as JSON for a page object in a list

```json
{
    "title": "string",
    "page_title": "string",
    "menu_title": "string",
    "meta_description": "string",
    "redirect": "string",
    "absolute_url": "string",
    "path": "string",
    "is_home": true,
    "login_required": true,
    "in_navigation": true,
    "soft_root": true,
    "template": "string",
    "xframe_options": "string",
    "limit_visibility_in_menu": false,
    "language": "string",
    "languages": [
        "string"
    ],
    "is_preview": false,
    "application_namespace": "string",
    "creation_date": "2025-05-29T07:59:21.301Z",
    "changed_date": "2025-05-29T07:59:21.301Z",
    "children": []
}
```

## API Endpoints

The following endpoints are available:

### Public API

If the API is not specifically protected, anyone can access all public content. It's a good idea to
disallow/limit public access, or at least implement proper caching.

| Public Endpoints                                                            | Description                                                                                                                                                                                                  |
|:----------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `/api/languages/`                                                           | Fetch available languages.                                                                                                                                                                                   |
| `/api/plugins/`                                                             | Fetch types for all installed plugins. Used for automatic type checks with frontend frameworks.                                                                                                              |
| `/api/{language}/pages-root/`                                               | Fetch the root page for a given language.                                                                                                                                                                    |
| `/api/{language}/pages-tree/`                                               | Fetch the complete page tree of all published documents for a given language. Suitable for smaller projects for automatic navigation generation. For large page sets, use the `pages-list` endpoint instead. |
| `/api/{language}/pages-list/`                                               | Fetch a paginated list. Supports `limit` and `offset` parameters for frontend structure building.                                                                                                            |
| `/api/{language}/pages/{path}/`                                             | Fetch page details by path for a given language. Path and language information is available via `pages-list` and `pages-tree` endpoints.                                                                     |
| `/api/{language}/placeholders/`<br/>`{content_type_id}/{object_id}/{slot}/` | Fetch published page content objects for a given language. Parameters available from page detail.                                                                                                            |

### Private API (Preview)

For all page related endpoints draft content can be fetched, if the user has the permission to view
preview content.
To determine permissions `user_can_view_page()` from djangocms is used, usually editors with
`is_staff` are allowed to view draft content.

| Private Endpoints                                                                  | Description                                                                                                        |
|:-----------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------|
| `/api/preview/{language}/pages-root`                                               | Fetch the latest draft content for the root page.                                                                  |
| `/api/preview/{language}/pages-tree`                                               | Fetch the page tree including unpublished pages.                                                                   |
| `/api/preview/{language}/pages-list`                                               | Fetch a paginated list including unpublished pages.                                                                |
| `/api/preview/{language}/pages/{path}`                                             | Fetch the latest draft content from a published or unpublished page, including latest unpublished content objects. |
| `/api/preview/{language}/placeholders/`<br/>`{content_type_id}/{object_id}/{slot}` | Fetch the latest draft content objects for the given language.                                                     |
|                                                                                    |

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
                                "text": "Test Content",
                                "type": "text"
                            }
                        ]
                    }
                ]
            },
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

[BSD-3](https://github.com/fsbraun/djangocms-rest/blob/main/LICENSE)
