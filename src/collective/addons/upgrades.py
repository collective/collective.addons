# -*- coding: utf-8 -*-
from collective.addons.adapter import IReleasesCompatVersions
from plone import api
from plone.app.upgrade.utils import loadMigrationProfile

import logging


logger = logging.getLogger(__name__)


def reload_gs_profile(context):
    loadMigrationProfile(
        context,
        'profile-collective.addons:default',
    )


def populat_release_compat_version_index(context):

    # Search for all projects:
    projects = api.content.find({
        'portal_type': 'collective.addons.addonproject',
    })

    for brain_project in projects:
        project = brain_project.getObject()
        query = '/'.join(project.getPhysicalPath())
        brains = api.contentfind({
            'path': {'query': query, 'depth': 1},
            'portal_type': ['collective.addons.addonrelease',
                            'collective.addons.addonlinkedrelease'],
        })

        result = []
        for brain in brains:
            if isinstance(brain.compatibility_choice, list):
                result = result + brain.compatibility_choice

        IReleasesCompatVersions(project).set(list(set(result)))
        logger.info('Updated project {0}'.format(project.id))
