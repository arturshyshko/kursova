from django import template

register = template.Library()

@register.simple_tag
def table_item(dict, key1, key2, default=None):
    if key1 not in dict:
        return default
    tmp = dict[key1]
    if key2 not in tmp:
        return default
    return tmp[key2] or default


@register.simple_tag
def url_replace(request, field, value):

    dict_ = request.GET.copy()

    dict_[field] = value

    return dict_.urlencode()