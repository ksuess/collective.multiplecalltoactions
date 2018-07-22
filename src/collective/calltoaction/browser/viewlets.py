"""todo viewlet class."""

from plone.app.layout.viewlets import common as base
# from plone import api

import logging
logger = logging.getLogger(__name__)


class CalltoactionViewlet(base.ViewletBase):
    """Show Call to Actions."""
