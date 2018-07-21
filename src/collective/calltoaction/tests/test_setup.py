# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from collective.calltoaction.testing import COLLECTIVE_CALLTOACTION_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.calltoaction is properly installed."""

    layer = COLLECTIVE_CALLTOACTION_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.calltoaction is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'collective.calltoaction'))

    def test_browserlayer(self):
        """Test that ICollectiveCalltoactionLayer is registered."""
        from collective.calltoaction.interfaces import (
            ICollectiveCalltoactionLayer)
        from plone.browserlayer import utils
        self.assertIn(
            ICollectiveCalltoactionLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_CALLTOACTION_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['collective.calltoaction'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if collective.calltoaction is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'collective.calltoaction'))

    def test_browserlayer_removed(self):
        """Test that ICollectiveCalltoactionLayer is removed."""
        from collective.calltoaction.interfaces import \
            ICollectiveCalltoactionLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            ICollectiveCalltoactionLayer,
            utils.registered_layers())
