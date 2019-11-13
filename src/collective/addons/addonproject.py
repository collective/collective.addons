# -*- coding: utf-8 -*-
from collective import dexteritytextindexer
from collective.addons import _
from collective.addons import quote_chars
from plone import api
from plone.app.textfield import RichText
from plone.autoform import directives
from plone.namedfile.field import NamedBlobFile
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from plone.supermodel.directives import primary
from Products.Five import BrowserView
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
    return context.allowed_apdocfileextensions.replace('|', ', ')


@provider(IContextAwareDefaultFactory)
def allowedapimagefileextensions(context):
    return context.allowed_apimageextension.replace('|', ', ')


def validatedocfileextension(value):
    catalog = api.portal.get_tool(name='portal_catalog')
    result = catalog.uniqueValuesFor('allowedapdocextensions')
    pattern = r'^.*\.({0})'.format(result[0])
    matches = re.compile(pattern, re.IGNORECASE).match
    if not matches(value.filename):
        raise Invalid(
            u'You could only upload files with an allowed file extension. '
            u'Please try again to upload a file with the correct file'
            u'extension.')
    return True


def validateimagefileextension(value):
    catalog = api.portal.get_tool(name='portal_catalog')
    result = catalog.uniqueValuesFor('allowedapimageextensions')
    pattern = r'^.*\.({0})'.format(result[0])
    matches = re.compile(pattern, re.IGNORECASE).match
    if not matches(value.filename):
        raise Invalid(
            u'You could only upload files with an allowed file extension. '
            u'Please try again to upload a file with the correct file'
            u'extension.')
    return True


class ProvideScreenshotLogo(Invalid):
    __doc__ = _(u'Please add a screenshot or a logo to your project. You find '
                u'the appropriate fields below on this page.')


class IAddonProject(model.Schema):
    directives.mode(information='display')
    information = schema.Text(
        title=_(u'Information'),
        description=_(u'The Dialog to create a new project consists of '
                      u'different register. Please go through this register '
                      u'and fill in the appropriate data for your project. '
                      u"The register 'Documentation' and its fields are "
                      u'optional.'),
    )

    dexteritytextindexer.searchable('title')
    title = schema.TextLine(
        title=_(u'Title'),
        description=_(u'Project Title - minimum 5 and maximum 50 characters'),
        min_length=5,
        max_length=50,
    )

    dexteritytextindexer.searchable('description')
    description = schema.Text(
        title=_(u'Project Summary'),
    )

    dexteritytextindexer.searchable('details')
    primary('details')
    details = RichText(
        title=_(u'Full Project Description'),
        required=False,
    )

    model.fieldset('Categories',
                   label='Category / Categories',
                   fields=['category_choice'],
                   )

    model.fieldset('logo_screenshot',
                   label='Logo / Screenshot',
                   fields=['addonimageextension', 'project_logo',
                           'addonimageextension1', 'screenshot'],
                   )

    model.fieldset('documentation',
                   label='Documentation',
                   fields=['documentation_link', 'addondocextension',
                           'documentation_file'],
                   )

    dexteritytextindexer.searchable('category_choice')
    directives.widget(category_choice=CheckBoxFieldWidget)
    category_choice = schema.List(
        title=_(u'Choose your categories'),
        description=_(u'Please select the appropriate categories (one or '
                      u'more) for your project.'),
        value_type=schema.Choice(source=vocabcategories),
        constraint=isNotEmptyCategory,
        required=True,
    )

    addoncontactAddress = schema.TextLine(
        title=_(u'Contact email-address'),
        description=_(u'Contact email-address for the project.'),
        constraint=validateemail,
    )

    homepage = schema.URI(
        title=_(u'Homepage'),
        description=_(u'If the project has an external home page, enter its '
                      u"URL (example: 'http://www.mysite.org')."),
        required=False,
    )

    documentation_link = schema.URI(
        title=_(u'URL of documentation repository '),
        description=_(u'If the project has externally hosted '
                      u'documentation, enter its URL '
                      u"(example: 'http://www.mysite.org')."),
        required=False,
    )

    directives.mode(addondocextension='display')
    addondocextension = schema.TextLine(
        title=_(u'The following file extensions are allowed for documentation '
                u'files (upper case and lower case and mix of both):'),
        defaultFactory=allowedapdocfileextensions,
    )

    documentation_file = NamedBlobFile(
        title=_(u'Dokumentation File'),
        description=_(u"If you have a Documentation in the file format 'PDF' "
                      u"or 'ODT' you could add it here."),
        required=False,
        constraint=validatedocfileextension,
    )

    directives.mode(addonimageextension='display')
    addonimageextension = schema.TextLine(
        title=_(u'The following file extensions are allowed for project logo '
                u'files (upper case and lower case and mix of both):'),
        defaultFactory=allowedapimagefileextensions,
    )

    project_logo = NamedBlobImage(
        title=_(u'Logo'),
        description=_(u'Add a logo for the project (or organization/company) '
                      u"by clicking the 'Browse' button. You could provide "
                      u"an image of the file format 'png', 'gif' or 'jpg'."),
        required=False,
        constraint=validateimagefileextension,
    )

    directives.mode(addonimageextension1='display')
    addonimageextension1 = schema.TextLine(
        title=_(u'The following file extensions are allowed for screenshot '
                u'files (upper case and lower case and mix of both):'),
        defaultFactory=allowedapimagefileextensions,
    )

    screenshot = NamedBlobImage(
        title=_(u'Screenshot of the Add-on'),
        description=_(u"Add a screenshot by clicking the 'Browse' button. You "
                      u"could provide an image of the file format 'png', "
                      u"'gif' or 'jpg'."),
        required=False,
        constraint=validateimagefileextension,
    )

    @invariant
    def missingScreenshotOrLogo(data):
        if not data.screenshot and not data.project_logo:
            raise ProvideScreenshotLogo(_(u'Please add a screenshot or a logo '
                                          u'to your project page. You will '
                                          u'find the appropriate fields below '
                                          u'on this page.'))


def notifyProjectManager(self, event):
    state = api.content.get_state(self)
    if (self.__parent__.contactForCenter) is not None:
        mailsender = str(self.__parent__.contactForCenter)
    else:
        mailsender = api.portal.get_registry_record('plone.email_from_address')
    api.portal.send_email(
        recipient=('{0}').format(self.addoncontactAddress),
        sender=(u'{0} <{1}>').format('Admin of the Website', mailsender),
        subject=(u'Your Project {0}').format(self.title),
        body=(u'The status of your changed. '
              u'The new status is {0}').format(state),
    )


def notifyProjectManagerReleaseAdd(self, event):
    if (self.__parent__.contactForCenter) is not None:
        mailrecipient = str(self.__parent__.contactForCenter)
    else:
        mailrecipient = api.portal.get_registry_record(
            'plone.email_from_address')
    api.portal.send_email(
        recipient=('{0}').format(self.addoncontactAddress),
        sender=(u'{0} <{1}>').format('Admin of the Website', mailrecipient),
        subject=(u'Your Project [{0}: new Release added').format(self.title),
        body=(u'A new release was added to your project: '
              u"'{0}'").format(self.title),
    )


def notifyProjectManagerLinkedReleaseAdd(self, event):
    if (self.__parent__.contactForCenter) is not None:
        mailrecipient = str(self.__parent__.contactForCenter)
    else:
        mailrecipient = api.portal.get_registry_record(
            'plone.email_from_address')
    api.portal.send_email(
        recipient=('{0}').format(self.addoncontactAddress),
        sender=(u'{0} <{1}>').format('Admin of the Website', mailrecipient),
        subject=(u'Your Project {0}: new linked Release '
                 u'added').format(self.title),
        body=(u'A new linked release was added to your '
              u"project: '{0}'").format(self.title),
    )


def notifyAboutNewReviewlistentry(self, event):
    state = api.content.get_state(self)
    if (self.__parent__.contactForCenter) is not None:
        mailrecipient = str(self.__parent__.contactForCenter)
    else:
        mailrecipient = api.portal.get_registry_record(
            'plone.email_from_address')

    if state == 'pending':
        api.portal.send_email(
            recipient=mailrecipient,
            subject=(u'A Project with the title {0} was added to the review '
                     u'list').format(self.title),
            body='Please have a look at the review list and check if the '
                 'project is ready for publication. \n'
                 '\n'
                 'Kind regards,\n'
                 'The Admin of the Website',
        )


def textmodified_project(self, event):
    state = api.content.get_state(self)
    if (self.__parent__.contactForCenter) is not None:
        mailrecipient = str(self.__parent__.contactForCenter)
    else:
        mailrecipient = api.portal.get_registry_record(
            'plone.email_from_address')
    if state == 'published':
        if self.details is not None:
            detailed_description = self.details.output
        else:
            detailed_description = None

        api.portal.send_email(
            recipient=mailrecipient,
            sender=(u'{0} <{1}>').format(
                'Admin of the Website', mailrecipient),
            subject=(u'The content of the project {0} has '
                     u'changed').format(self.title),
            body=(u'The content of the project {0} has changed. Here you get '
                  u'the text of the description field of the '
                  u"project: \n'{1}\n\nand this is the text of the "
                  u"details field:\n{2}'").format(self.title,
                                                  self.description,
                                                  detailed_description),
        )


def notifyAboutNewProject(self, event):
    if (self.__parent__.contactForCenter) is not None:
        mailrecipient = str(self.__parent__.contactForCenter)
    else:
        mailrecipient = api.portal.get_registry_record(
            'plone.email_from_address')
    api.portal.send_email(
        recipient=mailrecipient,
        subject=(u'A Project with the title {0} was added').format(self.title),
        body='A member added a new project',
    )


class ValidateAddonProjectUniqueness(validator.SimpleFieldValidator):
    # Validate site-wide uniqueness of project titles.

    def validate(self, value):
        # Perform the standard validation first

        super(ValidateAddonProjectUniqueness, self).validate(value)
        if value is not None:
            catalog = api.portal.get_tool(name='portal_catalog')
            results = catalog({'Title': quote_chars(value),
                               'object_provides':
                                   IAddonProject.__identifier__})
            contextUUID = api.content.get_uuid(self.context)
            for result in results:
                if result.UID != contextUUID:
                    raise Invalid(_(u'The project title is already in use.'))


validator.WidgetValidatorDiscriminators(
    ValidateAddonProjectUniqueness,
    field=IAddonProject['title'],
)


class AddonProjectView(BrowserView):

    def canPublishContent(self):
        return api.user.has_permission('cmf.ModifyPortalContent', self.context)

    def releaseLicense(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        path = '/'.join(self.context.getPhysicalPath())
        idx_data = catalog.getIndexDataForUID(path)
        licenses = idx_data.get('releaseLicense')
        return (r for r in licenses)

    def projectCategory(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        path = '/'.join(self.context.getPhysicalPath())
        idx_data = catalog.getIndexDataForUID(path)
        category = idx_data.get('getCategories')
        return (r for r in category)

    def releaseCompatibility(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        path = '/'.join(self.context.getPhysicalPath())
        idx_data = catalog.getIndexDataForUID(path)
        compatibility = idx_data.get('getCompatibility')
        return (r for r in compatibility)

    def all_releases(self):
        """Get a list of all releases, ordered by version, starting with
           the latest.
        """

        current_path = '/'.join(self.context.getPhysicalPath())
        res = api.content.find(
            portal_type=('collective.addons.addonrelease',
                         'collective.addons.addonlinkedrelease'),
            path=current_path,
            sort_on='Date',
            sort_order='reverse')
        return [r.getObject() for r in res]

    def latest_release(self):
        """Get the most recent final release or None if none can be found.
        """

        context = self.context
        res = None

        res = api.content.find(
            portal_type=('collective.addons.addonrelease',
                         'collective.addons.addonlinkedrelease'),
            path='/'.join(context.getPhysicalPath()),
            review_state='final',
            sort_on='effective',
            sort_order='reverse')

        if not res:
            return None
        else:
            return res[0].getObject()

    def latest_release_date(self):
        """Get the date of the latest release
        """

        latest_release = self.latest_release()
        if latest_release:
            return self.context.toLocalizedTime(latest_release.effective())
        else:
            return None

    def latest_unstable_release(self):

        context = self.context
        res = None

        res = api.content.find(
            portal_type=('collective.addons.addonrelease',
                         'collective.addons.addonlinkedrelease'),
            path='/'.join(context.getPhysicalPath()),
            review_state=('alpha', 'beta', 'release-candidate'),
            sort_on='effective',
            sort_order='reverse')

        if not res:
            return None
        else:
            return res[0].getObject()
