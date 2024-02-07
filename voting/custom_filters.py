# yourapp/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter(name='filter_by_candidate')
def filter_by_candidate(votes, candidate):
    return votes.filter(candidate=candidate)
