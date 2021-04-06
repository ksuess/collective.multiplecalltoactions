"""List of call-to-actions."""
# coding: utf-8
from collective.multiplecalltoactions import _
from plone import schema
from plone.app.z3cform.widget import LinkFieldWidget
from plone.autoform.directives import widget
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from z3c.form.converter import BaseDataConverter
from z3c.form.interfaces import DISPLAY_MODE
from z3c.form.interfaces import HIDDEN_MODE
from z3c.form.interfaces import IDataConverter
from z3c.form.interfaces import NO_VALUE
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface
from zope.interface import provider
from zope.schema.fieldproperty import FieldProperty

from collective.z3cform.datagridfield.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.interfaces import IDataGridField
from collective.z3cform.datagridfield.row import DictRow

# from ftw.referencewidget.sources import ReferenceObjSourceBinder
# from ftw.referencewidget.widget import ReferenceWidgetFactory
# from plone.autoform import directives
# from z3c.relationfield.schema import RelationChoice


class ICalltoactionSchema(Interface):
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
        default=u'',
        missing_value=u'',
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


@implementer(ICalltoactionSchema)
class cta(object):
    ctalabel = FieldProperty(ICalltoactionSchema['ctalabel'])
    ctaurl = FieldProperty(ICalltoactionSchema['ctaurl'])
    ctasharing = FieldProperty(ICalltoactionSchema['ctasharing'])
    ctacategory = FieldProperty(ICalltoactionSchema['ctacategory'])

class ctaList(list):
    pass

class ctaListField(schema.List):
    """We need to have a unique class for the field list so that we
    can apply a custom adapter."""
    pass


@provider(IFormFieldProvider)
class ICallToActionBehavior(model.Schema):
    """Call to Action behavior with one list of cta."""

    color = schema.TextLine(
        title=_(u'Background Color of Call to Action'),
        description=_(u'Hexcode or name: #00aa22, magenta, yellow, ...'),
        default=u"#D9017A",
        required=False,
    )

    widget('ctas', DataGridFieldFactory, auto_append = True, allow_reorder=True)
    ctas = ctaListField(
        title=_(u'List of Call to Action'),
        required=False,
        value_type=DictRow(title=u"calltoaction", schema=ICalltoactionSchema),
        missing_value=[],
        default=[],
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
        print("*** setter of CallToActionBehavior")
        print(value)
        # import pdb; pdb.set_trace()
        self.context.ctas = value




@adapter(ctaListField, IDataGridField)
@implementer(IDataConverter)
class GridDataConverter(BaseDataConverter):
    """Convert between the ctaList object and the widget.
       If you are using objects, you must provide a custom converter
    """

    def toWidgetValue(self, value):
        """Simply pass the data through with no change"""
        rv = list()
        print("** toWidgetValue")
        for row in value:
            d = dict()
            for name, f in getFieldsInOrder(ICalltoactionSchema):
                d[name] = getattr(row, name)
            rv.append(d)
        return rv

    def toFieldValue(self, value):
        rv = ctaList()
        print("** toFieldValue")
        for row in value:
            d = dict()
            for name, f in getFieldsInOrder(ICalltoactionSchema):
                if row.get(name, NO_VALUE) != NO_VALUE:
                    d[name] = row.get(name)
            rv.append(cta(**d))
        return rv
