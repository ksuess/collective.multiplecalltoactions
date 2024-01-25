"""Vocabularies."""
from plone import api
from plone.i18n.normalizer.interfaces import IIDNormalizer
from zope.component import getUtility
# from zope.interface import provider
# from zope.schema.interfaces import IVocabularyFactory
# from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


def CtoCategoryVocabularyFactory(context=None):
    """Vocabulary for Call to Action category."""
    normalizer = getUtility(IIDNormalizer)

    terms = []
    registryvalue = \
        api.portal.get_registry_record(
            'collective.multiplecalltoactions.ctocategories') \
        or {'default': 'Default'}
    for el in registryvalue:
        el_lower = normalizer.normalize(el)
        terms.append(SimpleVocabulary.createTerm(
            el_lower, el_lower, registryvalue[el]))
    return SimpleVocabulary(terms)
