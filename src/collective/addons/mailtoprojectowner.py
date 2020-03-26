# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from collective.addons import _
from plone import api
from plone.autoform.form import AutoExtensibleForm
from plone.formwidget.recaptcha.widget import ReCaptchaFieldWidget
from plone.z3cform.layout import wrap_form
from Products.CMFPlone.utils import safe_unicode
from z3c.form import button
from z3c.form import field
from z3c.form import form
from zope import interface
from zope import schema
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.interface import implementer
from zope.interface import Invalid
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory

import logging
import re


checkemail = re.compile(
    r'[a-zA-Z0-9._%-]+@([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,4}').match


def validateemail(value):
    if not checkemail(value):
        raise Invalid(_(safe_unicode('Invalid email address')))
    return True


logger = logging.getLogger(__name__)


@provider(IContextAwareDefaultFactory)
def getprojectname(context):
    return context.title


class IReCaptchaForm(interface.Interface):

    captcha = schema.TextLine(
        title=safe_unicode('ReCaptcha'),
        description=safe_unicode(''),
        required=False,
    )


class ReCaptcha(object):
    captcha = safe_unicode('')

    def __init__(self, context):
        self.context = context


class MailToProjectOwnerSchema(interface.Interface):

    inquirerfirstname = schema.TextLine(
        title=_(safe_unicode('Your First Name')),
        description=_(safe_unicode('Please fill in your first name(s)')),
    )

    inquirerfamilyname = schema.TextLine(
        title=_(safe_unicode('Your Family Name')),
        description=_(safe_unicode('Please fill in your familiy name')),
    )

    inquireremailaddress = schema.TextLine(
        title=_(safe_unicode('Your Email Address')),
        description=_(safe_unicode('Please fill in your email address.')),
        constraint=validateemail,
    )

    projectname = schema.TextLine(
        title=_(safe_unicode('Project Name')),
        description=_(safe_unicode('The name of the project, to which '
                                   'author you want to send feedback.')),
        defaultFactory=getprojectname,
    )

    inquiry = schema.Text(
        title=_(safe_unicode('Your Message To The Author')),
        description=_(safe_unicode('What is your message to the author '
                                   'of the project? Your message is '
                                   'limited to 1000 characters.')),
        max_length=1000,
    )


@implementer(MailToProjectOwnerSchema)
@adapter(interface.Interface)
class MailToProjectOwnerAdapter(object):

    def __init__(self, context):
        self.inquirerfirstname = None
        self.inquirerfamilyname = None
        self.inquireremailaddress = None
        self.projectname = None
        self.inquiry = None


class MailToProjectOwnerForm(AutoExtensibleForm, form.Form):
    schema = MailToProjectOwnerSchema
    form_name = 'projectownermail_form'

    label = _(safe_unicode('Mail To The Project Owner'))
    description = _(safe_unicode('Contact the project owner and send '
                                 'your feedback'))

    fields = field.Fields(MailToProjectOwnerSchema, IReCaptchaForm)
    fields['captcha'].widgetFactory = ReCaptchaFieldWidget

    def update(self):
        # disable Plone's editable border
        self.request.set('disable_border', True)

        # call the base class version - this is very important!
        super(MailToProjectOwnerForm, self).update()

    @button.buttonAndHandler(_(safe_unicode('Send Email')))
    def handleApply(self, action):
        data, errors = self.extractData()
        captcha = getMultiAdapter(
            (aq_inner(self.context), self.request),
            name='recaptcha',
        )

        if errors:
            self.status = self.formErrorsMessage
            return

        elif captcha.verify():
            logger.info('ReCaptcha validation passed.')
        else:
            logger.info(
                'Please validate the recaptcha field before sending the form.',
            )
            api.portal.show_message(
                message=_(
                    safe_unicode('Please validate the recaptcha field '
                                 'before sending the form.')),
                request=self.request,
                type='error')
            return

        if api.portal.get_registry_record(
                'plone.email_from_address') is not None:
            contactaddress = api.portal.get_registry_record(
                'plone.email_from_address')

        catalog = api.portal.get_tool('portal_catalog')
        project = catalog(
            portal_type='collective.addons.addonproject',
            Title=data['projectname'],
        )

        for brain in project[:1]:
            if brain.getObject().addoncontactAddress is not None:
                projectemail = brain.getObject().addoncontactAddress

            else:
                projectemail = contactaddress

        mailrecipient = (safe_unicode('{0}')).format(projectemail)
        api.portal.send_email(
            recipient=mailrecipient,
            sender=(safe_unicode('{0} {1} <{2}>')).format(
                data['inquirerfirstname'],
                data['inquirerfamilyname'],
                data['inquireremailaddress']),
            subject=(safe_unicode('Your Project: {0}')).format(
                data['projectname']),
            body=(safe_unicode('{0}')).format(data['inquiry']),


        )

        # Redirect back to the front page with a status message

        api.portal.show_message(
            message=_(safe_unicode('We send your message to the author of '
                                   "the project. It's on her / his choice, "
                                   "if she'll / he'll get back to you.")),
            request=self.request,
            type='info')

        contextURL = self.context.absolute_url()
        self.request.response.redirect(contextURL)

    @button.buttonAndHandler(_(safe_unicode('Cancel')))
    def handleCancel(self, action):
        """User cancelled. Redirect back to the front page.
            """
        contextURL = self.context.absolute_url()
        self.request.response.redirect(contextURL)


ReCaptchaForm = wrap_form(MailToProjectOwnerForm)
