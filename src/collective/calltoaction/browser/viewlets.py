"""Viewlet class."""
from plone import api
from plone.app.layout.viewlets import common as base
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

# links starting with these URL scheme should not be redirected to
NON_REDIRECTABLE_URL_SCHEMES = [
    'mailto:',
    'tel:',
    'callto:',  # nonstandard according to RFC 3966. used for skype.
    'webdav:',
    'caldav:'
]

# links starting with these URL scheme should not be resolved to paths
NON_RESOLVABLE_URL_SCHEMES = NON_REDIRECTABLE_URL_SCHEMES + [
    'file:',
    'ftp:',
]

import logging
logger = logging.getLogger(__name__)


class CalltoactionViewlet(base.ViewletBase):
    """Show Call to Actions."""

    def update(self):
        super(CalltoactionViewlet, self).update()
        self.registry = getUtility(IRegistry)

    def ctasdictionary(self):
        """Get categorized ctas.

        registry:
        [
        {'ctalabel': u'Gottesdienste', 'ctasharing': False, 'ctacategory': 'komm_vorbei', 'ctaurl': 'https://www.zhkath.ch'},
        {'ctalabel': u'Orte der Ruhe', 'ctasharing': False, 'ctacategory': 'komm_vorbei', 'ctaurl': 'https://www.zhkath.ch'},
        {'ctalabel': u'Veranstaltungen', 'ctasharing': False, 'ctacategory': 'mach_mit', 'ctaurl': 'https://www.zhkath.ch'},
        {'ctalabel': u'Freiwilligenarbeit', 'ctasharing': False, 'ctacategory': 'mach_mit', 'ctaurl': 'https://www.zhkath.ch'},
        {'ctalabel': u'Kurse', 'ctasharing': False, 'ctacategory': 'mach_mit', 'ctaurl': 'https://www.zhkath.ch'},
        {'ctalabel': u'Sharing', 'ctasharing': True, 'ctacategory': 'mach_mit', 'ctaurl': None}]

        returns
        {'komm_vorbei': [{'ctacategory': 'komm_vorbei',
   'ctalabel': 'Gottesdienste',
   'ctasharing': False,
   'ctaurl': 'https://www.zhkath.ch'},
  {'ctacategory': 'komm_vorbei',
   'ctalabel': 'Orte der Ruhe',
   'ctasharing': False,
   'ctaurl': 'https://www.zhkath.ch'}],
 'mach_mit': [{'ctacategory': 'mach_mit',
   'ctalabel': 'Veranstaltungen',
   'ctasharing': False,
   'ctaurl': 'https://www.zhkath.ch'},
  {'ctacategory': 'mach_mit',
   'ctalabel': 'Freiwilligenarbeit',
   'ctasharing': False,
   'ctaurl': 'https://www.zhkath.ch'},
  {'ctacategory': 'mach_mit',
   'ctalabel': 'Kurse',
   'ctasharing': False,
   'ctaurl': 'https://www.zhkath.ch'},
  {'ctacategory': 'mach_mit',
   'ctalabel': 'Sharing',
   'ctasharing': True,
   'ctaurl': None}]}
   """
        ctas = self.context.ctas
        dct = {}
        if not ctas:
            return
        for el in ctas:
            dct[el['ctacategory']] = []
        for el in ctas:
            dct[el['ctacategory']].append(el)
        # print("ctasdictionary {}".format(dct))

        factory = getUtility(
            IVocabularyFactory,
            'collective.calltoaction.CtoCategoryVocabulary')
        vocabulary = factory()
        # term = vocabulary.getTerm('value1')
        # value, token, term =  (term.value, term.token, term.title)

        result = {}
        for k in dct:
            result[vocabulary.getTerm(k).title] = dct[k]

        # print("ctasdictionary {}".format(result))
        return result

    def _url_uses_scheme(self, schemes, url=None):
        url = url  # or self.context.remoteUrl
        for scheme in schemes:
            if url.startswith(scheme):
                return True
        return False

    def absolute_target_url(self, urlstring):
        """Compute the absolute target URL."""
        url = urlstring  # self.url()

        if self._url_uses_scheme(NON_RESOLVABLE_URL_SCHEMES, url):
            # For non http/https url schemes, there is no path to resolve.
            return url

        if url.startswith('.'):
            # we just need to adapt ../relative/links, /absolute/ones work
            # anyway -> this requires relative links to start with ./ or
            # ../
            context_state = self.context.restrictedTraverse(
                '@@plone_context_state'
            )
            url = '/'.join([
                context_state.canonical_object_url(),
                url
            ])
        if url.startswith('${portal_url}'):
            url = url.replace('${portal_url}', '')
            url = '/'.join([
                api.portal.get().absolute_url(),
                url
            ])
        else:
            if not (url.startswith('http://') or url.startswith('https://')):
                url = self.request.physicalPathToURL(url)

        return url

    def getDataServices(self):
        """<div class='shariff'
            data-services='twitter, facebook, googleplus, mail, info'
        """
        dataservices_default = ('twitter', 'mail',)
        shariff_dataservices = self.registry.get(
            'collective.calltoaction.shariff_services',
            dataservices_default)
        return shariff_dataservices

    def style(self):
        color = getattr(self.context, 'color', 'transparent')
        return 'background-color: {}'.format(color)
