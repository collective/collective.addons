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

    available_versions = schema.List(title=_(u"Available Versions"),
                                     default=['Product 1.0',
                                             ],
                                     value_type=schema.TextLine())
    available_platforms = schema.List(title=_(u"Available Platforms"),
                                      default=['All platforms',
                                               'Linux',
                                               'Linux-x64',
                                               'Mac OS X',
                                               'Windows',
                                               'BSD',
                                               'UNIX (other)'],
                                      value_type=schema.TextLine())

    model.fieldset('instructions',
                   label=u'Instructions',
                   fields=['install_instructions', 'reporting_bugs', ])

    primary('install_instructions')
    install_instructions = RichText(
        title=_(u"Extension Installation Instructions"),
        description=_(u"Please fill in the install instructions"),
        required=False
    )

    primary('reporting_bugs')
    reporting_bugs = RichText(
        title=_(u"Instruction how to report Bugs"),
        required=False
    )

    odel.fieldset('disclaimer',
                  label=u'Legal Disclaimer',
                  fields=['title_legaldisclaimer', 'legal_disclaimer',
                          'title_legaldownloaddisclaimer',
                          'legal_downloaddisclaimer'])

    title_legaldisclaimer = schema.TextLine(
        title=_(u"Title for Legal Disclaimer and Limitations"),
        default=_(u"Legal Disclaimer and Limitations"),
        required=False
    )

    legal_disclaimer = schema.Text(
        title=_(u"Text of the Legal Disclaimer and Limitations"),
        description=_(u"Enter the text of the legal disclaimer and "
                      u"limitations that should be displayed to the "
                      u"project creator and should be accepted by "
                      u"the owner of the project."),
        default=_(u"Fill in the legal disclaimer, that had to be "
                  u"accepted by the project owner."),
        required=False
    )

    title_legaldownloaddisclaimer = schema.TextLine(
        title=_(
            u"Title of the Legal Disclaimer and Limitations for Downloads"),
        default=_(u"Legal Disclaimer and Limitations for Downloads"),
        required=False
    )

    primary('legal_downloaddisclaimer')
    legal_downloaddisclaimer = RichText(
        title=_(u"Text of the Legal Disclaimer and Limitations for Downlaods"),
        description=_(u"Enter any legal disclaimer and limitations for "
                      u"downloads that should appear on each page for "
                      u"dowloadable files."),
        default=_(u"Fill in the text for the legal download disclaimer."),
        required=False
    )


class AddonCenterView(BrowserView):
    pass
