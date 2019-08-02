# -*- coding: utf-8 -*-
from collective.addons import _
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


yesnochoice = SimpleVocabulary(
    [SimpleTerm(value=0, title=_(u'No')),
     SimpleTerm(value=1, title=_(u'Yes')), ]
)
