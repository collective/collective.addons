# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.addons


class CollectiveAddonsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=collective.addons)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.addons:default')


COLLECTIVE_ADDONS_FIXTURE = CollectiveAddonsLayer()


COLLECTIVE_ADDONS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_ADDONS_FIXTURE,),
    name='CollectiveAddonsLayer:IntegrationTesting',
)


COLLECTIVE_ADDONS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_ADDONS_FIXTURE,),
    name='CollectiveAddonsLayer:FunctionalTesting',
)


COLLECTIVE_ADDONS_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_ADDONS_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='CollectiveAddonsLayer:AcceptanceTesting',
)
