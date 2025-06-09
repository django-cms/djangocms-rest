from cms.models import Page, PageContent, Placeholder
from cms.utils.i18n import get_language_tuple, get_languages
from cms.utils.page_permissions import user_can_view_page
from rest_framework.exceptions import NotFound
from rest_framework.permissions import BasePermission
from rest_framework.request import Request

from djangocms_rest.views_base import BaseAPIView


class IsAllowedLanguage(BasePermission):
    """
    Check whether the provided language is allowed for a given site.
    """

    def has_permission(self, request: Request, view: BaseAPIView) -> bool:
        site = view.site
        language = view.kwargs.get("language")
        allowed_languages = [lang[0] for lang in get_language_tuple(site.pk)]
        if language not in allowed_languages:
            raise NotFound()
        return True


class IsAllowedPublicLanguage(IsAllowedLanguage):
    """
    Check whether the provided language is allowed and public for a given site.
    """

    def has_permission(self, request: Request, view: BaseAPIView) -> bool:
        super().has_permission(request, view)
        language = view.kwargs.get("language")
        languages = get_languages()
        public_languages = [
            lang["code"] for lang in languages if lang.get("public", True)
        ]
        if language not in public_languages:
            raise NotFound()
        return True


class CanViewPage(IsAllowedLanguage):
    """
    Check whether the provided language is allowed and the user can view the page.
    """

    def has_object_permission(
        self, request: Request, view: BaseAPIView, obj: Page
    ) -> bool:
        if isinstance(obj, Page):
            if not super().has_permission(request, view):
                raise NotFound()
            return user_can_view_page(request.user, obj)
        return False


class CanViewPlaceholder(BasePermission):
    """
    Object-level permission to check if the user is allowed to view Placeholder.
    This is flaky because it only checks the Placeholder's source object's visibility,
    and general view permission on that model. It only checks object-level permissions
    for Placeholder instances that are linked to PageContent.
    """

    def has_object_permission(
        self, request: Request, view: BaseAPIView, obj: Placeholder
    ) -> bool:
        """
        Check if the object is a Placeholder instance and enforce page view permission
        """
        model = obj.content_type.model_class()
        if issubclass(model, PageContent):
            # If the object is a PageContent, check the page view permission
            if not user_can_view_page(request.user, obj.page):
                raise NotFound()
        if model.objects.filter(id=obj.id).empty():
            # If the object is not visible with the default manager, deny access
            raise NotFound()
        return True

class CanViewPageContent(IsAllowedLanguage):
    """
    Object-level permission to check if the user is allowed to view PageContent.
    """

    def has_object_permission(
        self, request: Request, view: BaseAPIView, obj: PageContent
    ) -> bool:
        """
        # Check if the object is a PageContent instance and enforce page view permission
        """
        if isinstance(obj, PageContent):
            if not user_can_view_page(request.user, obj.page):
                raise NotFound()
        return True
