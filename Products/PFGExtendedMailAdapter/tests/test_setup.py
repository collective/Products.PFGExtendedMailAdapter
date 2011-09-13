import unittest
from Products.CMFCore.utils import getToolByName
from Products.PFGExtendedMailAdapter.tests.base import PFGExtendedMailAdapterTestCase

class TestSetup(PFGExtendedMailAdapterTestCase):

    def afterSetUp(self):
        self.catalog = getToolByName(self.portal, 'portal_catalog')
        self.types = getToolByName(self.portal, 'portal_types')
        self.wftool = getToolByName(self.portal, 'portal_workflow')
        self.content_types = [
            'PFGExtendedMailAdapter',
        ]
        self.installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.skins      = getToolByName(self.portal, 'portal_skins')
        self.properties = getToolByName(self.portal, 'portal_properties')
        self.site_properties = getattr(self.properties, 'site_properties')
        self.navtree_properties = getattr(self.properties, 'navtree_properties')

    def test_is_pfg_installed(self):
        self.failUnless(self.installer.isProductInstalled('PloneFormGen'))

    def test_is_pfg_extended_mail_adapter_installed(self):
        self.failUnless(self.installer.isProductInstalled('PFGExtendedMailAdapter'))

    ## Content Types
    def test_contents_installed(self):
        for type in self.content_types:
            self.failUnless(type in self.types.objectIds())

    def test_not_searchable(self):
        self.failUnless('PFGExtendedMailAdapter' in list(self.site_properties.getProperty('types_not_searched')))

    def test_use_folder_tabs(self):
        self.failUnless('PFGExtendedMailAdapter' not in self.site_properties.getProperty('use_folder_tabs'))

    def test_typesLinkToFolderContentsInFC(self):
        self.failUnless('PFGExtendedMailAdapter' not in self.site_properties.getProperty('typesLinkToFolderContentsInFC'))

    def test_not_in_navtree(self):
        self.failUnless('PFGExtendedMailAdapter' in list(self.navtree_properties.getProperty('metaTypesNotToList')))

    # Workflow
    def test_workflow(self):
        self.assertEquals((), self.wftool.getChainForPortalType('PFGExtendedMailAdapter'))

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite
