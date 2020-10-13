from django.template.defaulttags import register


@register.filter(name='times')
def times(number):
    return range(number)


@register.filter
def subtract(value, arg):
    return value - arg
