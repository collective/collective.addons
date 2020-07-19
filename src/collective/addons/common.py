# -*- coding: utf-8 -*-
from collective.addons import _
from plone import api
from zope.interface import Invalid
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

import re

yesnochoice = SimpleVocabulary(
    [SimpleTerm(value=0, title=_(u'No')),
     SimpleTerm(value=1, title=_(u'Yes'))],
)

checkemail = re.compile(
    r'[a-zA-Z0-9._%-]+@([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,4}').match


def validateemail(value):
    if not checkemail(value):
        raise Invalid(_(u'Invalid email address'))
    return True


def allowedaddonfileextensions():
    return api.portal.get_registry_record('collectiveaddons.allowed_addonfileextension').replace('|', ', ')


def allowedimageextensions():
    return api.portal.get_registry_record('collectiveaddons.allowed_apimageextension').replace('|', ', ')
