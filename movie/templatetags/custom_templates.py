from django import template
from django.conf import settings

register = template.Library()


@register.filter
def hour_mins(runtime):
    """
    :param runtime: Runtime in minutes - 83
    :return: Runtime as 1:23
    """
    hours = runtime // 60
    minutes = runtime - hours * 60
    h_m = "%d:%02d" % (hours, minutes)
    return h_m


"""
'images': {
    'secure_base_url': 'https://image.tmdb.org/t/p/',
    'profile_sizes': ['w45', 'w185', 'h632', 'original'],
    'poster_sizes': ['w92', 'w154', 'w185', 'w342', 'w500', 'w780', 'original'],
    'still_sizes': ['w92', 'w185', 'w300', 'original'],
    'logo_sizes': ['w45', 'w92', 'w154', 'w185', 'w300', 'w500', 'original'],
    'backdrop_sizes': ['w300', 'w780', 'w1280', 'original'],
    'base_url': 'http://image.tmdb.org/t/p/'
}
"""
@register.filter
# PROFILE
def w45(link):
    secure_base_url = settings.SECURE_BASE_URL
    return secure_base_url+'w45'+link

@register.filter
# PROFILE and POSTER
def w185(link):
    secure_base_url = settings.SECURE_BASE_URL
    return secure_base_url+'w185'+link

@register.filter
# PROFILE
def h632(link):
    secure_base_url = settings.SECURE_BASE_URL
    return secure_base_url+'h632'+link

@register.filter
# PROFILE and POSTER
def original(link):
    secure_base_url = settings.SECURE_BASE_URL
    return secure_base_url+'original'+link

@register.filter
# POSTER
def w92(link):
    secure_base_url = settings.SECURE_BASE_URL
    return secure_base_url+'w92'+link

@register.filter
# POSTER
def w154(link):
    secure_base_url = settings.SECURE_BASE_URL
    if not link:
        return 'http://via.placeholder.com/171x256'
    return secure_base_url+'w154'+link

@register.filter
# POSTER
def w342(link):
    secure_base_url = settings.SECURE_BASE_URL
    return secure_base_url+'w342'+link

@register.filter
# POSTER
def w500(link):
    secure_base_url = settings.SECURE_BASE_URL
    return secure_base_url+'w500'+link

@register.filter
# POSTER
def w780(link):
    secure_base_url = settings.SECURE_BASE_URL
    return secure_base_url+'w780'+link


@register.simple_tag(takes_context=True)
def push_GET_data(context, **kwargs):
    '''
    Returns the URL-encoded querystring for the current page,
    updating the params with the key/value pairs passed to the tag.

    E.g: given the querystring ?foo=1&bar=2
    {% query_transform bar=3 %} outputs ?foo=1&bar=3
    {% query_transform foo='baz' %} outputs ?foo=baz&bar=2
    {% query_transform foo='one' bar='two' baz=99 %} outputs ?foo=one&bar=two&baz=99

    A RequestContext is required for access to the current querystring.
    Reference:
    1. https://gist.github.com/benbacardi/d6cd0fb8c85e1547c3c60f95f5b2d5e1
    2. https://simpleisbetterthancomplex.com/snippet/2016/08/22/dealing-with-querystring-parameters.html
    '''
    query = context['request'].GET.copy()
    for k, v in kwargs.items():
        query[k] = v
    return '?'+query.urlencode()