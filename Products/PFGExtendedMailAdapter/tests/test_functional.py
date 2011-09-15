# #from Products.PloneFormGen import HAS_PLONE30

# #if HAS_PLONE30:
# import unittest
# import doctest
import StringIO
from zope.component import getSiteManager
# from Acquisition import aq_base
# from Testing import ZopeTestCase as ztc
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.tests.utils import MockMailHost
from Products.MailHost.interfaces import IMailHost

# from Products.PFGExtendedMailAdapter.tests import base

# class TestSetup(base.PFGExtendedMailAdapterFunctionalTestCase):

#     def afterSetUp( self ):
#         """After SetUp"""
#         self.setRoles(('Manager',))
#         ## Set up sessioning objects
#         ztc.utils.setupCoreSessions(self.app)
#         ## Setup MockMailHost
#         portal = self.portal
#         portal._original_MailHost = portal.MailHost
#         portal.MailHost = mailhost = MockMailHost('MailHost')
#         sm = getSiteManager(context=portal)
#         sm.unregisterUtility(provided=IMailHost)
#         sm.registerUtility(mailhost, provided=IMailHost)
#         ## Tools
#         wftool = getToolByName(portal, 'portal_workflow')
#         ## Create Form Folder
#         portal.invokeFactory(
#             'FormFolder',
#             'form',
#             title="Form Folder",
#         )
#         form = portal.form
#         wftool.doActionFor(form, "publish")
#         form.invokeFactory(
#             'PFGExtendedMailAdapter',
#             'adapter',
#             title = 'Verkkomaksut Adapter',
#             recipient_email = 'recipient@abita.fi',
#         )
#         adapter = form.adapter
#         form.setActionAdapter(('adapter',))
#         ## Add Image and File under adapter
#         dummy_image = StringIO.StringIO('Dummy Image')
#         adapter.invokeFactory(
#             'Image',
#             'dummy_image',
#             title = 'dummy.gif',
#             image_file = dummy_image,
#         )
#         dummy_file = StringIO.StringIO('Dummy File')
#         adapter.invokeFactory(
#             'File',
#             'dummy_file',
#             title = 'dummy.pdf',
#             file_file = dummy_file,
#         )

#     def beforeTearDown(self):
#         portal = self.portal
#         portal.MailHost = portal._original_MailHost
#         sm = getSiteManager(context=portal)
#         sm.unregisterUtility(provided=IMailHost)
#         sm.registerUtility(aq_base(portal._original_MailHost), provided=IMailHost)

# def test_suite():
#     return unittest.TestSuite([

#         ztc.FunctionalDocFileSuite(
#             'tests/functional/form_functional.txt',
#             package='Products.PFGExtendedMailAdapter',
#             test_class=TestSetup,
#             optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),

#             ])

# if __name__ == '__main__':
#     unittest.main(defaultTest='test_suite')

from Testing import ZopeTestCase as ztc
from Products.PFGExtendedMailAdapter.tests.base import FUNCTIONAL_TESTING
from leo.testing.browser import Browser
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.testing import layered
from zope.annotation.interfaces import IAnnotations
from zope.interface import alsoProvides
from zope.testing import renormalizing

import doctest
import manuel.codeblock
import manuel.doctest
import manuel.testing
import re
import transaction
import unittest2 as unittest

FLAGS = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS | doctest.REPORT_NDIFF | doctest.REPORT_ONLY_FIRST_FAILURE

CHECKER = renormalizing.RENormalizing([
    # Normalize the generated UUID values to always compare equal.
    (re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'), '<UUID>'),
])


def setUp(self):
    layer = self.globs['layer']
    self.globs.update({
        'portal': layer['portal'],
        'portal_url': layer['portal'].absolute_url(),
        'browser': Browser(layer['app']),
    })
    ztc.utils.setupCoreSessions(layer['app'])
    portal = self.globs['portal']
    browser = self.globs['browser']
    portal_url = self.globs['portal_url']
    browser.setBaseUrl(portal_url)

    browser.handleErrors = True
    portal.error_log._ignored_exceptions = ()

    setRoles(portal, TEST_USER_ID, ['Manager'])

    from plone.app.testing import TEST_USER_NAME, TEST_USER_PASSWORD
    basic = 'Basic {0}:{1}'.format(TEST_USER_NAME, TEST_USER_PASSWORD)
    browser.setHeader('Authorization', basic)

    ## Setup MockMailHost
    portal._original_MailHost = portal.MailHost
    portal.MailHost = mailhost = MockMailHost('MailHost')
    sm = getSiteManager(context=portal)
    sm.unregisterUtility(provided=IMailHost)
    sm.registerUtility(mailhost, provided=IMailHost)

    wftool = getToolByName(portal, 'portal_workflow')

    # Create Form Folder
    # portal.invokeFactory(
    #     'FormFolder',
    #     'form',
    #     title="Form Folder",
    # )
    # form = portal.form
    # wftool.doActionFor(form, "publish")
    # form.invokeFactory(
    #     'PFGExtendedMailAdapter',
    #     'adapter',
    #     title = 'Verkkomaksut Adapter',
    #     recipient_email = 'recipient@abita.fi',
    # )
    # adapter = form.adapter
    # form.setActionAdapter(('adapter',))
    # ## Add Image and File under adapter
    # dummy_image = StringIO.StringIO('Dummy Image')
    # adapter.invokeFactory(
    #     'Image',
    #     'dummy_image',
    #     title = 'dummy.gif',
    #     image_file = dummy_image,
    # )
    # dummy_file = StringIO.StringIO('Dummy File')
    # adapter.invokeFactory(
    #     'File',
    #     'dummy_file',
    #     title = 'dummy.pdf',
    #     file_file = dummy_file,
    # )

    transaction.commit()


def DocFileSuite(testfile, flags=FLAGS, setUp=setUp, layer=FUNCTIONAL_TESTING):
    """Returns a test suite configured with a test layer.

    :param testfile: Path to a doctest file.
    :type testfile: str

    :param flags: Doctest test flags.
    :type flags: int

    :param setUp: Test set up function.
    :type setUp: callable

    :param layer: Test layer
    :type layer: object

    :rtype: `manuel.testing.TestSuite`
    """
    m = manuel.doctest.Manuel(optionflags=flags, checker=CHECKER)
    m += manuel.codeblock.Manuel()

    return layered(
        manuel.testing.TestSuite(m, testfile, setUp=setUp, globs=dict(layer=layer)),
        layer=layer)


def test_suite():
    return unittest.TestSuite([
        # DocFileSuite('functional/content_types_functional.txt'),
        ])
