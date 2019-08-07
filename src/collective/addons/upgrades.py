# -*- coding: utf-8 -*-
from plone.app.upgrade.utils import loadMigrationProfile
from plone import api
from collective.addons.adapter import IReleasesCompatVersions

import logging

logger = logging.getLogger(__name__)



def reload_gs_profile(context):
    loadMigrationProfile(
        context,
        'profile-collective.addons:default',
    )


def populat_release_compat_version_index(context):
    pc = api.portal.get_tool(name='portal_catalog')

    # Search for all projects:
    projects = pc.searchResults({
        'portal_type': 'collective.addons.addonproject'
    })

    for brain_project in projects:
        project = brain_project.getObject()
        query = '/'.join(project.getPhysicalPath())
        brains = pc.searchResults({
            'path': {'query': query, 'depth': 1},
            'portal_type': ['collective.addons.addonrelease',
                            'collective.addons.addonlinkedrelease']
        })

        result = []
        for brain in brains:
            if isinstance(brain.compatibility_choice, list):
                result = result + brain.compatibility_choice

        IReleasesCompatVersions(project).set(list(set(result)))
        logger.info('Updated project {}'.format(project.id))
