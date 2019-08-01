# -*- coding: utf-8 -*-
from collective.addons import _
from zope import schema
from plone.supermodel import model
from plone.autoform import directives
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory
from plone.app.textfield import RichText
from plone.supermodel.directives import primary
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.interface import directlyProvides
from Acquisition import aq_inner, aq_parent
from zope.schema.interfaces import IContextSourceBinder
from plone import api
from zope.interface import Invalid
from Products.Five import BrowserView

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


def validatelinkedaddonfileextension(value):
    catalog = api.portal.get_tool(name='portal_catalog')
    result = catalog.uniqueValuesFor('allowedaddonfileextensions')
    pattern = r'^.*\.{0}'.format(result[0])
    matches = re.compile(pattern, re.IGNORECASE).match
    if not matches(value):
        raise Invalid(
            u'You could only upload files with an allowed file '
            u'extension. Please try again to upload a file with the '
            u'correct file extension.')
    return True




class IAddonLinkedRelease(model.Schema):
    directives.mode(information="display")
    information = schema.Text(
        title=_(u"Information"),
        description=_(
            u"This Dialog to create a new release consists of different "
            u"register. Please go through this register and fill in the "
            u"appropriate data for your linked release. This register "
            u"'Default' provide fields for general information of your "
            u"linked release. The next register 'compatibility' is the "
            u"place to submit information about the versions with which "
            u"your linked release file(s) is / are compatible. The "
            u"following register asks for some legal informations. "
            u"The next register 'Linked File' provide a field to link "
            u"your release file. The further register are optional. "
            u"There is the opportunity to link further release files "
            u"(for different platforms).")
    )

    directives.mode(projecttitle='hidden')
    projecttitle = schema.TextLine(
        title=_(u"The Computed Project Title"),
        description=_(
            u"The linked release title will be computed from the parent project "
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
        description=_(u"A detailed log of what has changed since the "
                      u"previous release."),
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
        description=_(u"Please mark one or more licenses you publish your "
                      u"release."),
        value_type=schema.Choice(source=vocabAvailLicenses),
        required=True,
    )

    directives.widget(compatibility_choice=CheckBoxFieldWidget)
    compatibility_choice = schema.List(
        title=_(u"Compatible with versions of LibreOffice"),
        description=_(u"Please mark one or more program versions with which "
                      u"this release is compatible with."),
        value_type=schema.Choice(source=vocabAvailVersions),
        required=True,
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
        description=_(u"Please declare that you accept the above legal "
                      u"disclaimer."),
        required=True
    )

    contact_address2 = schema.TextLine(
        title=_(u"Contact email-address"),
        description=_(u"Contact email-address for the project."),
        required=False,
        defaultFactory=contactinfoDefault
    )

    source_code_inside = schema.Choice(
        title=_(u"Is the source code inside the add-on?"),
        vocabulary=yesnochoice,
        required=True
    )

    link_to_source = schema.URI(
        title=_(u"Please fill in the Link (URL) to the Source Code."),
        required=False
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
        defaultFactory=allowedaddonfileextensions,
    )


    link_to_file = schema.URI(
        title=_(u"The Link to the file of the release"),
        description=_(u"Please insert a link to your add-on file."),
        required=True,
        constraint=validatelinkedaddonfileextension,
    )

    external_file_size = schema.Float(
        title=_(u"The size of the external hosted file"),
        description=_(
            u"Please fill in the size in kilobyte of the external hosted "
            u"file (e.g. 633, if the size is 633 kb)"),
        required=False
    )

    directives.widget(platform_choice=CheckBoxFieldWidget)
    platform_choice = schema.List(
        title=_(u"First linked file is compatible with the Platform(s)"),
        description=_(u"Please mark one or more platforms with which the "
                      u"uploaded file is compatible."),
        value_type=schema.Choice(source=vocabAvailPlatforms),
        required=True,
    )

    directives.mode(information_further_file_uploads='display')
    primary('information_further_file_uploads')
    information_further_file_uploads = RichText(
        title=_(u"Further linked files for this Release"),
        description=_(
            u"If you want to link more files for this release, e.g. because "
            u"there are files for other operating systems, you'll find the "
            u"fields to link this files on the next registers, e.g. "
            u"'Second linked file' for this Release'."),
        required=False
    )



class TAddonLinkedReleaseView(BrowserView):
    pass
