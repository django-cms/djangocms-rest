from django.urls import path

from . import views


urlpatterns = [
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
        views.PageDetailView.as_view(),
        name="page-root",
    ),
    path(
        "<slug:language>/pages/<path:path>/",
        views.PageDetailView.as_view(),
        name="page-detail",
    ),
    path(
        "<slug:language>/placeholders/<int:content_type_id>/<int:object_id>/<str:slot>/",
        views.PlaceholderDetailView.as_view(),
        name="placeholder-detail",
    ),
    path("plugins/", views.PluginDefinitionView.as_view(), name="plugin-list"),
    # Menu endpoints
    path("<slug:language>/menu/", views.MenuView.as_view(), name="menu"),
    path(
        "<slug:language>/menu/<int:from_level>/<int:to_level>/<int:extra_inactive>/<int:extra_active>/",
        views.MenuView.as_view(),
        name="menu",
    ),
    path("<slug:language>/menu/<path:path>/", views.MenuView.as_view(), name="menu"),
    path(
        "<slug:language>/menu/<path:path>/<int:from_level>/<int:to_level>/<int:extra_inactive>/<int:extra_active>/",
        views.MenuView.as_view(),
        name="menu",
    ),
]
