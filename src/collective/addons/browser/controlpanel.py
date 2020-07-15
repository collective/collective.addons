# -*- coding: utf-8 -*-
from collective.addons import _
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout
from zope import schema
from zope.interface import Interface


class ICollectiveaddonsControlPanel(Interface):
    available_category = schema.Tuple(
        title=_(u'Available Categories'),
        default=('Product one',),
        value_type=schema.TextLine(),
    )

    available_licenses = schema.Tuple(title=_(u'Available Licenses'),
                                      default=(
                                          'GNU-GPL-v2 (GNU General Public'
                                          'License Version 2)',
                                          'GNU-GPL-v3+ (General Public License'
                                          'Version 3 and later)',
                                          'LGPL-v2.1 (GNU Lesser General'
                                          'Public License Version 2.1)',
                                          'LGPL-v3+ (GNU Lesser General Public'
                                          'License Version 3 and later)',
                                          'BSD (BSD License (revised))',
                                          'MPL-v1.1 (Mozilla Public License'
                                          'Version 1.1)',
                                          'MPL-v2.0+ (Mozilla Public License'
                                          'Version 2.0 or later)',
                                          'CC-by-sa-v3 (Creative Commons'
                                          'Attribution-ShareAlike 3.0)',
                                          'CC-BY-SA-v4 (Creative Commons'
                                          'Attribution-ShareAlike 4.0 '
                                          'International)',
                                          'AL-v2 (Apache License Version 2.0)'),
                                      value_type=schema.TextLine(),
                                      )

    available_versions = schema.Tuple(title=_(u'Available Versions'),
                                      default=('Product 1.0',
                                               ),
                                      value_type=schema.TextLine(),
                                      )

    available_platforms = schema.Tuple(title=_(u'Available Platforms'),
                                       default=('All platforms',
                                                'Linux',
                                                'Linux-x64',
                                                'Mac OS X',
                                                'Windows',
                                                'BSD',
                                                'UNIX (other)'),
                                       value_type=schema.TextLine(),
                                       )

    allowed_addonfileextension = schema.TextLine(
        title=_(u'Allowed file extensions'),
        description=_(u'Fill in the allowed file extensions, seperated by '
                      u"a pipe '|'."),
    )

    allowed_apimageextension = schema.TextLine(
        title=_(u'Allowed image file extension'),
        description=_(u'Fill in the allowed image file extensions, seperated '
                      u"by a pipe '|'."),
    )

    allowed_apdocfileextensions = schema.TextLine(
        title=_(u'Allowed documentation file extension'),
        description=_(u'Fill in the allowed documentation file extensions, '
                      u"seperated by a pipe '|'."),
    )


class CollectiveaddonsControlPanelForm(RegistryEditForm):
    schema = ICollectiveaddonsControlPanel
    schema_prefix = 'collectiveaddons'
    label = u'Collective Addons Settings'


CollectiveaddonsControlPanelView = layout.wrap_form(
    CollectiveaddonsControlPanelForm, ControlPanelFormWrapper)
