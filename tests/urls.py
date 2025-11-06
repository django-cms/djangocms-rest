from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

try:
    from drf_spectacular.views import SpectacularAPIView

    HAS_SPECTACULAR = True
except ImportError:
    HAS_SPECTACULAR = False

admin.autodiscover()

urlpatterns = [
    path(
        "api/",
        include("djangocms_rest.urls"),
    ),
    path("api/pizza/<int:pk>/", lambda request, pk: f"<Pizza: {pk}>", name="pizza-detail"),
    path("admin/", admin.site.urls),
    path("", include("cms.urls")),
]

if HAS_SPECTACULAR:
    urlpatterns.insert(0, path("api/schema/", SpectacularAPIView.as_view(), name="schema"))

urlpatterns += staticfiles_urlpatterns()
