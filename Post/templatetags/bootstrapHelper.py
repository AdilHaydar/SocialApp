from django import template


register = template.Library()

@register.filter(name='isActive')
def isActive(path,element):
    if path == element:
        return 'active'
    else:
        return 'inactive'