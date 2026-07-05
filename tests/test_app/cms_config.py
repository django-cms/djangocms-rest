"""Alias-style consumer: contributes an independent endpoint via cms_config."""

from django.urls import path

from cms.app_base import CMSAppConfig

from rest_framework.response import Response
from rest_framework.views import APIView


class DemoAliasView(APIView):
    http_method_names = ("get", "options")

    def get(self, request, language, pk):
        return Response({"id": pk, "language": language, "kind": "demo-alias"})


class DemoAppCMSConfig(CMSAppConfig):
    cms_enabled = False
    djangocms_rest_enabled = True
    cms_rest_endpoints = [
        path(
            "<slug:language>/demo-aliases/<int:pk>/",
            DemoAliasView.as_view(),
            name="demo-alias-detail",
        ),
    ]
