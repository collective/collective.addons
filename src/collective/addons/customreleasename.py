# -*- coding: utf-8 -*-
from plone.dexterity.content import Item


class CustomReleaseName(Item):
    """Custom name for a release and linked release from the title and
    the release number"""

    @property
    def title(self):
        if hasattr(self, 'projecttitle') and hasattr(self, 'releasenumber'):   # noqa
            # Guard required for migration
            if self.projecttitle is None:
                self.projecttitle = ''
            return self.projecttitle + ' - ' + self.releasenumber
        else:
            return ''

    def setTitle(self, value):
        return
