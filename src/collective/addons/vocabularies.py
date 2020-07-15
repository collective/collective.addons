# -*- coding: utf-8 -*-
from plone import api
from plone.app.vocabularies.terms import safe_simplevocabulary_from_values
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory


@provider(IVocabularyFactory)
def CategoriesVocabularyFactory(context):
    values = api.portal.get_registry_record('collectiveaddons.available_category')
    return safe_simplevocabulary_from_values(values)


@provider(IVocabularyFactory)
def LicensesVocabularyFactory(context):
    values = api.portal.get_registry_record('collectiveaddons.available_licenses')
    return safe_simplevocabulary_from_values(values)


@provider(IVocabularyFactory)
def VersionsVocabularyFactory(context):
    values = api.portal.get_registry_record('collectiveaddons.available_versions')
    return safe_simplevocabulary_from_values(values)


@provider(IVocabularyFactory)
def PlatformVocabularyFactory(context):
    values = api.portal.get_registry_record('collectiveaddons.available_platforms')
    return safe_simplevocabulary_from_values(values)
