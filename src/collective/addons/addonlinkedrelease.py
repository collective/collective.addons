# -*- coding: utf-8 -*-
from Acquisition import aq_inner, aq_parent  # noqa
from collective.addons import _
from collective.addons.adapter import IReleasesCompatVersions
from collective.addons.common import yesnochoice
from plone import api
from plone.app.textfield import RichText
from plone.autoform import directives
from plone.dexterity.browser.view import DefaultView
from plone.indexer.decorator import indexer
from plone.supermodel import model
from plone.supermodel.directives import primary
from Products.validation import V_REQUIRED  # noqa
from z3c.form import validator
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope import schema
from zope.interface import directlyProvides
from zope.interface import Invalid
from zope.interface import invariant
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

import re


@provider(IContextAwareDefaultFactory)
def getContainerTitle(self):
    return (self.aq_inner.title)


@provider(IContextAwareDefaultFactory)
def contactinfoDefault(context):
    return context.addoncontactAddress


@provider(IContextAwareDefaultFactory)
def legal_declaration_title(context):
    context = context.aq_inner.aq_parent
    return context.title_legaldisclaimer


@provider(IContextAwareDefaultFactory)
def legal_declaration_text(context):
    context = context.aq_inner.aq_parent
    return context.legal_disclaimer


@provider(IContextAwareDefaultFactory)
def allowedaddonlinkedfileextensions(context):
    context = context.aq_inner.aq_parent
    return context.allowed_addonfileextension.replace('|', ', ')


def vocabAvailLicenses(context):
    """ pick up licenses list from parent """

    license_list = getattr(context.__parent__, 'available_licenses', [])
    terms = []
    for value in license_list:
        terms.append(SimpleTerm(value, token=value.encode('unicode_escape'),
                                title=value))
    return SimpleVocabulary(terms)


directlyProvides(vocabAvailLicenses, IContextSourceBinder)


def vocabAvailVersions(context):
    """ pick up the program versions list from parent """

    versions_list = getattr(context.__parent__, 'available_versions', [])
    terms = []
    for value in versions_list:
        terms.append(SimpleTerm(value, token=value.encode('unicode_escape'),
                                title=value))
    return SimpleVocabulary(terms)


directlyProvides(vocabAvailVersions, IContextSourceBinder)


def vocabAvailPlatforms(context):
    """ pick up the list of platforms from parent """

    platforms_list = getattr(context.__parent__, 'available_platforms', [])
    terms = []
    for value in platforms_list:
        terms.append(SimpleTerm(value, token=value.encode('unicode_escape'),
                                title=value))
    return SimpleVocabulary(terms)


directlyProvides(vocabAvailPlatforms, IContextSourceBinder)


def validatelinkedaddonfileextension(value):
    catalog = api.portal.get_tool(name='portal_catalog')
    result = catalog.uniqueValuesFor('allowedaddonfileextensions')
    pattern = r'^.*\.({0})'.format(result[0])
    matches = re.compile(pattern, re.IGNORECASE).match
    if not matches(value):
        raise Invalid(
            u'You could only upload files with an allowed file '
            u'extension. Please try again to upload a file with the '
            u'correct file extension.')
    return True


class AcceptLegalDeclaration(Invalid):
    __doc__ = _(u'It is necessary that you accept the Legal Declaration')


class IAddonLinkedRelease(model.Schema):
    directives.mode(information='display')
    information = schema.Text(
        title=_(u'Information'),
        description=_(
            u'This Dialog to create a new release consists of different '
            u'register. Please go through this register and fill in the '
            u'appropriate data for your linked release. This register '
            u"'Default' provide fields for general information of your "
            u"linked release. The next register 'compatibility' is the "
            u'place to submit information about the versions with which '
            u'your linked release file(s) is / are compatible. The '
            u'following register asks for some legal informations. '
            u"The next register 'Linked File' provide a field to link "
            u'your release file. The further register are optional. '
            u'There is the opportunity to link further release files '
            u'(for different platforms).'),
    )

    directives.mode(projecttitle='hidden')
    projecttitle = schema.TextLine(
        title=_(u'The computed project title'),
        description=_(
            u'The linked release title will be computed from the parent '
            u'project title'),
        defaultFactory=getContainerTitle,
    )

    releasenumber = schema.TextLine(
        title=_(u'Release Number'),
        description=_(u'Release Number (up to twelf chars)'),
        default=_(u'1.0'),
        max_length=12,
    )

    description = schema.Text(
        title=_(u'Release Summary'),
    )

    primary('details')
    details = RichText(
        title=_(u'Full Release Description'),
        required=False,
    )

    primary('changelog')
    changelog = RichText(
        title=_(u'Changelog'),
        description=_(u'A detailed log of what has changed since the '
                      u'previous release.'),
        required=False,
    )

    model.fieldset('compatibility',
                   label=u'Compatibility',
                   fields=['compatibility_choice'])

    model.fieldset('legal',
                   label=u'Legal',
                   fields=['licenses_choice', 'title_declaration_legal',
                           'declaration_legal', 'accept_legal_declaration',
                           'source_code_inside', 'link_to_source'])

    directives.widget(licenses_choice=CheckBoxFieldWidget)
    licenses_choice = schema.List(
        title=_(u'License of the uploaded file'),
        description=_(u'Please mark one or more licenses you publish your '
                      u'release.'),
        value_type=schema.Choice(source=vocabAvailLicenses),
        required=True,
    )

    directives.widget(compatibility_choice=CheckBoxFieldWidget)
    compatibility_choice = schema.List(
        title=_(u'Compatible with the versions of the product'),
        description=_(u'Please mark one or more program versions with which '
                      u'this release is compatible with.'),
        value_type=schema.Choice(source=vocabAvailVersions),
        required=True,
    )

    directives.mode(title_declaration_legal='display')
    title_declaration_legal = schema.TextLine(
        title=_(u''),
        required=False,
        defaultFactory=legal_declaration_title,
    )

    directives.mode(declaration_legal='display')
    declaration_legal = schema.Text(
        title=_(u''),
        required=False,
        defaultFactory=legal_declaration_text,
    )

    accept_legal_declaration = schema.Bool(
        title=_(u'Accept the above legal disclaimer'),
        description=_(u'Please declare that you accept the above legal '
                      u'disclaimer.'),
        required=True,
    )

    contact_address2 = schema.TextLine(
        title=_(u'Contact email-address'),
        description=_(u'Contact email-address for the project.'),
        required=False,
        defaultFactory=contactinfoDefault,
    )

    source_code_inside = schema.Choice(
        title=_(u'Is the source code inside the add-on?'),
        vocabulary=yesnochoice,
        required=True,
    )

    link_to_source = schema.URI(
        title=_(u'Please fill in the Link (URL) to the Source Code.'),
        required=False,
    )

    model.fieldset('linked_file',
                   label='Linked File',
                   fields=['addonlinkedfileextension',
                           'link_to_file',
                           'external_file_size',
                           'platform_choice',
                           'information_further_file_uploads'])

    directives.mode(addonlinkedfileextension='display')
    addonlinkedfileextension = schema.TextLine(
        title=_(u'The following file extensions are allowed for linked '
                u'files (upper case and lower case and mix of '
                u'both):'),
        defaultFactory=allowedaddonlinkedfileextensions,
    )

    link_to_file = schema.URI(
        title=_(u'The Link to the file of the release'),
        description=_(u'Please insert a link to your add-on file.'),
        required=True,
        constraint=validatelinkedaddonfileextension,
    )

    external_file_size = schema.Float(
        title=_(u'The size of the external hosted file'),
        description=_(
            u'Please fill in the size in kilobyte of the external hosted '
            u'file (e.g. 633, if the size is 633 kb)'),
        required=False,
    )

    directives.widget(platform_choice=CheckBoxFieldWidget)
    platform_choice = schema.List(
        title=_(u'First linked file is compatible with the Platform(s)'),
        description=_(u'Please mark one or more platforms with which the '
                      u'uploaded file is compatible.'),
        value_type=schema.Choice(source=vocabAvailPlatforms),
        required=True,
    )

    directives.mode(information_further_file_uploads='display')
    primary('information_further_file_uploads')
    information_further_file_uploads = RichText(
        title=_(u'Further linked files for this Release'),
        description=_(
            u'If you want to link more files for this release, e.g. because '
            u"there are files for other operating systems, you'll find the "
            u'fields to link this files on the next registers, e.g. '
            u"'Second linked file' for this Release'."),
        required=False,
    )

    model.fieldset('fieldset1',
                   label=_(u'Second linked file'),
                   fields=['addonlinkedfileextension1',
                           'link_to_file1',
                           'external_file_size1',
                           'platform_choice1'],
                   )

    model.fieldset('fieldset2',
                   label=_(u'Third linked file'),
                   fields=['addonlinkedfileextension2',
                           'link_to_file2',
                           'external_file_size2',
                           'platform_choice2'],
                   )

    model.fieldset('fieldset3',
                   label=_(u'Fourth linked file'),
                   fields=['addonlinkedfileextension3',
                           'link_to_file3',
                           'external_file_size3',
                           'platform_choice3'],
                   )

    model.fieldset('fieldset4',
                   label=_(u'Fifth linked file'),
                   fields=['addonlinkedfileextension4',
                           'link_to_file4',
                           'external_file_size4',
                           'platform_choice4'],
                   )

    model.fieldset('fieldset5',
                   label=_(u'Sixth linked file'),
                   fields=['addonlinkedfileextension5',
                           'link_to_file5',
                           'external_file_size5',
                           'platform_choice5'],
                   )

    directives.mode(addonlinkedfileextension1='display')
    addonlinkedfileextension1 = schema.TextLine(
        title=_(u'The following file extensions are allowed for linked '
                u'files (upper case and lower case and mix of '
                u'both):'),
        defaultFactory=allowedaddonlinkedfileextensions,
    )

    link_to_file1 = schema.URI(
        title=_(u'The Link to the file of the release'),
        description=_(u'Please insert a link to your add-on file.'),
        required=False,
        constraint=validatelinkedaddonfileextension,
    )

    external_file_size1 = schema.Float(
        title=_(u'The size of the external hosted file'),
        description=_(u'Please fill in the size in kilobyte of the external '
                      u'hosted file (e.g. 633, if the size is 633 kb)'),
        required=False,
    )

    directives.widget(platform_choice1=CheckBoxFieldWidget)
    platform_choice1 = schema.List(
        title=_(u'Second linked file is compatible with the Platform(s)'),
        description=_(u'Please mark one or more platforms with which the '
                      u'linked file is compatible.'),
        value_type=schema.Choice(source=vocabAvailPlatforms),
        required=True,
    )

    directives.mode(addonlinkedfileextension2='display')
    addonlinkedfileextension2 = schema.TextLine(
        title=_(u'The following file extensions are allowed for linked '
                u'files (upper case and lower case and mix of '
                u'both):'),
        defaultFactory=allowedaddonlinkedfileextensions,
    )

    link_to_file2 = schema.URI(
        title=_(u'The Link to the file of the release'),
        description=_(u'Please insert a link to your add-on file.'),
        required=False,
        constraint=validatelinkedaddonfileextension,
    )

    external_file_size2 = schema.Float(
        title=_(u'The size of the external hosted file'),
        description=_(u'Please fill in the size in kilobyte of the external '
                      u'hosted file (e.g. 633, if the size is 633 kb)'),
        required=False,
    )

    directives.widget(platform_choice2=CheckBoxFieldWidget)
    platform_choice2 = schema.List(
        title=_(u'Third linked file is compatible with the Platform(s)'),
        description=_(u'Please mark one or more platforms with which the '
                      u'linked file is compatible.'),
        value_type=schema.Choice(source=vocabAvailPlatforms),
        required=True,
    )

    directives.mode(addonlinkedfileextension3='display')
    addonlinkedfileextension3 = schema.TextLine(
        title=_(u'The following file extensions are allowed for linked '
                u'files (upper case and lower case and mix of '
                u'both):'),
        defaultFactory=allowedaddonlinkedfileextensions,
    )

    link_to_file3 = schema.URI(
        title=_(u'The Link to the file of the release'),
        description=_(u'Please insert a link to your add-on file.'),
        required=False,
        constraint=validatelinkedaddonfileextension,
    )

    external_file_size3 = schema.Float(
        title=_(u'The size of the external hosted file'),
        description=_(u'Please fill in the size in kilobyte of the external '
                      u'hosted file (e.g. 633, if the size is 633 kb)'),
        required=False,
    )

    directives.widget(platform_choice3=CheckBoxFieldWidget)
    platform_choice3 = schema.List(
        title=_(u'Fourth linked file is compatible with the Platform(s)'),
        description=_(u'Please mark one or more platforms with which the '
                      u'linked file is compatible.'),
        value_type=schema.Choice(source=vocabAvailPlatforms),
        required=True,
    )

    directives.mode(addonlinkedfileextension4='display')
    addonlinkedfileextension4 = schema.TextLine(
        title=_(u'The following file extensions are allowed for linked '
                u'files (upper case and lower case and mix of '
                u'both):'),
        defaultFactory=allowedaddonlinkedfileextensions,
    )

    link_to_file4 = schema.URI(
        title=_(u'The Link to the file of the release'),
        description=_(u'Please insert a link to your add-on file.'),
        required=False,
        constraint=validatelinkedaddonfileextension,
    )

    external_file_size4 = schema.Float(
        title=_(u'The size of the external hosted file'),
        description=_(u'Please fill in the size in kilobyte of the external '
                      u'hosted file (e.g. 633, if the size is 633 kb)'),
        required=False,
    )

    directives.widget(platform_choice4=CheckBoxFieldWidget)
    platform_choice4 = schema.List(
        title=_(u'Fifth linked file is compatible with the Platform(s)'),
        description=_(u'Please mark one or more platforms with which the '
                      u'linked file is compatible.'),
        value_type=schema.Choice(source=vocabAvailPlatforms),
        required=True,
    )

    directives.mode(addonlinkedfileextension5='display')
    addonlinkedfileextension5 = schema.TextLine(
        title=_(u'The following file extensions are allowed for linked '
                u'files (upper case and lower case and mix of '
                u'both):'),
        defaultFactory=allowedaddonlinkedfileextensions,
    )

    link_to_file5 = schema.URI(
        title=_(u'The Link to the file of the release'),
        description=_(u'Please insert a link to your add-on file.'),
        required=False,
        constraint=validatelinkedaddonfileextension,
    )

    external_file_size5 = schema.Float(
        title=_(u'The size of the external hosted file'),
        description=_(u'Please fill in the size in kilobyte of the external '
                      u'hosted file (e.g. 633, if the size is 633 kb)'),
        required=False,
    )

    directives.widget(platform_choice5=CheckBoxFieldWidget)
    platform_choice5 = schema.List(
        title=_(u'Sixth linked file is compatible with the Platform(s)'),
        description=_(u'Please mark one or more platforms with which the '
                      u'linked file is compatible.'),
        value_type=schema.Choice(source=vocabAvailPlatforms),
        required=True,
    )

    @invariant
    def licensenotchoosen(value):
        if not value.licenses_choice:
            raise Invalid(_(u'Please choose a license for your release.'))

    @invariant
    def compatibilitynotchoosen(data):
        if not data.compatibility_choice:
            raise Invalid(_(u'Please choose one or more compatible product '
                            u'versions for your release.'))

    @invariant
    def legaldeclarationaccepted(data):
        if data.accept_legal_declaration is not True:
            raise AcceptLegalDeclaration(_(u'Please accept the Legal '
                                           u'Declaration about your Release '
                                           u'and your linked File'))

    @invariant
    def testingvalue(data):
        if data.source_code_inside != 1 and data.link_to_source is None:
            raise Invalid(_(u'You answered the question, whether the source '
                            u'code is inside your add-on with no '
                            u'(default answer). If this is the correct '
                            u'answer, please fill in the Link (URL) '
                            u'to the Source Code.'))

    @invariant
    def noOSChosen(data):
        if data.link_to_file is not None and data.platform_choice == []:
            raise Invalid(_(u'Please choose a compatible platform for the '
                            u'linked file.'))


@indexer(IAddonLinkedRelease)
def addon_release_number(context, **kw):
    return context.releasenumber


def update_project_releases_compat_versions_on_creation(
        addonlinkedrelease, event):
    IReleasesCompatVersions(
        addonlinkedrelease.aq_parent).update(
        addonlinkedrelease.compatibility_choice)


def update_project_releases_compat_versions(addonlinkedrelease, event):
    pc = api.portal.get_tool(name='portal_catalog')
    query = '/'.join(addonlinkedrelease.aq_parent.getPhysicalPath())
    brains = pc.searchResults({                # noqa
        'path': {'query': query, 'depth': 1},
        'portal_type': ['collective.addons.addonrelease',
                        'collective.addons.addonlinkedrelease'],
    })

    result = []
    for brain in brains:
        if isinstance(brain.compatibility_choice, list):
            result = result + brain.compatibility_choice

    IReleasesCompatVersions(
        addonlinkedrelease.aq_parent).set(list(set(result)))


def notifyAddonHubLinkedReleaseAdd(self, event):
    state = api.content.get_state(self)
    releasemessagereceipient = self.releaseAllert
    catalog = api.portal.get_tool(name='portal_catalog')
    results = catalog(Title=self.title)
    for brain in results:
        url = brain.getURL()

        category = list(self.category_choice)
        compatibility = list(self.compatibility_choice)
        licenses = list(self.licenses_choice)
        pf_list = \
            list(self.platform_choice) + list(self.platform_choice1) + \
            list(self.platform_choice2) + list(self.platform_choice3) + \
            list(self.platform_choice4) + list(self.platform_choice5)
        pf_set = set(pf_list)
        platform = list(pf_set)
        platform.sort()

    if state == 'final' and releasemessagereceipient is not None:
        api.portal.send_email(
            recipient=releasemessagereceipient,
            subject='New Release added',
            body=("""A new linked release was added and published with\n
                  title: {0}\nURL: {1}\nCompatibility:{2}\n
                  Categories: {3}\nLicenses: {4}\n
                  Platforms: {5}""").format(self.title,
                                            url,
                                            compatibility,
                                            category,
                                            licenses,
                                            platform),
        )

    else:
        return None


class ValidateAddonLinkedReleaseUniqueness(validator.SimpleFieldValidator):
    # Validate site-wide uniqueness of release titles.

    def validate(self, value):
        # Perform the standard validation first
        super(ValidateAddonLinkedReleaseUniqueness, self).validate(value)

        if value is not None:
            if IAddonLinkedRelease.providedBy(self.context):
                # The release number is the same as the previous value stored
                # in the object
                if self.context.releasenumber == value:
                    return None

            catalog = api.portal.get_tool(name='portal_catalog')
            # Differentiate between possible contexts (on creation or editing)
            # on creation the context is the container
            # on editing the context is already the object
            if IAddonLinkedRelease.providedBy(self.context):
                query = '/'.join(self.context.aq_parent.getPhysicalPath())
            else:
                query = '/'.join(self.context.getPhysicalPath())

            result = catalog({
                'path': {'query': query, 'depth': 1},
                'portal_type': ['collective.addons.addonrelease',
                                'collective.addons.addonlinkedrelease'],
                'addon_release_number': value})

            if len(result) > 0:
                raise Invalid(_(u'The release number is already in use. '
                                u'Please choose another one.'))


validator.WidgetValidatorDiscriminators(
    ValidateAddonLinkedReleaseUniqueness,
    field=IAddonLinkedRelease['releasenumber'],
)


class AddonLinkedReleaseView(DefaultView):

    def canPublishContent(self):
        return api.user.has_permission(
            'Modify portal content', obj=self.context)

    def releaseLicense(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        path = '/'.join(self.context.getPhysicalPath())
        idx_data = catalog.getIndexDataForUID(path)
        licenses = idx_data.get('releaseLicense')
        return (r for r in licenses)

    def linkedreleaseCompatibility(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        path = '/'.join(self.context.getPhysicalPath())
        idx_data = catalog.getIndexDataForUID(path)
        compatibility = idx_data.get('getCompatibility')
        return (r for r in compatibility)
