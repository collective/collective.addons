# -*- coding: utf-8 -*-
from collective.addons import _
from plone import api
from plone.app.layout.viewlets import ViewletBase
from plone.app.multilingual.dx import directives
from plone.app.textfield import RichText
from plone.supermodel import model
from plone.supermodel.directives import primary
from Products.CMFPlone.browser.search import quote_chars
from Products.Five import BrowserView
from Products.ZCTextIndex.ParseTree import ParseError
from zope import schema
from zope.interface import Invalid

import re


MULTISPACE = u'\u3000'.encode('utf-8')
BAD_CHARS = ('?', '-', '+', '*', MULTISPACE)

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
        title=_(u'Name of the Add-on Center'),
    )

    description = schema.Text(
        title=_(u'Description of the Add-on Center'),
    )

    product_description = schema.Text(
        title=_(u'Description of the features of Add-ons'),
    )

    product_title = schema.TextLine(
        title=_(u'Add-on product name'),
        description=_(
            u'Name of the Add-on product, e.g. only Add-ons'),
    )

    model.fieldset('category',
                   label='Categories et. all',
                   fields=['available_category',
                           'available_licenses',
                           'available_versions',
                           'available_platforms'],
                   )

    available_category = schema.List(title=_(u'Available Categories'),
                                     default=['Product one'],
                                     value_type=schema.TextLine(),
                                     )

    available_licenses = schema.List(title=_(u'Available Licenses'),
                                     default=[
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
                                         'AL-v2 (Apache License Version 2.0)',
    ],
        value_type=schema.TextLine())

    available_versions = schema.List(title=_(u'Available Versions'),
                                     default=['Product 1.0',
                                              ],
                                     value_type=schema.TextLine())
    available_platforms = schema.List(title=_(u'Available Platforms'),
                                      default=['All platforms',
                                               'Linux',
                                               'Linux-x64',
                                               'Mac OS X',
                                               'Windows',
                                               'BSD',
                                               'UNIX (other)'],
                                      value_type=schema.TextLine())

    model.fieldset('Allowed File Extensions',
                   label=u'Allowed file extensions',
                   fields=['allowed_addonfileextension',
                           'allowed_apimageextension',
                           'allowed_apdocfileextensions'])

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

    model.fieldset('instructions',
                   label=u'Instructions',
                   fields=['install_instructions', 'reporting_bugs'],
                   )

    primary('install_instructions')
    install_instructions = RichText(
        title=_(u'Add-on installation instructions'),
        description=_(u'Please fill in the install instructions'),
        required=False,
    )

    primary('reporting_bugs')
    reporting_bugs = RichText(
        title=_(u'Instruction how to report Bugs'),
        required=False,
    )

    model.fieldset('disclaimer',
                   label=u'Legal Disclaimer',
                   fields=['title_legaldisclaimer', 'legal_disclaimer',
                           'title_legaldownloaddisclaimer',
                           'legal_downloaddisclaimer'],
                   )

    title_legaldisclaimer = schema.TextLine(
        title=_(u'Title for Legal Disclaimer and Limitations'),
        default=_(u'Legal Disclaimer and Limitations'),
        required=False,
    )

    legal_disclaimer = schema.Text(
        title=_(u'Text of the Legal Disclaimer and Limitations'),
        description=_(u'Enter the text of the legal disclaimer and '
                      u'limitations that should be displayed to the '
                      u'project creator and should be accepted by '
                      u'the owner of the project.'),
        default=_(u'Fill in the legal disclaimer, that had to be '
                  u'accepted by the project owner.'),
        required=False,
    )

    title_legaldownloaddisclaimer = schema.TextLine(
        title=_(
            u'Title of the Legal Disclaimer and Limitations for Downloads'),
        default=_(u'Legal Disclaimer and Limitations for Downloads'),
        required=False,
    )

    primary('legal_downloaddisclaimer')
    legal_downloaddisclaimer = RichText(
        title=_(u'Text of the Legal Disclaimer and Limitations for Downlaods'),
        description=_(u'Enter any legal disclaimer and limitations for '
                      u'downloads that should appear on each page for '
                      u'dowloadable files.'),
        default=_(u'Fill in the text for the legal download disclaimer.'),
        required=False,
    )

    primary('information_oldversions')
    information_oldversions = RichText(
        title=_(u'Information about search for old product versions'),
        description=_(u'Enter an information about the search for older '
                      u'versions of the product, if they are not on the '
                      u'versions list (compatibility) anymore.'),
        required=False,
    )

    model.fieldset('contactadresses',
                   label=u'Special email adresses',
                   fields=['releaseAllert', 'contactForCenter'],
                   )

    releaseAllert = schema.ASCIILine(
        title=_(u'EMail address for the messages about new releases'),
        description=_(
            u'Enter an email address to which information about a new '
            u'release should be send.'),
        required=False,
    )

    contactForCenter = schema.ASCIILine(
        title=_(
            u'EMail address for communication with the add-on center '
            u'manager and reviewer'),
        description=_(
            u'Enter an email address for the communication with add-on '
            u'center manager and reviewer'),
        default='projects@foo.org',
        constraint=validateEmail,
    )


directives.languageindependent('available_category')
directives.languageindependent('available_licenses')
directives.languageindependent('available_versions')
directives.languageindependent('available_platforms')


class AddonCenterView(BrowserView):

    def get_most_popular_products(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        sort_on = 'positive_ratings'
        contentFilter = {
            'sort_on': sort_on,
            'sort_order': 'reverse',
            'review_state': 'published',
            'portal_type': 'collective.addons.addonproject'}
        return catalog(**contentFilter)

    def category_name(self):
        category = list(self.context.available_category)
        return category

    def get_latest_program_release(self):
        versions = list(self.context.available_versions)
        versions.sort(reverse=True)
        return versions[0]

    def get_newest_products(self):
        sort_on = 'created'
        contentFilter = {
            'sort_on': sort_on,
            'sort_order': 'reverse',
            'review_state': 'published',
            'portal_type': 'collective.addons.addonproject',
        }
        results = api.content.find(**contentFilter)
        return results

    def addonproject_count(self):
        """Return number of projects
        """
        catalog = api.portal.get_tool(name='portal_catalog')

        return len(catalog(portal_type='collective.addons.addonproject',
                           review_state='published'))

    def get_products(self, category, version, sort_on, SearchableText=None):
        # sort_on = 'positive_ratings'
        if SearchableText:
            SearchableText = self.munge_search_term(SearchableText)
            contentFilter = {
                'sort_on': sort_on,
                'SearchableText': SearchableText,
                'sort_order': 'reverse',
                'portal_type': 'collective.addons.addonproject',
            }

        else:
            contentFilter = {
                'sort_on': sort_on,
                'sort_order': 'reverse',
                'portal_type': 'collective.addons.addonproject',
            }

        if version != 'any':
            contentFilter['releases_compat_versions'] = version

        if category:
            contentFilter['getCategories'] = category

        try:
            return api.content.find(**contentFilter)
        except ParseError:
            return []

    def munge_search_term(self, q):
        for char in BAD_CHARS:
            char = str(char)
            q = q.replace(char, ' ')
        r = q.split()
        r = ' AND '.join(r)
        r = quote_chars(r) + '*'
        return r

    def show_search_form(self):
        return 'getCategories' in self.request.environ['QUERY_STRING']


class AddonCenterOwnProjectsViewlet(ViewletBase):

    def get_results(self):
        current_user = api.user.get_current()
        pc = api.portal.get_tool('portal_catalog')
        return pc.portal_catalog(
            portal_type='collective.addons.addonproject',
            sort_on='Date',
            sort_order='reverse',
            Creator=str(current_user))
