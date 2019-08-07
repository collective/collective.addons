# -*- coding: utf-8 -*-
from collective.addons import _
from plone.autoform.form import AutoExtensibleForm
from zope import interface
from zope import schema
from zope import component
from z3c.form import form, button
import re
from zope.interface import Invalid
from plone import api
from Products.statusmessages.interfaces import IStatusMessage

import logging
from z3c.form import field

from plone.formwidget.recaptcha.widget import ReCaptchaFieldWidget
from Acquisition import aq_inner
from zope.component import getMultiAdapter
from zope.interface import implementer


checkemail = re.compile(
    r"[a-zA-Z0-9._%-]+@([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,4}").match


def validateemail(value):
    if not checkemail(value):
        raise Invalid(_(u"Invalid email address"))
    return True

def validateprojectname(value):
    catalog = api.portal.get_tool('portal_catalog')
    project = catalog(
        portal_type='collective.addons.addonproject',
        Title=value
    )

    for brain in project[:1]:
        if brain.Title is None:
            raise Invalid(_(u"Not a valid project name. Please retry."))
        return True


logger = logging.getLogger(__name__)


class IReCaptchaForm(interface.Interface):

    captcha = schema.TextLine(
        title=u"ReCaptcha",
        description=u"",
        required=False
    )


class ReCaptcha(object):
    captcha = u""

    def __init__(self, context):
        self.context = context


class MailToAuthorSchema(interface.Interface):

    inquirerfirstname = schema.TextLine(
        title=_(u"Your First Name"),
        description=_(u"Please fill in your first name(s)")
    )

    inquirerfamilyname = schema.TextLine(
        title=_(u"Your Family Name"),
        description=_(u"Please fill in your familiy name")
    )

    inquireremailaddress = schema.TextLine(
        title=_(u"Your Email Address"),
        description=_(u"Please fill in your email address."),
        constraint=validateemail
    )

    projectname = schema.TextLine(
        title=_(u"Project Name"),
        description=_(u"The name of the project, to which author you want "
                      u"to send feedback."),
        constraint= validateprojectname
    )

    inquiry = schema.Text(
        title=_(u"Your Message To The Author"),
        description=_(u"What is your message to the author of the project? "
                      u"Your message is limited to 1000 characters."),
        max_length=1000
    )

@implementer(MailToAuthorSchema)
class MailToAuthorAdapter(object):
   # interface.implements(MailToAuthorSchema)
    component.adapts(interface.Interface)

    def __init__(self, context):
        self.inquirerfirstname = None
        self.inquirerfamilyname = None
        self.inquireremailaddress = None
        self.projectname = None
        self.inquiry = None


class MailToAuthorForm(AutoExtensibleForm, form.Form):
    schema = MailToAuthorSchema
    form_name = 'authormail_form'

    label = _(u"Mail To The Project Author")
    description = _(u"Contact the project author and send your feedback")

    fields = field.Fields(MailToAuthorSchema, IReCaptchaForm)
    fields['captcha'].widgetFactory = ReCaptchaFieldWidget

    def update(self):
        # disable Plone's editable border
        self.request.set('disable_border', True)

        # call the base class version - this is very important!
        super(MailToAuthorForm, self).update()

    @button.buttonAndHandler(_(u'Send Email'))
    def handleApply(self, action):
        data, errors = self.extractData()
        captcha = getMultiAdapter(
            (aq_inner(self.context), self.request),
            name='recaptcha'
        )

        if errors:
            self.status = self.formErrorsMessage
            return

        elif captcha.verify():
            logger.info('ReCaptcha validation passed.')
        else:
            logger.info(
                "Please validate the recaptcha field before sending the form."
            )
            IStatusMessage(self.request).addStatusMessage(
                _(u"Please validate the recaptcha field before sending "
                  u"the form."), "error"
            )
            return

        catalog = api.portal.get_tool('portal_catalog')
        project = catalog(
                      portal_type='collective.addons.addonproject',
                      Title=data['projectname']
        )

        for brain in project[:1]:
            if brain.getObject().contactAddress is not None:
                projectemail = brain.getObject().contactAddress

            else:
                projectemail = 'projects.foo.org'

        mailrecipient=(u"{}").format(projectemail)
        api.portal.send_email(
            recipient=mailrecipient,
            sender=(u"{} {} <{}>").format(data['inquirerfirstname'],
                                            data['inquirerfamilyname'],
                                            data['inquireremailaddress']),
            subject=(u"Your Project: {}").format(data['projectname']),
            body=(u"{}").format(data['inquiry'])


        )

        # Redirect back to the front page with a status message

        IStatusMessage(self.request).addStatusMessage(
                _(u"We send your message to the author of the project. It's "
                  u"on his choice, if he'll get back to you."),
                "info"
            )

        contextURL = self.context.absolute_url()
        self.request.response.redirect(contextURL)

    @button.buttonAndHandler(_(u"Cancel"))
    def handleCancel(self, action):
        """User cancelled. Redirect back to the front page.
            """
        contextURL = self.context.absolute_url()
        self.request.response.redirect(contextURL)
