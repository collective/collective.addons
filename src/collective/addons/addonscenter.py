# -*- coding: utf-8 -*-
from collective.addons import _
from plone.supermodel import model



class IAddonCenter(model.Schema):
    """ A Templates Upload Center.
    """

    title = schema.TextLine(
        title=_(u'Name Of The Add-on Center'),
    )

    description = schema.Text(
        title=_(u'Description of the Add-on Center'),
    )

    product_description = schema.Text(
        title=_(u'Description Of The Features of Add-ons'),
    )

    product_title = schema.TextLine(
        title=_(u'Add-on Product Name'),
        description=_(
            u'Name of the Add-on product, e.g. only Extensions'),
    )

    available_category = schema.List(title=_(u"Available Categories"),
                                     default=['Product one',],
                                     value_type=schema.TextLine())



class AddonCenterView(BrowserView):
    pass
