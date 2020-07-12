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
        value_type=schema.TextLine(),
    )


class CollectiveaddonsControlPanelForm(RegistryEditForm):
    schema = ICollectiveaddonsControlPanel
    schema_prefix = 'collectiveaddons'
    label = u'Collective Addons Settings'


CollectiveaddonsControlPanelView = layout.wrap_form(
    CollectiveaddonsControlPanelForm, ControlPanelFormWrapper)
