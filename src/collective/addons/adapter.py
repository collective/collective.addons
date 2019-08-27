# -*- coding: utf-8 -*-
from collective.addons.addonproject import IAddonProject
from plone.indexer import indexer
from zope.annotation.interfaces import IAnnotations
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


ANNO_KEY = 'collective.releasecompatversions'


class IReleasesCompatVersions(Interface):
    """ The adapter interface for access the releases compat
     versions annotation """


# @implementer(interfaces.IUUID)
# @adapter(interfaces.IAttributeUUID)
# def attributeUUID(context):
#     return getattr(context, interfaces.ATTRIBUTE_NAME, None)


@implementer(IReleasesCompatVersions)
@adapter(IAddonProject)
class ReleasesCompatVersions(object):

    def __init__(self, context):
        self.context = context
        annotations = IAnnotations(context)
        self.versions = annotations.setdefault(ANNO_KEY, [])

    def get(self):
        return self.versions

    def set(self, value):
        annotations = IAnnotations(self.context)
        annotations[ANNO_KEY] = value
        self.context.reindexObject(idxs=['releases_compat_versions'])

    def update(self, value):
        self.set(list(set(self.versions + value)))


@indexer(IAddonProject)
def releases_compat_versions(context):
    """Create a catalogue indexer, registered as an adapter for DX content. """
    return IReleasesCompatVersions(context).get()
