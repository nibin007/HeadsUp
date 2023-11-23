# custom_filters.py
from django import template

register = template.Library()


@register.filter
def is_desired_element_present(queryset, desired_element):
    return any(desired_element in obj.field_name for obj in queryset)
