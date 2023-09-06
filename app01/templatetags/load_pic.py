from django import template
from websiteDjango import settings

register = template.Library()

@register.filter
def addstr(s1, s2):
    return str(s1) + str(s2)