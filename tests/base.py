from typing import Optional, Union

from cms.api import create_page
from cms.models import Page
from cms.test_utils.testcases import CMSTestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class RESTTestCase(CMSTestCase):
    prefix = "http://testserver"


class BaseCMSRestTestCase(RESTTestCase):
    @classmethod
    def _create_pages(
        cls,
        page_list: Union[int, list[Union[int, tuple[int, int]]]],
        parent: Optional["Page"] = None,
        is_first: bool = True,
    ):
        new_pages = [
            create_page(
                f"page {i}",
                language="en",
                template="INHERIT",
                parent=parent,
                in_navigation=True,
            )
            for i in range(page_list if isinstance(page_list, int) else len(page_list))
        ]

        if is_first and new_pages:
            homepage = new_pages[0]
            homepage.set_as_homepage()
            homepage.refresh_from_db()

        if isinstance(page_list, list):
            for i, page in enumerate(new_pages):
                cls._create_pages(page_list[i], page, is_first=False)
        else:
            cls.pages = new_pages

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="testpass",
            is_staff=True,
            is_superuser=True,
        )

        cls._create_pages([2, (3, 1), 2], is_first=True)

    @classmethod
    def tearDownClass(cls):
        Page.objects.all().delete()
        super().tearDownClass()
