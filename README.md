[![codecov](https://codecov.io/gh/django-cms/djangocms-rest/graph/badge.svg?token=RKQJL8L8BT)](https://codecov.io/gh/django-cms/djangocms-rest)
[![djangocms4]( https://img.shields.io/badge/django%20CMS-4+-blue.svg)](https://www.django-cms.org/en/)

# django CMS Headless Mode

## What is djangocms-rest?

djangocms-rest enables frontend projects to consume django CMS content through a browseable
read-only, REST/JSON API. It is based on the django rest framework (DRF).

## What is headless mode?

A Headless CMS (Content Management System) is a backend-only content management system that provides
content through APIs, making it decoupled from the front-end presentation layer. This allows
developers to deliver content to any device or platform, such as websites, mobile apps, or IoT
devices, using any technology stack. By separating content management from content presentation,
a Headless CMS offers greater flexibility and scalability in delivering content.

## What are the main benefits of running a CMS in headless mode?

Running a CMS in headless mode offers several benefits, including greater flexibility in delivering
content to multiple platforms and devices through APIs, enabling consistent and efficient
multi-channel experiences. It enhances performance and scalability by allowing frontend and backend
development to progress independently using the best-suited technologies. Additionally, it
streamlines content management, making it easier to update and maintain content across various
applications without needing to alter the underlying infrastructure.

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


## Does the TextPlugin (Rich Text Editor, RTE) provide a json representation of the rich text?

Yes, djangocms-text has both HTML blob and structured JSON support for rich text.

URLs to other CMS objects are dynamic, in the form of `<app-name>.<object-name>:<uid>`, for example
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
pip install git+https://github.com/fsbraun/djangocms-rest@main
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
    "in_navigation": true,
    "soft_root": true,
    "template": "string",
    "xframe_options": "string",
    "limit_visibility_in_menu": true,
    "language": "string",
    "languages": [
        "string"
    ],
    "children": []
}
```

## API Endpoints

The following endpoints are available:

### Public API

If the API is not specifically protected, anyone can access all public content. It's a good idea to
disallow/limit public access, or at least implement proper caching.

| Public Endpoints                                                     | Description                                                                                                                                                                                                  |
|:---------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `/api/languages/`                                                    | Fetch available languages.                                                                                                                                                                                   |
| `/api/plugins/`                                                      | Fetch types for all installed plugins. Used for automatic type checks with frontend frameworks.                                                                                                              |
| `/api/{language}/pages-root/`                                        | Fetch the root page for a given language.                                                                                                                                                                    |
| `/api/{language}/pages-tree/`                                        | Fetch the complete page tree of all published documents for a given language. Suitable for smaller projects for automatic navigation generation. For large page sets, use the `pages-list` endpoint instead. |
| `/api/{language}/pages-list/`                                        | Fetch a paginated list. Supports `limit` and `offset` parameters for frontend structure building.                                                                                                            |
| `/api/{language}/pages/{path}/`                                      | Fetch page details by path for a given language. Path and language information is available via `pages-list` and `pages-tree` endpoints.                                                                     |
| `/api/{language}/placeholders/{content_type_id}/{object_id}/{slot}/` | Fetch published page content objects for a given language. Parameters available from page detail.                                                                                                            |

### Private API (Preview)

For all page related endpoints draft content can be fetched, if the user has the permission to view
preview content.
To determine permissions `user_can_view_page()` from djangocms is used, usually editors with
`is_staff` are allowed to view draft content.

| Private Endpoints                                                           | Description                                                                                                        |
|:----------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------|
| `/api/preview/{language}/pages-root`                                        | Fetch the latest draft content for the root page.                                                                  |
| `/api/preview/{language}/pages-tree`                                        | Fetch the page tree including unpublished pages.                                                                   |
| `/api/preview/{language}/pages-list`                                        | Fetch a paginated list including unpublished pages.                                                                |
| `/api/preview/{language}/pages/{path}`                                      | Fetch the latest draft content from a published or unpublished page, including latest unpublished content objects. |
| `/api/preview/{language}/placeholders/{content_type_id}/{object_id}/{slot}` | Fetch the latest draft content objects for the given language.                                                     |

### Sample API-Response: api/{en}/pages/{sub}/

```json
{
    "title": "sub",
    "page_title": "sub",
    "menu_title": "sub",
    "meta_description": "",
    "redirect": null,
    "in_navigation": true,
    "soft_root": false,
    "template": "INHERIT",
    "xframe_options": 0,
    "limit_visibility_in_menu": null,
    "language": "en",
    "path": "sub",
    "absolute_url": "/sub/",
    "is_home": false,
    "languages": [
        "en"
    ],
    "is_preview": false,
    "creation_date": "2025-02-26T21:22:16.844637Z",
    "changed_date": "2025-02-26T21:22:16.856326Z",
    // GET CONTENT using `/api/{language}/placeholders/{content_type_id}/{object_id}/{slot}/`
    "placeholders": [
        {
            "content_type_id": 5,
            "object_id": 5,
            "slot": "content"
        }
    ]
}
```

### Sample API-Response: api/{en}/placeholders/{5}/{5}/{content}/[?html=1]

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
    //Rendered HTML when uins ?html=1
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
