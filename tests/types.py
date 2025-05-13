"""
Type definitions used across multiple test files.
Contains expected field structures, type mappings, and validation schemas.
"""

# API Response Type Definitions
PAGE_META_FIELD_TYPES = {
    "title": str,
    "page_title": str,
    "menu_title": str,
    "meta_description": (str, type(None)),
    "redirect": (str, type(None)),
    "in_navigation": bool,
    "soft_root": bool,
    "template": str,
    "xframe_options": (int, str),
    "limit_visibility_in_menu": (str, type(None)),
    "language": str,
    "path": str,
    "absolute_url": str,
    "is_home": bool,
    "languages": list,
    "is_preview": bool,
    "creation_date": str,
    "changed_date": str,
}

PAGE_CONTENT_FIELD_TYPES = {**PAGE_META_FIELD_TYPES, "placeholders": list}

PAGE_TREE_META_FIELD_TYPES = {**PAGE_META_FIELD_TYPES, "children": list}

LANGUAGE_FIELD_TYPES = {
    "code": str,
    "name": str,
    "public": bool,
    "redirect_on_fallback": bool,
    "fallbacks": list,
    "hide_untranslated": bool,
}

PLACEHOLDER_FIELD_TYPES = {
    "slot": str,
    "label": str,
    "language": str,
    "content": list,
}

PLUGIN_FIELD_TYPES = {
    "plugin_type": str,
    "title": str,
    "type": str,
    "properties": dict,
}
