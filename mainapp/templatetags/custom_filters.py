from django import template

register = template.Library()

@register.filter
def dict_has_key(d, key):
    if isinstance(d, dict):
        return key in d
    return False

@register.filter
def dict_get(d, key):
    if isinstance(d, dict):
        return d.get(key)
    return None
