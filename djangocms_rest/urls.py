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
        "<slug:language>/pages-root/",
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
    path("<slug:language>/menu-root/", views.MenuView.as_view(), name="menu"),
    path(
        "<slug:language>/menu-root/<int:from_level>/<int:to_level>/<int:extra_inactive>/<int:extra_active>/",
        views.MenuView.as_view(),
        name="menu",
    ),
    path("<slug:language>/menu/<path:path>/", views.MenuView.as_view(), name="menu"),
    path(
        "<slug:language>/menu/<path:path>/<int:from_level>/<int:to_level>/<int:extra_inactive>/<int:extra_active>/",
        views.MenuView.as_view(),
        name="menu",
    ),
    # Preview content endpoints
    path(
        "preview/<slug:language>/pages-root/",
        views.PreviewPageView.as_view(),
        name="preview-page-root",
    ),
    path(
        "preview/<slug:language>/pages-tree/",
        views.PreviewPageTreeListView.as_view(),
        name="preview-page-tree-list",
    ),
    path(
        "preview/<slug:language>/pages-list/",
        views.PreviewPageListView.as_view(),
        name="preview-page-list",
    ),
    path(
        "preview/<slug:language>/pages/<path:path>/",
        views.PreviewPageView.as_view(),
        name="preview-page",
    ),
    path(
        "preview/<slug:language>/placeholders/<int:content_type_id>/<int:object_id>/<str:slot>/",
        views.PreviewPlaceholderDetailView.as_view(),
        name="preview-placeholder-detail",
    ),
]
