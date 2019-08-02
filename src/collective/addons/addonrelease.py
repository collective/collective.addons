# -*- coding: utf-8 -*-
from collective.addons import _
from zope import schema
from plone.supermodel import model
from plone.autoform import directives
from plone.supermodel.directives import primary
from plone.app.textfield import RichText
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory
from Products.Five import BrowserView
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.interface import directlyProvides
from Acquisition import aq_inner, aq_parent
from plone.namedfile.field import NamedBlobFile
from plone import api
from zope.interface import Invalid

import re
import six


@provider(IContextAwareDefaultFactory)
def getContainerTitle(self):
    return (self.aq_inner.title)


@provider(IContextAwareDefaultFactory)
def contactinfoDefault(context):
    return context.contactAddress


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
    return context.allowed_addonfileextension.replace("|", ", ")


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

yesnochoice = SimpleVocabulary(
    [SimpleTerm(value=0, title=_(u'No')),
     SimpleTerm(value=1, title=_(u'Yes')), ]
)


def validateaddonfileextension(value):
    catalog = api.portal.get_tool(name='portal_catalog')
    result = catalog.uniqueValuesFor('allowedaddonfileextensions')
    pattern = r'^.*\.{0}'.format(result[0])
    matches = re.compile(pattern, re.IGNORECASE).match
    if not matches(value.filename):
        raise Invalid(
            u'You could only upload files with an allowed file '
            u'extension. Please try again to upload a file with the '
            u'correct file extension.')
    return True





class IAddonRelease(model.Schema):
    directives.mode(information="display")
    information = schema.Text(
        title=_(u"Information"),
        description=_(
            u"This Dialog to create a new release consists of different "
            u"register. Please go through this register and fill in the "
            u"appropriate data for your release. This register 'Default' "
            u"provide fields for general information of your release. The "
            u"next register 'compatibility' is the place to submit "
            u"information about the versions with which your release file(s) "
            u"is / are compatible. The following register asks for some "
            u"legal informations. The next register File Upload' provide a "
            u"field to upload your release file. The further register are "
            u"optional. There is the opportunity to upload further release "
            u"files (for different platforms).")
    )

    directives.mode(projecttitle='hidden')
    projecttitle = schema.TextLine(
        title=_(u"The Computed Project Title"),
        description=_(
            u"The release title will be computed from the parent project "
            u"title"),
        defaultFactory=getContainerTitle
    )

    releasenumber = schema.TextLine(
        title=_(u"Release Number"),
        description=_(u"Release Number (up to twelf chars)"),
        default=_(u"1.0"),
        max_length=12
    )

    description = schema.Text(
        title=_(u"Release Summary"),
    )

    primary('details')
    details = RichText(
        title=_(u"Full Release Description"),
        required=False
    )

    primary('changelog')
    changelog = RichText(
        title=_(u"Changelog"),
        description=_(
            u"A detailed log of what has changed since the previous release."),
        required=False,
    )


    model.fieldset('compatibility',
                   label=u"Compatibility",
                   fields=['compatibility_choice'])

    model.fieldset('legal',
                   label=u"Legal",
                   fields=['licenses_choice', 'title_declaration_legal',
                           'declaration_legal', 'accept_legal_declaration',
                           'source_code_inside', 'link_to_source'])


    directives.widget(licenses_choice=CheckBoxFieldWidget)
    licenses_choice = schema.List(
        title=_(u'License of the uploaded file'),
        description=_(
            u"Please mark one or more licenses you publish your release."),
        value_type=schema.Choice(source=vocabAvailLicenses),
        required=True,
    )

    directives.widget(compatibility_choice=CheckBoxFieldWidget)
    compatibility_choice = schema.List(
        title=_(u"Compatible With Versions Of The Product"),
        description=_(
            u"Please mark one or more program versions with which this "
            u"release is compatible with."),
        value_type=schema.Choice(source=vocabAvailVersions),
        required=True,
        default=[]
    )

    directives.mode(title_declaration_legal='display')
    title_declaration_legal = schema.TextLine(
        title=_(u""),
        required=False,
        defaultFactory=legal_declaration_title
    )

    directives.mode(declaration_legal='display')
    declaration_legal = schema.Text(
        title=_(u""),
        required=False,
        defaultFactory=legal_declaration_text

    )

    accept_legal_declaration = schema.Bool(
        title=_(u"Accept the above legal disclaimer"),
        description=_(
            u"Please declare that you accept the above legal disclaimer"),
        required=True
    )

    contact_address2 = schema.TextLine(
        title=_(u"Contact email-address"),
        description=_(u"Contact email-address for the project."),
        required=False,
        defaultFactory=contactinfoDefault
    )

    source_code_inside = schema.Choice(
        title=_(u"Is The Source Code Inside The Addon?"),
        vocabulary=yesnochoice,
        required=True
    )

    link_to_source = schema.URI(
        title=_(u"Please fill in the Link (URL) to the Source Code"),
        required=False
    )


    model.fieldset('fileupload',
                   label=u"Fileupload",
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
        title=_(u"The irst file you want to upload."),
        description=_(u"Please upload your file."),
        required=True,
        constraint=validateaddonfileextension
    )

    directives.widget(platform_choice=CheckBoxFieldWidget)
    platform_choice = schema.List(
        title=_(u"First uploaded file is compatible with the Platform(s)"),
        description=_(u"Please mark one or more platforms with which the "
                      u"uploaded file is compatible."),
        value_type=schema.Choice(source=vocabAvailPlatforms),
        required=True,
    )

    directives.mode(information_further_file_uploads='display')
    primary('information_further_file_uploads')
    information_further_file_uploads = RichText(
        title=_(u"Further File Uploads for this Release"),
        description=_(u"If you want to upload more files for this release, "
                      u"e.g. because there are files for other operating "
                      u"systems, you'll find the upload fields on the "
                      u"register 'Further Uploads' and 'Further More "
                      u"Uploads'."),
        required=False
    )

    model.fieldset('fileset1',
                   label=u"Further File Uploads",
                   fields=['filetitlefield1', 'addonfileextension1',
                           'file1', 'platform_choice1',
                           'filetitlefield2', 'addonfileextension2',
                           'file2', 'platform_choice2',
                           'filetitlefield3', 'addonfileextension3',
                           'file3', 'platform_choice3']
                   )

    directives.mode(filetitlefield1='display')
    filetitlefield1 = schema.TextLine(
        title=_(u"Second Release File"),
    )

    directives.mode(addonfileextension1='display')
    addonfileextension1 = schema.TextLine(
        title=_(u'The following file extensions are allowed for '
                u'uploaded files (upper case and lower case and mix of '
                u'both):'),
        defaultFactory=allowedaddonfileextensions,
    )

    file1 = NamedBlobFile(
        title=_(u"The second file you want to upload (this is optional)"),
        description=_(u"Please upload your file."),
        required=False,
        constraint=validateaddonfileextension
    )

    directives.widget(platform_choice1=CheckBoxFieldWidget)
    platform_choice1 = schema.List(
        title=_(u"Second uploaded file is compatible with the Platform(s)"),
        description=_(u"Please mark one or more platforms with which the "
                      u"uploaded file is compatible."),
        value_type=schema.Choice(source=vocabAvailPlatforms),
        required=False,
    )

    directives.mode(filetitlefield2='display')
    filetitlefield2 = schema.TextLine(
        title=_(u"Third Release File"),
    )

    directives.mode(addonfileextension2='display')
    addonfileextension2 = schema.TextLine(
        title=_(u'The following file extensions are allowed for '
                u'uploaded files (upper case and lower case and mix of '
                u'both):'),
        defaultFactory=allowedaddonfileextensions,
    )

    file2 = NamedBlobFile(
        title=_(u"The third file you want to upload (this is optional)"),
        description=_(u"Please upload your file."),
        required=False,
        constraint=validateaddonfileextension
    )

    directives.widget(platform_choice2=CheckBoxFieldWidget)
    platform_choice2 = schema.List(
        title=_(u"Third uploaded file is compatible with the Platform(s))"),
        description=_(u"Please mark one or more platforms with which the "
                      u"uploaded file is compatible."),
        value_type=schema.Choice(source=vocabAvailPlatforms),
        required=False,
    )

    directives.mode(filetitlefield3='display')
    filetitlefield3 = schema.TextLine(
        title=_(u"Fourth Release File"),
    )

    directives.mode(addonfileextension3='display')
    addonfileextension3 = schema.TextLine(
        title=_(u'The following file extensions are allowed for '
                u'uploaded files (upper case and lower case and mix of '
                u'both):'),
        defaultFactory=allowedaddonfileextensions,
    )

    file3 = NamedBlobFile(
        title=_(u"The fourth file you want to upload (this is optional)"),
        description=_(u"Please upload your file."),
        required=False,
        constraint=validateaddonfileextension
    )

    directives.widget(platform_choice3=CheckBoxFieldWidget)
    platform_choice3 = schema.List(
        title=_(u"Fourth uploaded file is compatible with the Platform(s)"),
        description=_(u"Please mark one or more platforms with which the "
                      u"uploaded file is compatible."),
        value_type=schema.Choice(source=vocabAvailPlatforms),
        required=False,
    )

    model.fieldset('fileset2',
                   label=u"Further More File Uploads",
                   fields=['filetitlefield4', 'addonfileextension4',
                           'file4', 'platform_choice4',
                           'filetitlefield5', 'addonfileextension5',
                           'file5', 'platform_choice5']
                   )

    directives.mode(filetitlefield4='display')
    filetitlefield4 = schema.TextLine(
        title=_(u"Fifth Release File"),
    )

    directives.mode(addonfileextension4='display')
    addonfileextension4 = schema.TextLine(
        title=_(u'The following file extensions are allowed for '
                u'uploaded files (upper case and lower case and mix of '
                u'both):'),
        defaultFactory=allowedaddonfileextensions,
    )

    file4 = NamedBlobFile(
        title=_(u"The fifth file you want to upload (this is optional)"),
        description=_(u"Please upload your file."),
        required=False,
        constraint=validateaddonfileextension
    )

    directives.widget(platform_choice4=CheckBoxFieldWidget)
    platform_choice4 = schema.List(
        title=_(u"Fifth uploaded file is compatible with the Platform(s)"),
        description=_(u"Please mark one or more platforms with which the "
                      u"uploaded file is compatible."),
        value_type=schema.Choice(source=vocabAvailPlatforms),
        required=False,
    )

    directives.mode(filetitlefield5='display')
    filetitlefield5 = schema.TextLine(
        title=_(u"Sixth Release File"),
    )

    directives.mode(addonfileextension5='display')
    addonfileextension5 = schema.TextLine(
        title=_(u'The following file extensions are allowed for '
                u'uploaded files (upper case and lower case and mix of '
                u'both):'),
        defaultFactory=allowedaddonfileextensions,
    )

    file5 = NamedBlobFile(
        title=_(u"The sixth file you want to upload (this is optional)"),
        description=_(u"Please upload your file."),
        required=False,
        constraint=validateaddonfileextension
    )

    directives.widget(platform_choice5=CheckBoxFieldWidget)
    platform_choice5 = schema.List(
        title=_(u"Sixth uploaded file is compatible with the Platform(s)"),
        description=_(u"Please mark one or more platforms with which the "
                      u"uploaded file is compatible."),
        value_type=schema.Choice(source=vocabAvailPlatforms),
        required=False,
    )






class TAddonReleaseView(BrowserView):
    pass