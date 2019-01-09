# coding: utf-8
"""Module where all interfaces, events and exceptions live."""

from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class ICollectiveCalltoactionLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class ICTAActivated(Interface):
    """Marker interface for content type that supports the behavior."""

    pass
