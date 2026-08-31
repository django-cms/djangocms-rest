"""Stories-style apphook: duck-types ``get_rest_urls`` for path-mirrored mounting."""

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


@apphook_pool.register
class DemoStoriesApphook(CMSApp):
    name = "Demo Stories"
    app_name = "demo_stories"

    def get_urls(self, page=None, language=None, **kwargs):
        return ["tests.test_app.rest_urls"]

    def get_rest_urls(self, page=None, language=None, **kwargs):
        return ["tests.test_app.rest_urls"]


@apphook_pool.register
class DemoPlainApphook(CMSApp):
    """Plain apphook without REST support -- must be ignored by the REST resolver."""

    name = "Demo Plain"
    app_name = "demo_plain"

    def get_urls(self, page=None, language=None, **kwargs):
        return ["tests.test_app.rest_urls"]
