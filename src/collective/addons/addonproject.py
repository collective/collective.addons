# -*- coding: utf-8 -*-
from collective.addons import _
from zope import schema
from plone.supermodel import model
from plone.supermodel.directives import primary
from plone.autoform import directives
from collective import dexteritytextindexer
from plone.app.textfield import RichText
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IContextSourceBinder
from zope.interface import directlyProvides
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory
from plone.namedfile.field import NamedBlobFile
from plone.namedfile.field import NamedBlobImage
from Products.Five import BrowserView

import re
import six



def vocabcategories(context):
    # For add forms

    # For other forms edited or displayed
    from collective.addons.addoncenter import IAddonCenter
    while context is not None and not IAddonCenter.providedBy(context):
        # context = aq_parent(aq_inner(context))
        context = context.__parent__

    category_list = []
    if context is not None and context.available_category:
        category_list = context.available_category

    terms = []
    for value in category_list:
        terms.append(SimpleTerm(value, token=value.encode('unicode_escape'),
                                title=value))

    return SimpleVocabulary(terms)

directlyProvides(vocabcategories, IContextSourceBinder)



def isNotEmptyCategory(value):
    if not value:
        raise Invalid(u'You have to choose at least one category for your '
                      u'project.')
    return True


checkemail = re.compile(
    r'[a-zA-Z0-9._%-]+@([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,4}').match


def validateemail(value):
    if not checkemail(value):
        raise Invalid(_(u'Invalid email address'))
    return True


@provider(IContextAwareDefaultFactory)
def allowedapdocfileextensions(context):
    return context.allowed_docfileextensions.replace("|", ", ")


@provider(IContextAwareDefaultFactory)
def allowedapimagefileextensions(context):
    return context.allowed_imageextension.replace("|", ", ")



def validatedocfileextension(value):
    catalog = api.portal.get_tool(name='portal_catalog')
    result=catalog.uniqueValuesFor('allowedapdocextensions')
    pattern = r'^.*\.{0}'.format(result)
    matches = re.compile(pattern, re.IGNORECASE).match
    if not matches(value.filename):
        raise Invalid(
            u'You could only upload files with an allowed file extension. '
            u'Please try again to upload a file with the correct file'
            u'extension.')
    return True


def validateimagefileextension(value):
    catalog = api.portal.get_tool(name='portal_catalog')
    result=catalog.uniqueValuesFor('allowedapimageextensions')
    pattern = r'^.*\.{0}'.format(result)
    matches = re.compile(pattern, re.IGNORECASE).match
    if not matches(value.filename):
        raise Invalid(
            u'You could only upload files with an allowed file extension. '
            u'Please try again to upload a file with the correct file'
            u'extension.')
    return True



class IAddonProject(model.Schema):
    directives.mode(information="display")
    information = schema.Text(
        title=_(u"Information"),
        description=_(u"The Dialog to create a new project consists of "
                      u"different register. Please go through this register "
                      u"and fill in the appropriate data for your project. "
                      u"The register 'Documentation' and its fields are "
                      u"optional.")
    )

    dexteritytextindexer.searchable('title')
    title = schema.TextLine(
        title=_(u"Title"),
        description=_(u"Project Title - minimum 5 and maximum 50 characters"),
        min_length=5,
        max_length=50
    )

    dexteritytextindexer.searchable('description')
    description = schema.Text(
        title=_(u"Project Summary"),
    )

    dexteritytextindexer.searchable('details')
    primary('details')
    details = RichText(
        title=_(u"Full Project Description"),
        required=False
    )

    model.fieldset('Categories',
                   label='Category / Categories',
                   fields=['category_choice']
                   )

    model.fieldset('logo_screenshot',
                   label='Logo / Screenshot',
                   fields=['eupimageextension', 'project_logo',
                           'eupimageextension1', 'screenshot']
                   )

    model.fieldset('documentation',
                   label='Documentation',
                   fields=['documentation_link', 'eupdocextension',
                           'documentation_file']
                   )

    dexteritytextindexer.searchable('category_choice')
    directives.widget(category_choice=CheckBoxFieldWidget)
    category_choice = schema.List(
        title=_(u"Choose your categories"),
        description=_(u"Please select the appropriate categories (one or "
                      u"more) for your project."),
        value_type=schema.Choice(source=vocabcategories),
        constraint=isNotEmptyCategory,
        required=True
    )

    contactAddress = schema.TextLine(
        title=_(u"Contact email-address"),
        description=_(u"Contact email-address for the project."),
        constraint=validateemail
    )

    homepage = schema.URI(
        title=_(u"Homepage"),
        description=_(u"If the project has an external home page, enter its "
                      u"URL (example: 'http://www.mysite.org')."),
        required=False
    )

    documentation_link = schema.URI(
        title=_(u"URL of documentation repository "),
        description=_(u"If the project has externally hosted "
                      u"documentation, enter its URL "
                      u"(example: 'http://www.mysite.org')."),
        required=False
    )

    directives.mode(eupdocextension='display')
    eupdocextension = schema.TextLine(
        title=_(u'The following file extensions are allowed for documentation '
                u'files (upper case and lower case and mix of both):'),
        defaultFactory=allowedapdocfileextensions,
    )

    documentation_file = NamedBlobFile(
        title=_(u"Dokumentation File"),
        description=_(u"If you have a Documentation in the file format 'PDF' "
                      u"or 'ODT' you could add it here."),
        required=False,
        constraint=validatedocfileextension
    )

    directives.mode(eupimageextension='display')
    eupimageextension = schema.TextLine(
        title=_(u'The following file extensions are allowed for project logo '
                u'files (upper case and lower case and mix of both):'),
        defaultFactory=allowedapimagefileextensions,
    )

    project_logo = NamedBlobImage(
        title=_(u"Logo"),
        description=_(u"Add a logo for the project (or organization/company) "
                      u"by clicking the 'Browse' button. You could provide "
                      u"an image of the file format 'png', 'gif' or 'jpg'."),
        required=False,
        constraint=validateimagefileextension
    )

    directives.mode(eupimageextension1='display')
    eupimageextension1 = schema.TextLine(
        title=_(u'The following file extensions are allowed for screenshot '
                u'files (upper case and lower case and mix of both):'),
        defaultFactory=allowedapimagefileextensions,
    )

    screenshot = NamedBlobImage(
        title=_(u"Screenshot of the Extension"),
        description=_(u"Add a screenshot by clicking the 'Browse' button. You "
                      u"could provide an image of the file format 'png', "
                      u"'gif' or 'jpg'."),
        required=False,
        constraint=validateimagefileextension
    )


class AddonProjectView(BrowserView):
    pass
