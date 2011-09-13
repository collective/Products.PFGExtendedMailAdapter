#from Products.PloneFormGen import HAS_PLONE30

#if HAS_PLONE30:
import unittest
import doctest
import StringIO
from zope.component import getSiteManager
from Acquisition import aq_base
from Testing import ZopeTestCase as ztc
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.tests.utils import MockMailHost
from Products.MailHost.interfaces import IMailHost

from Products.PFGExtendedMailAdapter.tests import base

class TestSetup(base.PFGExtendedMailAdapterFunctionalTestCase):

    def afterSetUp( self ):
        """After SetUp"""
        self.setRoles(('Manager',))
        ## Set up sessioning objects
        ztc.utils.setupCoreSessions(self.app)
        ## Setup MockMailHost
        portal = self.portal
        portal._original_MailHost = portal.MailHost
        portal.MailHost = mailhost = MockMailHost('MailHost')
        sm = getSiteManager(context=portal)
        sm.unregisterUtility(provided=IMailHost)
        sm.registerUtility(mailhost, provided=IMailHost)
        ## Tools
        wftool = getToolByName(portal, 'portal_workflow')
        ## Create Form Folder
        portal.invokeFactory(
            'FormFolder',
            'form',
            title="Form Folder",
        )
        form = portal.form
        wftool.doActionFor(form, "publish")
        form.invokeFactory(
            'PFGExtendedMailAdapter',
            'adapter',
            title = 'Verkkomaksut Adapter',
            recipient_email = 'recipient@abita.fi',
        )
        adapter = form.adapter
        form.setActionAdapter(('adapter',))
        ## Add Image and File under adapter
        dummy_image = StringIO.StringIO('Dummy Image')
        adapter.invokeFactory(
            'Image',
            'dummy_image',
            title = 'dummy.gif',
            image_file = dummy_image,
        )
        dummy_file = StringIO.StringIO('Dummy File')
        adapter.invokeFactory(
            'File',
            'dummy_file',
            title = 'dummy.pdf',
            file_file = dummy_file,
        )

    def beforeTearDown(self):
        portal = self.portal
        portal.MailHost = portal._original_MailHost
        sm = getSiteManager(context=portal)
        sm.unregisterUtility(provided=IMailHost)
        sm.registerUtility(aq_base(portal._original_MailHost), provided=IMailHost)

def test_suite():
    return unittest.TestSuite([

        ztc.FunctionalDocFileSuite(
            'tests/functional/form_functional.txt',
            package='Products.PFGExtendedMailAdapter',
            test_class=TestSetup,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),

            ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
