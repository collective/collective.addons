# -*- coding: utf-8 -*-
from Acquisition import aq_inner  # noqa
from collective.addons import _
from collective.addons.adapter import IReleasesCompatVersions
from collective.addons.common import allowedaddonfileextensions
from collective.addons.common import legaldeclarationtext
from collective.addons.common import legaldeclarationtitle
from collective.addons.common import validateaddonextension
from collective.addons.common import yesnochoice
from plone import api
from plone.app.textfield import RichText
from plone.autoform import directives
from plone.dexterity.browser.view import DefaultView
from plone.indexer.decorator import indexer
from plone.namedfile.field import NamedBlobFile
from plone.supermodel import model
from plone.supermodel.directives import primary
from Products.CMFPlone.utils import safe_unicode
from Products.validation import V_REQUIRED  # noqa
from z3c.form import validator
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope import schema
from zope.interface import Invalid
from zope.interface import invariant
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory

import itertools


@provider(IContextAwareDefaultFactory)
def getContainerTitle(self):
    return (self.aq_inner.title)


@provider(IContextAwareDefaultFactory)
def contactinfoDefault(context):
    return context.addoncontactAddress


class AcceptLegalDeclaration(Invalid):
    __doc__ = _(safe_unicode('It is necessary that you accept the Legal Declaration'))


class IAddonRelease(model.Schema):
    directives.mode(information='display')
    information = schema.Text(
        title=_(safe_unicode('Information')),
        description=_(safe_unicode(
            'This Dialog to create a new release consists of different '
            'register. Please go through this register and fill in the '
            "appropriate data for your release. This register 'Default' "
            'provide fields for general information of your release. The '
            "next register 'compatibility' is the place to submit "
            'information about the versions with which your release file(s) '
            'is / are compatible. The following register asks for some '
            "legal informations. The next register 'File Upload' provide a "
            'field to upload your release file. The further register are '
            'optional. There is the opportunity to upload further release '
            'files (for different platforms).')),
    )

    directives.mode(projecttitle='hidden')
    projecttitle = schema.TextLine(
        title=_(safe_unicode('The computed project title')),
        description=_(safe_unicode(
            'The release title will be computed from the parent project '
            'title')),
        defaultFactory=getContainerTitle,
    )

    releasenumber = schema.TextLine(
        title=_(safe_unicode('Release Number')),
        description=_(safe_unicode('Release Number (up to twelf chars)')),
        default=_(safe_unicode('1.0')),
        max_length=12,
    )

    description = schema.Text(
        title=_(safe_unicode('Release Summary')),
    )

    primary('details')
    details = RichText(
        title=_(safe_unicode('Full Release Description')),
        required=False,
    )

    primary('changelog')
    changelog = RichText(
        title=_(safe_unicode('Changelog')),
        description=_(safe_unicode(
            'A detailed log of what has changed since the previous release.')),
        required=False,
    )

    model.fieldset('compatibility',
                   label=_(safe_unicode('Compatibility')),
                   fields=['compatibility_choice'])

    model.fieldset('legal',
                   label=_(safe_unicode('Legal')),
                   fields=['licenses_choice', 'title_declaration_legal',
                           'declaration_legal', 'accept_legal_declaration',
                           'source_code_inside', 'link_to_source'])

    directives.widget(licenses_choice=CheckBoxFieldWidget)
    licenses_choice = schema.List(
        title=_(safe_unicode('License of the uploaded file')),
        description=_(safe_unicode(
            'Please mark one or more licenses you publish your release.')),
        value_type=schema.Choice(source='Licenses'),
        required=True,
    )

    directives.widget(compatibility_choice=CheckBoxFieldWidget)
    compatibility_choice = schema.List(
        title=_(safe_unicode('Compatible with versions of the product')),
        description=_(safe_unicode(
            'Please mark one or more program versions with which this '
            'release is compatible with.')),
        value_type=schema.Choice(source='Versions'),
        required=True,
        default=[],
    )

    directives.mode(title_declaration_legal='display')
    title_declaration_legal = schema.TextLine(
        title=_(safe_unicode('')),
        required=False,
        defaultFactory=legaldeclarationtitle,
    )

    directives.mode(declaration_legal='display')
    declaration_legal = schema.Text(
        title=_(safe_unicode('')),
        required=False,
        defaultFactory=legaldeclarationtext,

    )

    accept_legal_declaration = schema.Bool(
        title=_(safe_unicode('Accept the above legal disclaimer')),
        description=_(safe_unicode(
            'Please declare that you accept the above legal disclaimer')),
        required=True,
    )

    contact_address2 = schema.TextLine(
        title=_(safe_unicode('Contact email-address')),
        description=_(safe_unicode('Contact email-address for the project.')),
        required=False,
        defaultFactory=contactinfoDefault,
    )

    source_code_inside = schema.Choice(
        title=_(safe_unicode('Is the source code inside the add-on?')),
        vocabulary=yesnochoice,
        required=True,
    )

    link_to_source = schema.URI(
        title=_(safe_unicode('Please fill in the Link (URL) to the Source Code')),
        required=False,
    )

    model.fieldset('fileupload',
                   label=_(safe_unicode('Fileupload')),
                   fields=['addonfileextension', 'file', 'platform_choice',
                           'information_further_file_uploads'])

    directives.mode(addonfileextension='display')
    addonfileextension = schema.TextLine(
        title=_(safe_unicode(
            'The following file extensions are allowed for '
            'uploaded files (upper case and lower case and mix of '
            'both):')),
        defaultFactory=allowedaddonfileextensions,
    )

    file = NamedBlobFile(
        title=_(safe_unicode('The first file you want to upload.')),
        description=_(safe_unicode('Please upload your file.')),
        required=True,
        constraint=validateaddonextension,
    )

    directives.widget(platform_choice=CheckBoxFieldWidget)
    platform_choice = schema.List(
        title=_(safe_unicode('First uploaded file is compatible with the Platform(s)')),
        description=_(safe_unicode(
            'Please mark one or more platforms with which the '
            'uploaded file is compatible.')),
        value_type=schema.Choice(source='Platforms'),
        required=True,
    )

    directives.mode(information_further_file_uploads='display')
    primary('information_further_file_uploads')
    information_further_file_uploads = RichText(
        title=_(safe_unicode('Further File Uploads for this Release')),
        description=_(safe_unicode(
            'If you want to upload more files for this release, '
            'e.g. because there are files for other operating '
            "systems, you'll find the upload fields on the "
            "register 'Further Uploads' and 'Further More "
            "Uploads'.")),
        required=False,
    )

    model.fieldset('fileset1',
                   label=_(safe_unicode('Further File Uploads')),
                   fields=['filetitlefield1', 'addonfileextension1',
                           'file1', 'platform_choice1',
                           'filetitlefield2', 'addonfileextension2',
                           'file2', 'platform_choice2',
                           'filetitlefield3', 'addonfileextension3',
                           'file3', 'platform_choice3'],
                   )

    directives.mode(filetitlefield1='display')
    filetitlefield1 = schema.TextLine(
        title=_(safe_unicode('Second Release File')),
    )

    directives.mode(addonfileextension1='display')
    addonfileextension1 = schema.TextLine(
        title=_(safe_unicode(
            'The following file extensions are allowed for '
            'uploaded files (upper case and lower case and mix of '
            'both):')),
        defaultFactory=allowedaddonfileextensions,
    )

    file1 = NamedBlobFile(
        title=_(safe_unicode('The second file you want to upload (this is optional)')),
        description=_(safe_unicode('Please upload your file.')),
        required=False,
        constraint=validateaddonextension,
    )

    directives.widget(platform_choice1=CheckBoxFieldWidget)
    platform_choice1 = schema.List(
        title=_(safe_unicode('Second uploaded file is compatible with the Platform(s)')),
        description=_(safe_unicode(
            'Please mark one or more platforms with which the '
            'uploaded file is compatible.')),
        value_type=schema.Choice(source='Platforms'),
        required=False,
    )

    directives.mode(filetitlefield2='display')
    filetitlefield2 = schema.TextLine(
        title=_(safe_unicode('Third Release File')),
    )

    directives.mode(addonfileextension2='display')
    addonfileextension2 = schema.TextLine(
        title=_(safe_unicode(
            'The following file extensions are allowed for '
            'uploaded files (upper case and lower case and mix of '
            'both):')),
        defaultFactory=allowedaddonfileextensions,
    )

    file2 = NamedBlobFile(
        title=_(safe_unicode('The third file you want to upload (this is optional)')),
        description=_(safe_unicode('Please upload your file.')),
        required=False,
        constraint=validateaddonextension,
    )

    directives.widget(platform_choice2=CheckBoxFieldWidget)
    platform_choice2 = schema.List(
        title=_(safe_unicode('Third uploaded file is compatible with the Platform(s))')),
        description=_(safe_unicode(
            'Please mark one or more platforms with which the '
            'uploaded file is compatible.')),
        value_type=schema.Choice(source='Platforms'),
        required=False,
    )

    directives.mode(filetitlefield3='display')
    filetitlefield3 = schema.TextLine(
        title=_(safe_unicode('Fourth Release File')),
    )

    directives.mode(addonfileextension3='display')
    addonfileextension3 = schema.TextLine(
        title=_(safe_unicode(
            'The following file extensions are allowed for '
            'uploaded files (upper case and lower case and mix of '
            'both):')),
        defaultFactory=allowedaddonfileextensions,
    )

    file3 = NamedBlobFile(
        title=_(safe_unicode('The fourth file you want to upload (this is optional)')),
        description=_(safe_unicode('Please upload your file.')),
        required=False,
        constraint=validateaddonextension,
    )

    directives.widget(platform_choice3=CheckBoxFieldWidget)
    platform_choice3 = schema.List(
        title=_(safe_unicode('Fourth uploaded file is compatible with the Platform(s)')),
        description=_(safe_unicode(
            'Please mark one or more platforms with which the '
            'uploaded file is compatible.')),
        value_type=schema.Choice(source='Platforms'),
        required=False,
    )

    model.fieldset('fileset2',
                   label=_(safe_unicode('Further more file uploads')),
                   fields=['filetitlefield4', 'addonfileextension4',
                           'file4', 'platform_choice4',
                           'filetitlefield5', 'addonfileextension5',
                           'file5', 'platform_choice5'],
                   )

    directives.mode(filetitlefield4='display')
    filetitlefield4 = schema.TextLine(
        title=_(safe_unicode('Fifth Release File')),
    )

    directives.mode(addonfileextension4='display')
    addonfileextension4 = schema.TextLine(
        title=_(safe_unicode(
            'The following file extensions are allowed for '
            'uploaded files (upper case and lower case and mix of '
            'both):')),
        defaultFactory=allowedaddonfileextensions,
    )

    file4 = NamedBlobFile(
        title=_(safe_unicode('The fifth file you want to upload (this is optional)')),
        description=_(safe_unicode('Please upload your file.')),
        required=False,
        constraint=validateaddonextension,
    )

    directives.widget(platform_choice4=CheckBoxFieldWidget)
    platform_choice4 = schema.List(
        title=_(safe_unicode('Fifth uploaded file is compatible with the Platform(s)')),
        description=_(safe_unicode(
            'Please mark one or more platforms with which the '
            'uploaded file is compatible.')),
        value_type=schema.Choice(source='Platforms'),
        required=False,
    )

    directives.mode(filetitlefield5='display')
    filetitlefield5 = schema.TextLine(
        title=_(safe_unicode('Sixth Release File')),
    )

    directives.mode(addonfileextension5='display')
    addonfileextension5 = schema.TextLine(
        title=_(safe_unicode(
            'The following file extensions are allowed for '
            'uploaded files (upper case and lower case and mix of '
            'both):')),
        defaultFactory=allowedaddonfileextensions,
    )

    file5 = NamedBlobFile(
        title=_(safe_unicode('The sixth file you want to upload (this is optional)')),
        description=_(safe_unicode('Please upload your file.')),
        required=False,
        constraint=validateaddonextension,
    )

    directives.widget(platform_choice5=CheckBoxFieldWidget)
    platform_choice5 = schema.List(
        title=_(safe_unicode('Sixth uploaded file is compatible with the Platform(s)')),
        description=_(safe_unicode(
            'Please mark one or more platforms with which the '
            'uploaded file is compatible.')),
        value_type=schema.Choice(source='Platforms'),
        required=False,
    )

    @invariant
    def testingvalue(data):
        if data.source_code_inside != 1 and data.link_to_source is None:
            raise Invalid(_(safe_unicode(
                'You answered the question, whether the source '
                'code is inside your add-on with no '
                '(default answer). If this is the correct '
                'answer, please fill in the Link (URL) '
                'to the Source Code.')))

    @invariant
    def licensenotchoosen(value):
        if not value.licenses_choice:
            raise Invalid(_(safe_unicode('Please choose a license for your release.')))

    @invariant
    def compatibilitynotchoosen(data):
        if not data.compatibility_choice:
            raise Invalid(_(safe_unicode(
                'Please choose one or more compatible product '
                'versions for your release.')))

    @invariant
    def legaldeclarationaccepted(data):
        if data.accept_legal_declaration is not True:
            raise AcceptLegalDeclaration(_(
                safe_unicode(
                    'Please accept the Legal '
                    'Declaration about your Release '
                    'and your linked File')))


@indexer(IAddonRelease)
def addon_release_number(context, **kw):
    return context.releasenumber


def update_project_releases_compat_versions_on_creation(addonrelease, event):
    IReleasesCompatVersions(
        addonrelease.aq_parent).update(addonrelease.compatibility_choice)


def update_project_releases_compat_versions(addonrelease, event):
    pc = api.portal.get_tool(name='portal_catalog')
    query = '/'.join(addonrelease.aq_parent.getPhysicalPath())
    brains = pc.searchResults({  # noqa
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
                raise Invalid(_(
                    safe_unicode(
                        'The release number is already in use. '
                        'Please choose another one.')))


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

    def downloaddisclaimertitle(self):
        return api.portal.get_registry_record('collectiveaddons.title_legaldownloaddisclaimer')

    def downloaddisclaimertext(self):
        return api.portal.get_registry_record('collectiveaddons.legal_downloaddisclaimer')
