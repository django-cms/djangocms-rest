from django.urls import reverse
from django.utils import translation

from djangocms_rest.serializers.plugins import serialize_fk, serialize_soft_refs
from tests.base import BaseCMSRestTestCase
from tests.test_app.models import Pizza, Topping


# patch function
def get_api_endpoint(self, language=None):
    if language is None:
        language = translation.get_language()
    return f"/api/{language}/pizza/{self.pk}/"


class PlaceholdersAPITestCase(BaseCMSRestTestCase):
    def test_serialize_fk(self):
        request = self.get_request(reverse("page-root", kwargs={"language": "en"}))

        # No get_api_endpoint method, no default api name registered
        fk = serialize_fk(request, Topping, pk="1")
        self.assertEqual(fk, "test_app.topping:1")

        # No get_api_endpoint method, but default api name registered
        self.assertEqual(
            reverse(f"{Pizza._meta.model_name}-detail", kwargs={"pk": 1}),
            "/api/pizza/1/",
        )
        fk = serialize_fk(request, Pizza, pk="1")
        self.assertEqual(fk, "http://testserver/api/pizza/1/")

        # With get_api_endpoint method
        try:
            Pizza.get_api_endpoint = get_api_endpoint

            pizza = Pizza.objects.create(description="Delicious pizza")
            fk = serialize_fk(request, Pizza, pk=pizza.pk)
            self.assertEqual(fk, f"http://testserver{pizza.get_api_endpoint('en')}")

            fk = serialize_fk(request, Pizza, pk=pizza.pk, obj=pizza)
            self.assertEqual(fk, f"http://testserver{pizza.get_api_endpoint('en')}")
        finally:
            del Pizza.get_api_endpoint

    def test_serialize_soft_refs(self):
        request = self.get_request(reverse("page-root", kwargs={"language": "en"}))

        pk = Pizza.objects.create(description="Delicious pizza").pk

        # Serialize a single soft reference
        fk = serialize_soft_refs(request, {"ref": {"model": "test_app.pizza", "pk": pk}})
        self.assertEqual(fk, {"ref": f"http://testserver/api/pizza/{pk}/"})

        fk = serialize_soft_refs(request, {"link": {"internal_link": f"test_app.pizza:{pk}"}})
        self.assertEqual(fk, {"link": f"http://testserver/api/pizza/{pk}/"})

        fk = serialize_soft_refs(request, {"attrs": {"data-cms-href": f"test_app.pizza:{pk}"}})
        self.assertEqual(fk, {"attrs": {"data-cms-href": f"http://testserver/api/pizza/{pk}/"}})

    def test_serialize_soft_refs_non_resolvable(self):
        request = self.get_request(reverse("page-root", kwargs={"language": "en"}))

        # Serialize a single soft reference
        fk = serialize_soft_refs(request, {"ref": {"model": "test_app.topping", "pk": 314}})
        self.assertEqual(fk, {"ref": "test_app.topping:314"})

        fk = serialize_soft_refs(request, {"link": {"internal_link": "test_app.topping:314"}})
        self.assertEqual(fk, {"link": "test_app.topping:314"})

        fk = serialize_soft_refs(request, {"link": {"file_link": "314"}})
        self.assertEqual(fk, {"link": "filer.file:314"})

        fk = serialize_soft_refs(request, {"attrs": {"data-cms-href": "test_app.topping:314"}})
        self.assertEqual(fk, {"attrs": {"data-cms-href": "test_app.topping:314"}})
