from cms.models import Page, PageUrl, Placeholder
from cms.utils.conf import get_languages
from cms.utils.i18n import get_language_tuple
from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.views import APIView as DRFAPIView

from djangocms_rest.serializers.pageserializer import PageSerializer, RESTPage
from djangocms_rest.serializers.placeholder import PlaceholderSerializer


class APIView(DRFAPIView):
    http_method_names = ("get", "options")


class LanguageList(APIView):
    def get(self, request, format=None):
        languages = get_languages().get(get_current_site(request).id, None)
        if languages is None:
            raise Http404
        for conf in languages:
            conf["pages"] = f"{request.scheme}://{request.get_host()}" + reverse(
                "pages-root", args=(conf["code"],)
            )
        return Response(languages)


class PageList(APIView):
    """
    List all pages, or create a new page.
    """

    def get(self, request, language, format=None):
        site = get_current_site(request)
        allowed_languages = [lang[0] for lang in get_language_tuple(site.id)]
        if language not in allowed_languages:
            raise Http404
        qs = Page.objects.filter(node__site=site)
        if request.user.is_anonymous:
            qs = qs.filter(login_required=False)
        pages = (RESTPage(request, page, language=language) for page in qs)
        serializer = PageSerializer(pages, many=True, read_only=True)
        return Response(serializer.data)


class PageDetail(APIView):
    """
    Retrieve, update or delete a page instance.
    """

    def get_object(self, site, path):
        page_urls = (
            PageUrl.objects.get_for_site(site)
            .filter(path=path)
            .select_related("page__node")
        )
        page_urls = list(page_urls)  # force queryset evaluation to save 1 query
        try:
            page = page_urls[0].page
        except IndexError:
            raise Http404
        else:
            page.urls_cache = {url.language: url for url in page_urls}
        return page

    def get(self, request, language, path="", format=None):
        site = get_current_site(request)
        allowed_languages = [lang[0] for lang in get_language_tuple(site.pk)]
        if language not in allowed_languages:
            raise Http404
        page = self.get_object(site, path)
        serializer = PageSerializer(
            RESTPage(request, page, language=language), read_only=True
        )
        return Response(serializer.data)


class PlaceholderDetail(APIView):
    def get_placeholder(self, content_type_id, object_id, slot):
        try:
            placeholder = Placeholder.objects.get(
                content_type_id=content_type_id, object_id=object_id, slot=slot
            )
        except Placeholder.DoesNotExist:
            raise Http404
        return placeholder

    def get(self, request, language, content_type_id, object_id, slot, format=None):
        placeholder = self.get_placeholder(content_type_id, object_id, slot)
        if placeholder is None:
            raise Http404
        source = (
            placeholder.content_type.model_class()
            .objects.filter(pk=placeholder.object_id)
            .first()
        )
        if source is None:
            raise Http404
        serializer = PlaceholderSerializer(
            request, placeholder, language, read_only=True
        )
        return Response(serializer.data)
