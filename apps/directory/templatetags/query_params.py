from django import template

register = template.Library()

@register.simple_tag
def append_query_params(request, **kwargs):
    updated_params = request.GET.copy()
    for key, value in kwargs.items():
        updated_params[key] = value
    return request.build_absolute_uri('?'+updated_params.urlencode())