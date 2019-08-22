# -*- coding: utf-8 -*-
from plone.app.content.interfaces import INameFromTitle
from zope.interface import implementer


class INameForReleaseURL(INameFromTitle):
    def title():
        """Return a processed title"""


@implementer(INameForReleaseURL)
class NameForReleaseURL(object):

    def __init__(self, context):
        self.context = context

    @property
    def title(self):
        return self.context.releasenumber
