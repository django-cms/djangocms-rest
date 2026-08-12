from django.apps import apps
from django.urls import path

from . import views
from .appresolver import get_rest_app_patterns
from .schemas import create_view_with_url_name


def _extension_endpoints():
    """Endpoints contributed by third-party apps via their ``cms_config.py``."""
    try:
        extension = apps.get_app_config("djangocms_rest").cms_extension
    except (LookupError, AttributeError):
        # App not ready or cms_config autodiscovery has not run yet.
        return []
    return list(getattr(extension, "endpoints", []))


urlpatterns = [
    path("healthcheck/", views.HealthCheckView.as_view(), name="healthcheck"),
    # Published content endpoints
    path(
        "languages/",
        views.LanguageListView.as_view(),
        name="language-list",
    ),
    path(
        "<slug:language>/pages-tree/",
        views.PageTreeListView.as_view(),
        name="page-tree-list",
    ),
    path(
        "<slug:language>/pages-list/",
        views.PageListView.as_view(),
        name="page-list",
    ),
    path(
        "<slug:language>/pages/",
        create_view_with_url_name(views.PageDetailView, "page-root"),
        name="page-root",
    ),
    path(
        "<slug:language>/pages/<path:path>/",
        create_view_with_url_name(views.PageDetailView, "page-detail"),
        name="page-detail",
    ),
    path(
        "<slug:language>/page_search/",
        views.PageSearchView.as_view(),
        name="page-search",
    ),
    path(
        "<slug:language>/placeholders/<int:content_type_id>/<int:object_id>/<str:slot>/",
        views.PlaceholderDetailView.as_view(),
        name="placeholder-detail",
    ),
    path("plugins/", views.PluginDefinitionView.as_view(), name="plugin-list"),
    # Menu endpoints
    path("<slug:language>/menu/", create_view_with_url_name(views.MenuView, "menu"), name="menu"),
    path(
        "<slug:language>/menu/<int:from_level>/<int:to_level>/<int:extra_inactive>/<int:extra_active>/",
        create_view_with_url_name(views.MenuView, "menu-levels"),
        name="menu-levels",
    ),
    path(
        "<slug:language>/menu/<int:from_level>/<int:to_level>/<int:extra_inactive>/<int:extra_active>/<path:path>/",
        create_view_with_url_name(views.MenuView, "menu-levels-path"),
        name="menu-levels-path",
    ),
    path(
        "<slug:language>/menu/<slug:root_id>/<int:from_level>/<int:to_level>/<int:extra_inactive>/<int:extra_active>/",
        create_view_with_url_name(views.MenuView, "menu-root-levels"),
        name="menu-root-levels",
    ),
    path(
        "<slug:language>/menu/<slug:root_id>/<int:from_level>/<int:to_level>/<int:extra_inactive>/<int:extra_active>/<path:path>/",
        create_view_with_url_name(views.MenuView, "menu-root-levels-path"),
        name="menu-root-levels-path",
    ),
    path(
        "<slug:language>/submenu/<int:levels>/<int:root_level>/<int:nephews>/<path:path>/",
        create_view_with_url_name(views.SubMenuView, "submenu-levels-root-nephews-path"),
        name="submenu-levels-root-nephews-path",
    ),
    path(
        "<slug:language>/submenu/<int:levels>/<int:root_level>/<int:nephews>/",
        create_view_with_url_name(views.SubMenuView, "submenu-levels-root-nephews"),
        name="submenu-levels-root-nephews",
    ),
    path(
        "<slug:language>/submenu/<int:levels>/<int:root_level>/<path:path>/",
        create_view_with_url_name(views.SubMenuView, "submenu-levels-root-path"),
        name="submenu-levels-root-path",
    ),
    path(
        "<slug:language>/submenu/<int:levels>/<int:root_level>/",
        create_view_with_url_name(views.SubMenuView, "submenu-levels-root"),
        name="submenu-levels-root",
    ),
    path(
        "<slug:language>/submenu/<int:levels>/<path:path>/",
        create_view_with_url_name(views.SubMenuView, "submenu-levels-path"),
        name="submenu-levels-path",
    ),
    path(
        "<slug:language>/submenu/<int:levels>/",
        create_view_with_url_name(views.SubMenuView, "submenu-levels"),
        name="submenu-levels",
    ),
    path(
        "<slug:language>/submenu/<path:path>/",
        create_view_with_url_name(views.SubMenuView, "submenu-path"),
        name="submenu-path",
    ),
    path(
        "<slug:language>/submenu/",
        create_view_with_url_name(views.SubMenuView, "submenu"),
        name="submenu",
    ),
    path(
        "<slug:language>/breadcrumbs/<int:start_level>/<path:path>/",
        create_view_with_url_name(views.BreadcrumbView, "breadcrumbs-level-path"),
        name="breadcrumbs-level-path",
    ),
    path(
        "<slug:language>/breadcrumbs/<int:start_level>/",
        create_view_with_url_name(views.BreadcrumbView, "breadcrumbs-level"),
        name="breadcrumbs-level",
    ),
    path(
        "<slug:language>/breadcrumbs/<path:path>/",
        create_view_with_url_name(views.BreadcrumbView, "breadcrumbs-path"),
        name="breadcrumbs-path",
    ),
    path(
        "<slug:language>/breadcrumbs/",
        create_view_with_url_name(views.BreadcrumbView, "breadcrumbs"),
        name="breadcrumbs",
    ),
]

# Independent endpoints contributed via cms_config (e.g. djangocms-alias).
urlpatterns += _extension_endpoints()

# Path-mirrored apphook REST endpoints (e.g. djangocms-stories).
urlpatterns += get_rest_app_patterns()
