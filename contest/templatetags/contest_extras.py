from django import template

register = template.Library()

@register.filter
def get_value(value,key):
	return value.get(key,0)

register.filter('get_value', get_value)
