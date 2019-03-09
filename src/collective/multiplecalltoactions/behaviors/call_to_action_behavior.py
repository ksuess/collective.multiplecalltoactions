"""List of call-to-actions."""
# coding: utf-8
from collective.multiplecalltoactions import _
from plone import schema
from plone.app.z3cform.widget import LinkFieldWidget
from plone.autoform.directives import widget
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider

from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield import DictRow
from zope import interface

# from ftw.referencewidget.sources import ReferenceObjSourceBinder
# from ftw.referencewidget.widget import ReferenceWidgetFactory
# from plone.autoform import directives
# from z3c.relationfield.schema import RelationChoice


class ICalltoactionSchema(interface.Interface):
    """Call to action.

    internal link, external link, sharing
    """

    ctalabel = schema.TextLine(
        title=_(u'Label'),
        required=False,
        default=u'',
        missing_value=u'call to action',
        )
    widget('ctaurl', LinkFieldWidget)
    ctaurl = schema.TextLine(
        title=_(u'Target of call to action'),
        required=False,
        default=None,  # u'',
        # missing_value=u'',
        )
    ctasharing = schema.Bool(
        title=_(u'Sharing'),
        required=False,
        default=False,
        missing_value=False,
    )
    ctacategory = schema.Choice(
        title=_(u'Category'),
        required=True,
        vocabulary='collective.multiplecalltoactions.CtoCategoryVocabulary'
    )

    # directives.widget(link=ReferenceWidgetFactory)
    # link = RelationChoice(
    #     title=u'Link',
    #     source=ReferenceObjSourceBinder(),
    #     required=False,
    #     )


@provider(IFormFieldProvider)
class ICallToActionBehavior(model.Schema):
    """Call to Action behavior with one list of cta."""

    color = schema.TextLine(
        title=_(u'Background Color of Call to Action'),
        description=_(u'Hexcode or name: #00aa22, magenta, yellow, ...'),
        default=u"#D9017A",
        required=False,
    )

    widget('ctas', DataGridFieldFactory, auto_append = False, allow_reorder=True)
    ctas = schema.List(
        title=_(u'List of Call to Action'),
        required=False,
        value_type=DictRow(title=u"calltoaction", schema=ICalltoactionSchema),
        missing_value=[],
        readonly=False
    )

    model.fieldset(
        'options',
        fields=['color', 'ctas']
    )


@implementer(ICallToActionBehavior)
@adapter(IDexterityContent)
class CallToActionBehavior(object):
    """Adapter."""

    def __init__(self, context):
        self.context = context

    @property
    def color(self):
        if hasattr(self.context, 'color'):
            return self.context.color
        return None

    @color.setter
    def color(self, value):
        self.context.color = value


    @property
    def ctas(self):
        if hasattr(self.context, 'ctas'):
            return self.context.ctas
        return None

    @ctas.setter
    def ctas(self, value):
        self.context.ctas = value
