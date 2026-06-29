[![Latest PyPI version](https://img.shields.io/pypi/v/djangocms-rest.svg?style=flat-square)](https://pypi.python.org/pypi/djangocms-rest)
[![Test coverage](https://codecov.io/gh/django-cms/djangocms-rest/graph/badge.svg?token=RKQJL8L8BT)](https://codecov.io/gh/django-cms/djangocms-rest)
[![Python versions](https://img.shields.io/pypi/pyversions/djangocms-rest.svg?style=flat-square)](https://pypi.python.org/pypi/djangocms-rest)
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

Make sure you have at least one published page, then make your first request:

```bash
curl http://localhost:8000/api/en/pages/
```

This returns the home page with its placeholder content embedded as JSON. If `rest_framework` is in `INSTALLED_APPS`, you can also browse the API at `http://localhost:8000/api/`.

See the [tutorial](https://djangocms-rest.readthedocs.io/en/latest/tutorial/index.html) for a full walkthrough.

## Documentation

The [full documentation](https://djangocms-rest.readthedocs.io/en/latest/index.html) is organised
along the [Diátaxis](https://diataxis.fr/) framework:

- **[Tutorial](https://djangocms-rest.readthedocs.io/en/latest/tutorial/index.html)** – a hands-on lesson from empty project to fetching real content
- **[How-to guides](https://djangocms-rest.readthedocs.io/en/latest/how-to/index.html)** – CORS, multi-site, preview, OpenAPI schema, custom plugin serialization
- **[Reference](https://djangocms-rest.readthedocs.io/en/latest/reference/index.html)** – endpoint catalogue, conventions, settings (per-endpoint detail lives in the live OpenAPI schema)
- **[Explanation](https://djangocms-rest.readthedocs.io/en/latest/explanation/index.html)** – headless mode, content model, preview & versioning, plugin serialization, multi-site, caching

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would
like to change.

## License

[BSD-3](https://github.com/django-cms/djangocms-rest/blob/main/LICENSE)
