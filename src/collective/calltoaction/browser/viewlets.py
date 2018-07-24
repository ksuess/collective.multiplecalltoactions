"""todo viewlet class."""

from plone.app.layout.viewlets import common as base
# from plone import api

import logging
logger = logging.getLogger(__name__)


class CalltoactionViewlet(base.ViewletBase):
    """Show Call to Actions."""

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
        for el in ctas:
            dct[el['ctacategory']] = []
        for el in ctas:
            dct[el['ctacategory']].append(el)
        print("ctasdictionary {}".format(dct))
        return dct
