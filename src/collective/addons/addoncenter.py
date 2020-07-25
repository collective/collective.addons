# -*- coding: utf-8 -*-
from collective.addons import _
from collective.addons.common import validateemail
from plone import api
from plone.app.layout.viewlets import ViewletBase
from plone.app.textfield import RichText
from plone.supermodel import model
from plone.supermodel.directives import primary
from Products.CMFPlone.browser.search import quote_chars
from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView
from Products.ZCTextIndex.ParseTree import ParseError
from zope import schema


MULTISPACE = u'\u3000'.encode('utf-8')
BAD_CHARS = ('?', '-', '+', '*', MULTISPACE)


class IAddonCenter(model.Schema):
    """ A Templates Upload Center.
    """

    title = schema.TextLine(
        title=_(safe_unicode('Name of the Add-on Center')),
    )

    description = schema.Text(
        title=_(safe_unicode('Description of the Add-on Center')),
    )

    product_description = schema.Text(
        title=_(safe_unicode('Description of the features of Add-ons')),
    )

    product_title = schema.TextLine(
        title=_(safe_unicode('Add-on product name')),
        description=_(safe_unicode(
            'Name of the Add-on product, e.g. only Add-ons')),
    )

    model.fieldset('instructions',
                   label=safe_unicode('Instructions'),
                   fields=['install_instructions', 'reporting_bugs'],
                   )

    primary('install_instructions')
    install_instructions = RichText(
        title=_(safe_unicode('Add-on installation instructions')),
        description=_(safe_unicode('Please fill in the install instructions')),
        required=False,
    )

    primary('reporting_bugs')
    reporting_bugs = RichText(
        title=_(safe_unicode('Instruction how to report Bugs')),
        required=False,
    )

    primary('information_oldversions')
    information_oldversions = RichText(
        title=_(safe_unicode('Information about search for old product versions')),
        description=_(safe_unicode('Enter an information about the search for older '
                                   'versions of the product, if they are not on the '
                                   'versions list (compatibility) anymore.')),
        required=False,
    )

    model.fieldset('contactadresses',
                   label=u'Special email adresses',
                   fields=['releaseAllert', 'contactForCenter'],
                   )

    releaseAllert = schema.ASCIILine(
        title=_(safe_unicode('EMail address for the messages about new releases')),
        description=_(safe_unicode(
            'Enter an email address to which information about a new '
            'release should be send.')),
        required=False,
    )

    contactForCenter = schema.ASCIILine(
        title=_(safe_unicode(
            'EMail address for communication with the add-on center '
            'manager and reviewer')),
        description=_(safe_unicode(
            'Enter an email address for the communication with add-on '
            'center manager and reviewer')),
        default='projects@foo.org',
        constraint=validateemail,
    )


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

    def category_names(self):
        return list(api.portal.get_registry_record('collectiveaddons.available_category'))

    def version_names(self):
        return list(api.portal.get_registry_record('collectiveaddons.available_versions'))

    def get_latest_program_release(self):
        versions = list(api.portal.get_registry_record('collectiveaddons.available_versions'))
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
