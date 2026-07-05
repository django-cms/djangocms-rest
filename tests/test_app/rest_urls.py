"""Demo REST urlconf for the stories-style apphook (path-mirrored mount)."""

from django.urls import path

from rest_framework.response import Response
from rest_framework.views import APIView


class DemoPostListView(APIView):
    http_method_names = ("get", "options")

    def get(self, request, language, **kwargs):
        return Response({"language": language, "posts": []})


class DemoPostDetailView(APIView):
    http_method_names = ("get", "options")

    def get(self, request, language, slug, **kwargs):
        return Response({"language": language, "slug": slug})


urlpatterns = [
    path("posts/", DemoPostListView.as_view(), name="post-list"),
    path("posts/<slug:slug>/", DemoPostDetailView.as_view(), name="post-detail"),
]
