from django import template

register = template.Library()

@register.filter(name="divideby")
def divideby(value, args):
    if args is not 0:
        return int(value)/int(args)
    else:
        return 0
