# -*- coding: utf-8 -*-
from collective import dexteritytextindexer
from collective.addons import _
from collective.addons import quote_chars
from collective.addons.common import alloweddocextensions
from collective.addons.common import allowedimageextensions
from collective.addons.common import validatedocextension
from collective.addons.common import validateemail
from collective.addons.common import validateimageextension
from collective.addons.common import yesnochoice
from plone import api
from plone.app.textfield import RichText
from plone.autoform import directives
from plone.namedfile.field import NamedBlobFile
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from plone.supermodel.directives import primary
from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView
from Products.validation import V_REQUIRED  # noqa
from z3c.form import validator
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope import schema
from zope.interface import Invalid
from zope.interface import invariant


def isNotEmptyCategory(value):
    if not value:
        raise Invalid(safe_unicode(
            'You have to choose at least one category for your '
            'project.'))
    return True


class ProvideScreenshotLogo(Invalid):
    __doc__ = _(safe_unicode(
        'Please add a screenshot or a logo to your project. You find '
        'the appropriate fields below on this page.'))


class IAddonProject(model.Schema):
    directives.mode(information='display')
    information = schema.Text(
        title=_(safe_unicode('Information')),
        description=_(safe_unicode(
            'The Dialog to create a new project consists of '
            'different register. Please go through this register '
            'and fill in the appropriate data for your project. '
            "The register 'Documentation' and its fields are "
            'optional.')),
    )

    dexteritytextindexer.searchable('title')
    title = schema.TextLine(
        title=_(safe_unicode('Title')),
        description=_(safe_unicode('Project Title - minimum 5 and maximum 50 characters')),
        min_length=5,
        max_length=50,
    )

    dexteritytextindexer.searchable('description')
    description = schema.Text(
        title=_(safe_unicode('Project Summary')),
    )

    dexteritytextindexer.searchable('details')
    primary('details')
    details = RichText(
        title=_(safe_unicode('Full Project Description')),
        required=False,
    )

    model.fieldset('Categories',
                   label=_(safe_unicode('Category / Categories')),
                   fields=['category_choice'],
                   )

    model.fieldset('logo_screenshot',
                   label=_(safe_unicode('Logo / Screenshot')),
                   fields=['addonimageextension', 'project_logo',
                           'addonimageextension1', 'screenshot'],
                   )

    model.fieldset('documentation',
                   label=_(safe_unicode('Documentation')),
                   fields=['documentation_link', 'addondocextension',
                           'documentation_file'],
                   )

    dexteritytextindexer.searchable('category_choice')
    directives.widget(category_choice=CheckBoxFieldWidget)
    category_choice = schema.List(
        title=_(safe_unicode('Choose your categories')),
        description=_(safe_unicode(
            'Please select the appropriate categories (one or '
            'more) for your project.')),
        value_type=schema.Choice(source='Categories'),
        constraint=isNotEmptyCategory,
        required=True,
    )

    addoncontactAddress = schema.TextLine(
        title=_(safe_unicode('Contact email-address')),
        description=_(safe_unicode('Contact email-address for the project.')),
        constraint=validateemail,
    )

    make_addon_contact_address_public = schema.Choice(
        title=_(safe_unicode('Email Public?')),
        description=_(safe_unicode(
            'Please decide if your email address '
            'should be displayed on the project website.')),
        vocabulary=yesnochoice,
        required=True,
    )

    display_addon_user_name = schema.Choice(
        title=_(safe_unicode('Project Author Public?')),
        description=_(safe_unicode(
            'Please decide if your name '
            'should be displayed on the project website.')),
        vocabulary=yesnochoice,
        required=True,
    )

    homepage = schema.URI(
        title=_(safe_unicode('Homepage')),
        description=_(safe_unicode(
            'If the project has an external home page, enter its '
            "URL (example: 'http://www.mysite.org').")),
        required=False,
    )

    documentation_link = schema.URI(
        title=_(safe_unicode('URL of documentation repository ')),
        description=_(safe_unicode(
            'If the project has externally hosted '
            'documentation, enter its URL '
            "(example: 'http://www.mysite.org').")),
        required=False,
    )

    directives.mode(addondocextension='display')
    addondocextension = schema.TextLine(
        title=_(safe_unicode(
            'The following file extensions are allowed for documentation '
            'files (upper case and lower case and mix of both):')),
        defaultFactory=alloweddocextensions,
    )

    documentation_file = NamedBlobFile(
        title=_(safe_unicode('Dokumentation File')),
        description=_(safe_unicode(
            "If you have a Documentation in the file format 'PDF' "
            "or 'ODT' you could add it here.")),
        required=False,
        constraint=validatedocextension,
    )

    directives.mode(addonimageextension='display')
    addonimageextension = schema.TextLine(
        title=_(safe_unicode(
            'The following file extensions are allowed for project logo '
            'files (upper case and lower case and mix of both):')),
        defaultFactory=allowedimageextensions,
    )

    project_logo = NamedBlobImage(
        title=_(safe_unicode('Logo')),
        description=_(safe_unicode(
            'Add a logo for the project (or organization/company) '
            "by clicking the 'Browse' button. You could provide "
            "an image of the file format 'png', 'gif' or 'jpg'.")),
        required=False,
        constraint=validateimageextension,
    )

    directives.mode(addonimageextension1='display')
    addonimageextension1 = schema.TextLine(
        title=_(safe_unicode(
            'The following file extensions are allowed for screenshot '
            'files (upper case and lower case and mix of both):')),
        defaultFactory=allowedimageextensions,
    )

    screenshot = NamedBlobImage(
        title=_(safe_unicode('Screenshot of the Add-on')),
        description=_(safe_unicode(
            "Add a screenshot by clicking the 'Browse' button. You "
            "could provide an image of the file format 'png', "
            "'gif' or 'jpg'.")),
        required=False,
        constraint=validateimageextension,
    )

    @invariant
    def missingScreenshotOrLogo(data):
        if not data.screenshot and not data.project_logo:
            raise ProvideScreenshotLogo(_(
                safe_unicode(
                    'Please add a screenshot or a logo '
                    'to your project page. You will '
                    'find the appropriate fields below '
                    'on this page.')))


def notifyProjectManager(self, event):
    state = api.content.get_state(self)
    if (self.__parent__.contactForCenter) is not None:
        mailsender = str(self.__parent__.contactForCenter)
    else:
        mailsender = api.portal.get_registry_record('plone.email_from_address')
    api.portal.send_email(
        recipient=('{0}').format(self.addoncontactAddress),
        sender=(safe_unicode('{0} <{1}>')).format('Admin of the Website', mailsender),
        subject=(safe_unicode('Your Project {0}')).format(self.title),
        body=(safe_unicode(
            'The status of your changed. '
            'The new status is {0}')).format(state),
    )


def notifyProjectManagerReleaseAdd(self, event):
    if (self.__parent__.contactForCenter) is not None:
        mailrecipient = str(self.__parent__.contactForCenter)
    else:
        mailrecipient = api.portal.get_registry_record(
            'plone.email_from_address')
    api.portal.send_email(
        recipient=('{0}').format(self.addoncontactAddress),
        sender=(safe_unicode('{0} <{1}>')).format('Admin of the Website', mailrecipient),
        subject=(safe_unicode('Your Project [{0}: new Release added')).format(self.title),
        body=(safe_unicode(
            'A new release was added to your project: '
            "'{0}'")).format(self.title),
    )


def notifyProjectManagerLinkedReleaseAdd(self, event):
    if (self.__parent__.contactForCenter) is not None:
        mailrecipient = str(self.__parent__.contactForCenter)
    else:
        mailrecipient = api.portal.get_registry_record(
            'plone.email_from_address')
    api.portal.send_email(
        recipient=('{0}').format(self.addoncontactAddress),
        sender=(safe_unicode('{0} <{1}>')).format('Admin of the Website', mailrecipient),
        subject=(safe_unicode(
            'Your Project {0}: new linked Release '
            'added')).format(self.title),
        body=(safe_unicode(
            'A new linked release was added to your '
            "project: '{0}'")).format(self.title),
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
            subject=(safe_unicode(
                'A Project with the title {0} was added to the review '
                'list')).format(self.title),
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

    def email_public(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        path = '/'.join(self.context.getPhysicalPath())
        idx_data = catalog.getIndexDataForUID(path)
        public_email = idx_data.get('publicaddonemail')
        return (public_email)

    def name_public(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        path = '/'.join(self.context.getPhysicalPath())
        idx_data = catalog.getIndexDataForUID(path)
        public_name = idx_data.get('publicaddonname')
        return (public_name)

    def downloaddisclaimertitle(self):
        return api.portal.get_registry_record('collectiveaddons.title_legaldownloaddisclaimer')

    def downloaddisclaimertext(self):
        return api.portal.get_registry_record('collectiveaddons.legal_downloaddisclaimer')
