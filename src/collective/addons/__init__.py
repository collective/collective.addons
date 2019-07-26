# -*- coding: utf-8 -*-
"""Init and utils."""
from zope.i18nmessageid import MessageFactory


_ = MessageFactory('collective.addons')


MULTISPACE = u'\u3000'


def quote_chars(value):
    # We need to quote parentheses when searching text indices
    if '(' in value:
        value = value.replace('(', '"("')
    if ')' in value:
        value = value.replace(')', '")"')
    if MULTISPACE in value:
        value = value.replace(MULTISPACE, ' ')
    return value
