# -*- coding: utf-8 -*-
from plone import api
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer

import logging


PROFILE_ID = 'profile-collective.addons:default'

# catalog indexes to add
CATALOG_INDEXES = (
    ('addon_release_number', 'FieldIndex'),
    ('releases_compat_versions', 'KeywordIndex'),
)


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            'collective.addons:uninstall',
        ]


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.
    import_catalog_indexes(context)


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.


def import_catalog_indexes(context, logger=None):
    """Method to add our wanted indexes to the portal_catalog.

    @parameters:

    When called from the import_various method below, 'context' is
    the plone site and 'logger' is the portal_setup logger.  But
    this method can also be used as upgrade step, in which case
    'context' will be portal_setup and 'logger' will be None.
    """

    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('vncportal.policy')

    # Run the catalog.xml step as that may have defined new metadata
    # columns.  We could instead add <depends name="catalog"/> to
    # the registration of our import step in zcml, but doing it in
    # code makes this method usable as upgrade step as well.
    # Remove these lines when you have no catalog.xml file.
    setup = api.portal.get_tool('portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'catalog')
    catalog = api.portal.get_tool('portal_catalog')

    indexes = catalog.indexes()
    indexables = []

    for name, meta_type in CATALOG_INDEXES:
        if name not in indexes:
            catalog.addIndex(name, meta_type)
            indexables.append(name)
            logger.info('Added %s for field %s.', meta_type, name)

    if len(indexables) > 0:
        logger.info('Indexing new indexes %s.', ', '.join(indexables))
        catalog.manage_reindexIndex(ids=indexables)
