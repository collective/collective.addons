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


def alloweddocextensions():
    return api.portal.get_registry_record('collectiveaddons.allowed_apdocfileextensions').replace('|', ', ')


def validateimageextension(value):
    result = str(api.portal.get_registry_record('collectiveaddons.allowed_apimageextension'))
    pattern = r'^.*\.({0})'.format(result)
    matches = re.compile(pattern, re.IGNORECASE).match
    if not matches(value.filename):
        raise Invalid(
            u'You could only upload files with an allowed file extension. '
            u'Please try again to upload a file with the correct file'
            u'extension.')
    return True


def validatedocextension(value):
    result = str(api.portal.get_registry_record('collectiveaddons.allowed_apdocfileextensions'))
    pattern = r'^.*\.({0})'.format(result[0])
    matches = re.compile(pattern, re.IGNORECASE).match
    if not matches(value.filename):
        raise Invalid(
            u'You could only upload files with an allowed file extension. '
            u'Please try again to upload a file with the correct file'
            u'extension.')
    return True


def validateaddonextension(value):
    result = str(api.portal.get_registry_record('collectiveaddons.allowed_allowedaddonfileextensions'))
    pattern = r'^.*\.({0})'.format(result[0])
    matches = re.compile(pattern, re.IGNORECASE).match
    if not matches(value.filename):
        raise Invalid(
            u'You could only upload files with an allowed file '
            u'extension. Please try again to upload a file with the '
            u'correct file extension.')
    return True
