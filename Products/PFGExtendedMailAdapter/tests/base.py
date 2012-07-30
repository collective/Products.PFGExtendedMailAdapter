from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import unittest


class PFGExtendedMailAdapterLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""
        # Load ZCML
        import Products.PloneFormGen
        self.loadZCML(package=Products.PloneFormGen)
        z2.installProduct(app, 'Products.PloneFormGen')
        import Products.PFGExtendedMailAdapter
        self.loadZCML(package=Products.PFGExtendedMailAdapter)
        z2.installProduct(app, 'Products.PFGExtendedMailAdapter')

    def setUpPloneSite(self, portal):
        """Set up Plone."""
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'Products.PloneFormGen:default')
        self.applyProfile(portal, 'Products.PFGExtendedMailAdapter:default')

    def tearDownZope(self, app):
        """Tear down Zope."""
        z2.uninstallProduct(app, 'Products.PloneFormGen')
        z2.uninstallProduct(app, 'Products.PFGExtendedMailAdapter')


FIXTURE = PFGExtendedMailAdapterLayer()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name="PFGExtendedMailAdapterLayer:Integration")
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name="PFGExtendedMailAdapterLayer:Functional")


class IntegrationTestCase(unittest.TestCase):
    """Base class for integration tests."""

    layer = INTEGRATION_TESTING


class FunctionalTestCase(unittest.TestCase):
    """Base class for functional tests."""

    layer = FUNCTIONAL_TESTING
