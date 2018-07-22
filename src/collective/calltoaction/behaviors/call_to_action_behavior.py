"""List of call-to-actions."""
# coding: utf-8
from collective.calltoaction import _
from plone import schema
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider

from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield import DictRow
from z3c.form import field
from z3c.form import form
from z3c.form.form import extends
from zope import interface


class ICalltoactionSchema(interface.Interface):
    """Call to action.

    internal link, external link, sharing
    """

    one = schema.TextLine(title=u"One")
    two = schema.TextLine(title=u"Two")
    three = schema.TextLine(title=u"Three")


@provider(IFormFieldProvider)
class ICallToActionBehavior(model.Schema):
    """Call to Action behavior with one list of cto."""

    ctos = schema.List(
        title=_(u'List of Call to Action'),
        required=False,
        value_type=DictRow(title=u"calltoaction", schema=ICalltoactionSchema)
    )


@implementer(ICallToActionBehavior)
@adapter(IDexterityContent)
class CallToActionBehavior(object):
    def __init__(self, context):
        self.context = context

    @property
    def ctos(self):
        if hasattr(self.context, 'ctos'):
            return self.context.ctos
        return None

    @ctos.setter
    def ctos(self, value):
        self.context.ctos = value
