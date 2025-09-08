import json
from django.urls import reverse
from tests.base import BaseCMSRestTestCase

from django.contrib.contenttypes.models import ContentType
from django.core.files import File


from cms import api
from cms.models import PageContent
from cms.toolbar.utils import get_object_edit_url, get_object_preview_url

from filer.models.imagemodels import Image
from bs4 import BeautifulSoup


def get_text_from_html(html, selector):
    soup = BeautifulSoup(html, "html.parser")
    element = soup.select_one(selector)
    if element:
        return element.get_text(strip=True)
    return None


class PlaceholdersAPITestCase(BaseCMSRestTestCase):
    def setUp(self):
        super().setUp()
        self.page = self.create_homepage(
            title="Test Page",
            template="INHERIT",
            language="en",
            in_navigation=True,
        )
        self.placeholder = self.page.get_placeholders(language="en").get(slot="content")
        self.text_plugin = api.add_plugin(
            placeholder=self.placeholder,
            plugin_type="TextPlugin",
            language="en",
            body="<p>Test content</p>",
            json={
                "type": "doc",
                "content": [
                    {
                        "type": "paragraph",
                        "attrs": {"textAlign": "left"},
                        "content": [{"text": "Test content", "type": "text"}],
                    }
                ],
            },
        )
        self.parent_plugin = api.add_plugin(
            placeholder=self.placeholder,
            plugin_type="DummyParentPlugin",
            language="en",
        )
        self.link_plugin = api.add_plugin(
            placeholder=self.placeholder,
            target=self.parent_plugin,
            plugin_type="DummyLinkPlugin",
            language="en",
            page=self.page,
        )
        self.image_plugin = api.add_plugin(
            placeholder=self.placeholder,
            target=self.parent_plugin,
            plugin_type="DummyImagePlugin",
            language="en",
            filer_image=self.create_image(),
        )
        self.number_plugin = api.add_plugin(
            placeholder=self.placeholder,
            plugin_type="DummyNumberPlugin",
            language="en",
        )

    def create_image(self, filename=None, folder=None):
        filename = filename or "test_image.jpg"
        with open(__file__, "rb") as fh:
            file_obj = File(fh, name=filename)
            image_obj = Image.objects.create(
                owner=self.get_superuser(),
                original_filename=filename,
                file=file_obj,
                folder=folder,
                mime_type="image/jpeg",
            )
            image_obj.save()
        return image_obj

    def test_edit_in_sync_with_api_endpoint(self):
        # Edit endpoint and api endpoint should return the same content

        self.client.force_login(self.user)
        response = self.client.get(
            get_object_edit_url(self.page.get_admin_content("en"))
        )
        api_response = self.client.get(
            reverse(
                "placeholder-detail",
                kwargs={
                    "language": "en",
                    "content_type_id": ContentType.objects.get_for_model(
                        PageContent
                    ).id,
                    "object_id": self.page.get_admin_content("en").id,
                    "slot": "content",
                },
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(api_response.status_code, 200)
        content = response.content.decode("utf-8")
        json_content = json.loads(get_text_from_html(content, "div.rest-placeholder"))
        api_content = api_response.json()
        self.assertEqual(json_content, api_content)

    def test_preview_in_sync_with_api_endpoint(self):
        # Edit endpoint and api endpoint should return the same content

        self.client.force_login(self.user)
        response = self.client.get(
            get_object_preview_url(self.page.get_admin_content("en"))
        )
        api_response = self.client.get(
            reverse(
                "placeholder-detail",
                kwargs={
                    "language": "en",
                    "content_type_id": ContentType.objects.get_for_model(
                        PageContent
                    ).id,
                    "object_id": self.page.get_admin_content("en").id,
                    "slot": "content",
                },
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(api_response.status_code, 200)
        content = response.content.decode("utf-8")

        json_content = json.loads(get_text_from_html(content, "div.rest-placeholder"))
        api_content = api_response.json()
        self.maxDiff = None  # Allow large diffs for detailed comparison
        self.assertEqual(json_content, api_content)

    def test_edit_endpoint(self):
        self.client.force_login(self.user)

        response = self.client.get(
            get_object_edit_url(self.page.get_admin_content("en"))
        )
        self.assertEqual(response.status_code, 200)

        # Test for plugin markers
        self.assertContains(
            response,
            f'<template class="cms-plugin cms-plugin-end cms-plugin-{self.text_plugin.pk}"></template>',
        )
        self.assertContains(
            response,
            f'<template class="cms-plugin cms-plugin-end cms-plugin-{self.parent_plugin.pk}"></template>',
        )
        self.assertContains(
            response,
            f'<template class="cms-plugin cms-plugin-end cms-plugin-{self.link_plugin.pk}"></template>',
        )
        self.assertContains(
            response,
            f'<template class="cms-plugin cms-plugin-end cms-plugin-{self.image_plugin.pk}"></template>',
        )

        # Test for parent plugin
        self.assertContains(
            response,
            '<span class="key">"plugin_type"</span>: <span class="str">"DummyParentPlugin"</span>',
        )

        # Test link plugin resolves link to page API endpoint
        self.assertContains(
            response,
            '<span class="key">"page"</span>: <span class="str">"http://testserver/api/en/pages/"</span>',
        )

        # Test image plugin resolves image URL
        self.assertContains(
            response,
            f'"filer_image"</span>: <span class="str ellipsis">"http://testserver{self.image_plugin.filer_image.url}"</span>',
        )

        # Test for rendering of numbers
        self.assertContains(
            response, '<span class="key">"integer"</span>: <span class="num">42</span>'
        )
        self.assertContains(
            response, '<span class="key">"float"</span>: <span class="num">3.14</span>'
        )
