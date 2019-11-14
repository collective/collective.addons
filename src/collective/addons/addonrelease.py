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
from plone.namedfile.field import NamedBlobFile
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

import itertools
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
def allowedaddonfileextensions(context):
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


def validateaddonfileextension(value):
    catalog = api.portal.get_tool(name='portal_catalog')
    result = catalog.uniqueValuesFor('allowedaddonfileextensions')
    pattern = r'^.*\.({0})'.format(result[0])
    matches = re.compile(pattern, re.IGNORECASE).match
    if not matches(value.filename):
        raise Invalid(
            u'You could only upload files with an allowed file '
            u'extension. Please try again to upload a file with the '
            u'correct file extension.')
    return True


class AcceptLegalDeclaration(Invalid):
    __doc__ = _(u'It is necessary that you accept the Legal Declaration')


class IAddonRelease(model.Schema):
    directives.mode(information='display')
    information = schema.Text(
        title=_(u'Information'),
        description=_(
            u'This Dialog to create a new release consists of different '
            u'register. Please go through this register and fill in the '
            u"appropriate data for your release. This register 'Default' "
            u'provide fields for general information of your release. The '
            u"next register 'compatibility' is the place to submit "
            u'information about the versions with which your release file(s) '
            u'is / are compatible. The following register asks for some '
            u"legal informations. The next register 'File Upload' provide a "
            u'field to upload your release file. The further register are '
            u'optional. There is the opportunity to upload further release '
            u'files (for different platforms).'),
    )

    directives.mode(projecttitle='hidden')
    projecttitle = schema.TextLine(
        title=_(u'The computed project title'),
        description=_(
            u'The release title will be computed from the parent project '
            u'title'),
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
        description=_(
            u'A detailed log of what has changed since the previous release.'),
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
        description=_(
            u'Please mark one or more licenses you publish your release.'),
        value_type=schema.Choice(source=vocabAvailLicenses),
        required=True,
    )

    directives.widget(compatibility_choice=CheckBoxFieldWidget)
    compatibility_choice = schema.List(
        title=_(u'Compatible with versions of the product'),
        description=_(
            u'Please mark one or more program versions with which this '
            u'release is compatible with.'),
        value_type=schema.Choice(source=vocabAvailVersions),
        required=True,
        default=[],
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
        description=_(
            u'Please declare that you accept the above legal disclaimer'),
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
        title=_(u'Please fill in the Link (URL) to the Source Code'),
        required=False,
    )

    model.fieldset('fileupload',
                   label=u'Fileupload',
                   fields=['addonfileextension', 'file', 'platform_choice',
                           'information_further_file_uploads'])

    directives.mode(addonfileextension='display')
    addonfileextension = schema.TextLine(
        title=_(u'The following file extensions are allowed for '
                u'uploaded files (upper case and lower case and mix of '
                u'both):'),
        defaultFactory=allowedaddonfileextensions,
    )

    file = NamedBlobFile(
        title=_(u'The first file you want to upload.'),
        description=_(u'Please upload your file.'),
        required=True,
        constraint=validateaddonfileextension,
    )

    directives.widget(platform_choice=CheckBoxFieldWidget)
    platform_choice = schema.List(
        title=_(u'First uploaded file is compatible with the Platform(s)'),
        description=_(u'Please mark one or more platforms with which the '
                      u'uploaded file is compatible.'),
        value_type=schema.Choice(source=vocabAvailPlatforms),
        required=True,
    )

    directives.mode(information_further_file_uploads='display')
    primary('information_further_file_uploads')
    information_further_file_uploads = RichText(
        title=_(u'Further File Uploads for this Release'),
        description=_(u'If you want to upload more files for this release, '
                      u'e.g. because there are files for other operating '
                      u"systems, you'll find the upload fields on the "
                      u"register 'Further Uploads' and 'Further More "
                      u"Uploads'."),
        required=False,
    )

    model.fieldset('fileset1',
                   label=u'Further File Uploads',
                   fields=['filetitlefield1', 'addonfileextension1',
                           'file1', 'platform_choice1',
                           'filetitlefield2', 'addonfileextension2',
                           'file2', 'platform_choice2',
                           'filetitlefield3', 'addonfileextension3',
                           'file3', 'platform_choice3'],
                   )

    directives.mode(filetitlefield1='display')
    filetitlefield1 = schema.TextLine(
        title=_(u'Second Release File'),
    )

    directives.mode(addonfileextension1='display')
    addonfileextension1 = schema.TextLine(
        title=_(u'The following file extensions are allowed for '
                u'uploaded files (upper case and lower case and mix of '
                u'both):'),
        defaultFactory=allowedaddonfileextensions,
    )

    file1 = NamedBlobFile(
        title=_(u'The second file you want to upload (this is optional)'),
        description=_(u'Please upload your file.'),
        required=False,
        constraint=validateaddonfileextension,
    )

    directives.widget(platform_choice1=CheckBoxFieldWidget)
    platform_choice1 = schema.List(
        title=_(u'Second uploaded file is compatible with the Platform(s)'),
        description=_(u'Please mark one or more platforms with which the '
                      u'uploaded file is compatible.'),
        value_type=schema.Choice(source=vocabAvailPlatforms),
        required=False,
    )

    directives.mode(filetitlefield2='display')
    filetitlefield2 = schema.TextLine(
        title=_(u'Third Release File'),
    )

    directives.mode(addonfileextension2='display')
    addonfileextension2 = schema.TextLine(
        title=_(u'The following file extensions are allowed for '
                u'uploaded files (upper case and lower case and mix of '
                u'both):'),
        defaultFactory=allowedaddonfileextensions,
    )

    file2 = NamedBlobFile(
        title=_(u'The third file you want to upload (this is optional)'),
        description=_(u'Please upload your file.'),
        required=False,
        constraint=validateaddonfileextension,
    )

    directives.widget(platform_choice2=CheckBoxFieldWidget)
    platform_choice2 = schema.List(
        title=_(u'Third uploaded file is compatible with the Platform(s))'),
        description=_(u'Please mark one or more platforms with which the '
                      u'uploaded file is compatible.'),
        value_type=schema.Choice(source=vocabAvailPlatforms),
        required=False,
    )

    directives.mode(filetitlefield3='display')
    filetitlefield3 = schema.TextLine(
        title=_(u'Fourth Release File'),
    )

    directives.mode(addonfileextension3='display')
    addonfileextension3 = schema.TextLine(
        title=_(u'The following file extensions are allowed for '
                u'uploaded files (upper case and lower case and mix of '
                u'both):'),
        defaultFactory=allowedaddonfileextensions,
    )

    file3 = NamedBlobFile(
        title=_(u'The fourth file you want to upload (this is optional)'),
        description=_(u'Please upload your file.'),
        required=False,
        constraint=validateaddonfileextension,
    )

    directives.widget(platform_choice3=CheckBoxFieldWidget)
    platform_choice3 = schema.List(
        title=_(u'Fourth uploaded file is compatible with the Platform(s)'),
        description=_(u'Please mark one or more platforms with which the '
                      u'uploaded file is compatible.'),
        value_type=schema.Choice(source=vocabAvailPlatforms),
        required=False,
    )

    model.fieldset('fileset2',
                   label=u'Further more file uploads',
                   fields=['filetitlefield4', 'addonfileextension4',
                           'file4', 'platform_choice4',
                           'filetitlefield5', 'addonfileextension5',
                           'file5', 'platform_choice5'],
                   )

    directives.mode(filetitlefield4='display')
    filetitlefield4 = schema.TextLine(
        title=_(u'Fifth Release File'),
    )

    directives.mode(addonfileextension4='display')
    addonfileextension4 = schema.TextLine(
        title=_(u'The following file extensions are allowed for '
                u'uploaded files (upper case and lower case and mix of '
                u'both):'),
        defaultFactory=allowedaddonfileextensions,
    )

    file4 = NamedBlobFile(
        title=_(u'The fifth file you want to upload (this is optional)'),
        description=_(u'Please upload your file.'),
        required=False,
        constraint=validateaddonfileextension,
    )

    directives.widget(platform_choice4=CheckBoxFieldWidget)
    platform_choice4 = schema.List(
        title=_(u'Fifth uploaded file is compatible with the Platform(s)'),
        description=_(u'Please mark one or more platforms with which the '
                      u'uploaded file is compatible.'),
        value_type=schema.Choice(source=vocabAvailPlatforms),
        required=False,
    )

    directives.mode(filetitlefield5='display')
    filetitlefield5 = schema.TextLine(
        title=_(u'Sixth Release File'),
    )

    directives.mode(addonfileextension5='display')
    addonfileextension5 = schema.TextLine(
        title=_(u'The following file extensions are allowed for '
                u'uploaded files (upper case and lower case and mix of '
                u'both):'),
        defaultFactory=allowedaddonfileextensions,
    )

    file5 = NamedBlobFile(
        title=_(u'The sixth file you want to upload (this is optional)'),
        description=_(u'Please upload your file.'),
        required=False,
        constraint=validateaddonfileextension,
    )

    directives.widget(platform_choice5=CheckBoxFieldWidget)
    platform_choice5 = schema.List(
        title=_(u'Sixth uploaded file is compatible with the Platform(s)'),
        description=_(u'Please mark one or more platforms with which the '
                      u'uploaded file is compatible.'),
        value_type=schema.Choice(source=vocabAvailPlatforms),
        required=False,
    )

    @invariant
    def testingvalue(data):
        if data.source_code_inside != 1 and data.link_to_source is None:
            raise Invalid(_(u'You answered the question, whether the source '
                            u'code is inside your add-on with no '
                            u'(default answer). If this is the correct '
                            u'answer, please fill in the Link (URL) '
                            u'to the Source Code.'))

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


@indexer(IAddonRelease)
def addon_release_number(context, **kw):
    return context.releasenumber


def update_project_releases_compat_versions_on_creation(addonrelease, event):
    IReleasesCompatVersions(
        addonrelease.aq_parent).update(addonrelease.compatibility_choice)


def update_project_releases_compat_versions(addonrelease, event):
    pc = api.portal.get_tool(name='portal_catalog')
    query = '/'.join(addonrelease.aq_parent.getPhysicalPath())
    brains = pc.searchResults({              # noqa
        'path': {'query': query, 'depth': 1},
        'portal_type': ['collective.addons.addonrelease',
                        'collective.addons.addonlinkedrelease'],
    })

    result = []
    for brain in brains:
        if isinstance(brain.compatibility_choice, list):
            result = result + brain.compatibility_choice

    IReleasesCompatVersions(
        addonrelease.aq_parent).set(list(set(result)))


def notifyAddonHubReleaseAdd(self, event):
    state = api.content.get_state(self)
    releasemessagereceipient = self.releaseAllert

    category = list(self.category_choice)
    compatibility = list(self.compatibility_choice)
    licenses = list(self.licenses_choice)
    platform_fields = [
        'platform_choice',
        'platform_choice2',
        'platform_choice3',
        'platform_choice4',
        'platform_choice5',
    ]
    pf_list = [field for field in platform_fields if getattr(self,
                                                             field, False)]
    pf_list = list(itertools.chain(*pf_list))
    pf_set = set(pf_list)
    platform = list(pf_set)
    platform.sort()

    if state == 'final' and releasemessagereceipient is not None:
        api.portal.send_email(
            recipient=releasemessagereceipient,
            subject='New Release added',
            body=("""A new release was added and published with\n
                  title: {0}\nURL: {1}\nCompatibility:{2}\n
                  Categories: {3}\nLicenses: {4}\n
                  Platforms: {5}""").format(self.title,
                                            self.absolute_url(),
                                            compatibility,
                                            category,
                                            licenses,
                                            platform),
        )

    else:
        return None


class ValidateAddonReleaseUniqueness(validator.SimpleFieldValidator):
    # Validate site-wide uniqueness of release titles.

    def validate(self, value):
        # Perform the standard validation first
        super(ValidateAddonReleaseUniqueness, self).validate(value)

        if value is not None:
            if IAddonRelease.providedBy(self.context):
                # The release number is the same as the previous value stored
                # in the object
                if self.context.releasenumber == value:
                    return None

            catalog = api.portal.get_tool(name='portal_catalog')
            # Differentiate between possible contexts (on creation or editing)
            # on creation the context is the container
            # on editing the context is already the object
            if IAddonRelease.providedBy(self.context):
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
    ValidateAddonReleaseUniqueness,
    field=IAddonRelease['releasenumber'],
)


class AddonReleaseView(DefaultView):

    def canPublishContent(self):
        return api.user.has_permission(
            'Modify portal content', obj=self.context)

    def releaseLicense(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        path = '/'.join(self.context.getPhysicalPath())
        idx_data = catalog.getIndexDataForUID(path)
        licenses = idx_data.get('releaseLicense')
        return (r for r in licenses)

    def releaseCompatibility(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        path = '/'.join(self.context.getPhysicalPath())
        idx_data = catalog.getIndexDataForUID(path)
        compatibility = idx_data.get('getCompatibility')
        return (r for r in compatibility)
