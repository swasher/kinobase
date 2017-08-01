from django import template

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