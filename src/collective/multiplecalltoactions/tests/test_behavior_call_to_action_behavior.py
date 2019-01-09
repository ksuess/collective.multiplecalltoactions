# -*- coding: utf-8 -*-
from collective.multiplecalltoactions.behaviors.call_to_action_behavior import ICallToActionBehavior
from collective.multiplecalltoactions.testing import COLLECTIVE_CALLTOACTION_INTEGRATION_TESTING  # noqa
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.behavior.interfaces import IBehavior
from zope.component import getUtility

import unittest


class CallToActionBehaviorIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_CALLTOACTION_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_behavior_call_to_action_behavior(self):
        behavior = getUtility(IBehavior, 'collective.multiplecalltoactions.call_to_action_behavior')
        self.assertEqual(
            behavior.marker,
            ICallToActionBehavior,
        )
        behavior_name = 'collective.multiplecalltoactions.behaviors.call_to_action_behavior.ICallToActionBehavior'
        behavior = getUtility(IBehavior, behavior_name)
        self.assertEqual(
            behavior.marker,
            ICallToActionBehavior,
        )
