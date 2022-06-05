from enum import Flag
from django import template
import json

register = template.Library()

def word_in(value, arg):
    lst = str(value).split(', ')
    query_lst = json.loads(arg)
    for val in query_lst:
        if val in lst:
            return True

register.filter('word_in', word_in)
