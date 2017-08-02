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

