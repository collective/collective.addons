# -*- coding: utf-8 -*-
from collective.addons import _
from plone.supermodel import model
from zope import schema
from plone.supermodel.directives import primary
from plone.app.textfield import RichText
from Products.Five import BrowserView
from plone.app.multilingual.dx import directives

import re
import six


checkEmail = re.compile(
    r'[a-zA-Z0-9._%-]+@([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,4}').match


def validateEmail(value):
    if not checkEmail(value):
        raise Invalid(_(u'Invalid email address'))
    return True


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

    model.fieldset('Allowed File Extensions',
                   label=u'Allowed File Extensions',
                   fields=['allowed_fileextension', 'allowed_imageextension'])

    allowed_fileextension = schema.TextLine(
        title=_(u'Allowed File Extensions'),
        description=_(u'Fill in the allowed file extensions, seperated by '
                    u'a pipe \'|\'.'),
        default=_(u'oxt'),
        )

    allowed_imageextension = schema.TextLine(
        title=_(u'Allowed Image File Extension'),
        description=_(u'Fill in the allowed image file extensions, seperated '
                     u'by a pipe \'|\'.'),
        default=_(u'png|gif|jpg'),
        )

    allowed_docfileextensions = schema.TextLine(
        title=_(u'Allowed Documentation File Extension'),
        description=_(u'Fill in the allowed documentation file extensions, '
                      u'seperated by a pipe \'|\'.'),
        default=_(u'odt|pdf'),
    )

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

    model.fieldset('disclaimer',
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

    primary('information_oldversions')
    information_oldversions = RichText(
        title=_(u'Information About Search For Old Product Versions'),
        description=_(u'Enter an information about the search for older '
                      u'versions of the product, if they are not on the '
                      u'versions list (compatibility) anymore.'),
        required=False,
    )

    model.fieldset('contactadresses',
                   label=u'Special Email Adresses',
                   fields=['contactForCenter'])

    contactForCenter = schema.ASCIILine(
        title=_(
            u'EMail address for communication with the template center '
            u'manager and reviewer'),
        description=_(
            u'Enter an email address for the communication with template '
            u'center manager and reviewer'),
        default='projects@foo.org',
        constraint=validateEmail,
    )


directives.languageindependent('available_category')
directives.languageindependent('available_licenses')
directives.languageindependent('available_versions')
directives.languageindependent('available_platforms')


class AddonCenterView(BrowserView):
    pass
