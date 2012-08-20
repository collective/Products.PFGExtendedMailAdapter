from Products.PFGExtendedMailAdapter.tests.base import FUNCTIONAL_TESTING
from Testing import ZopeTestCase as ztc
from hexagonit.testing.browser import Browser
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.testing import setRoles
from plone.testing import layered
from zope.testing import renormalizing

import StringIO
import doctest
import manuel.codeblock
import manuel.doctest
import manuel.testing
import re
import transaction
import unittest


FLAGS = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS | doctest.REPORT_NDIFF | doctest.REPORT_ONLY_FIRST_FAILURE

CHECKER = renormalizing.RENormalizing([
    # Normalize the generated UUID values to always compare equal.
    (re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'), '<UUID>'),
])


def prink(e):
    print eval('"""{0}"""'.format(str(e)))


def setUp(self):
    layer = self.globs['layer']
    portal = layer['portal']
    browser = Browser(layer['app'])
    self.globs.update({
        'portal': portal,
        'browser': browser,
        'prink': prink,
        'TEST_USER_NAME': TEST_USER_NAME,
        'TEST_USER_PASSWORD': TEST_USER_PASSWORD,
    })
    ztc.utils.setupCoreSessions(layer['app'])
    browser.setBaseUrl(portal.absolute_url())

    browser.handleErrors = True
    portal.error_log._ignored_exceptions = ()

    setRoles(portal, TEST_USER_ID, ['Manager'])

    basic = 'Basic {}:{}'.format(TEST_USER_NAME, TEST_USER_PASSWORD)
    browser.setHeader('Authorization', basic)

    # ## Setup MockMailHost
    from Products.CMFPlone.tests.utils import MockMailHost
    from Products.MailHost.interfaces import IMailHost
    from zope.component import getSiteManager
    portal._original_MailHost = portal.MailHost
    portal.MailHost = mailhost = MockMailHost('MailHost')
    sm = getSiteManager(context=portal)
    sm.unregisterUtility(provided=IMailHost)
    sm.registerUtility(mailhost, provided=IMailHost)
    self.globs.update({
        'mailhost': portal.MailHost,
    })

    # Create Form Folder
    portal.invokeFactory(
        'FormFolder',
        'form',
        title="Form Folder")
    form = portal.form
    form_url = form.absolute_url()
    self.globs.update({
        'form': form,
        'form_url': form_url,
    })
    form.invokeFactory(
        'PFGExtendedMailAdapter',
        'adapter',
        title='Verkkomaksut Adapter',
        recipient_email='recipient@abita.fi')
    adapter = form.adapter
    adapter_url = adapter.absolute_url()
    self.globs.update({
        'adapter': adapter,
        'adapter_url': adapter_url,
    })
    form.setActionAdapter(('adapter',))
    ## Add Image and File under adapter
    dummy_image = StringIO.StringIO('Dummy Image')
    adapter.invokeFactory(
        'Image',
        'dummy_image',
        title='dummy.gif',
        image_file=dummy_image)
    dummy_image = adapter['dummy_image']
    dimage_uid = dummy_image.UID()
    dummy_file = StringIO.StringIO('Dummy File')
    adapter.invokeFactory(
        'File',
        'dummy_file',
        title='dummy.pdf',
        file_file=dummy_file)
    dummy_file = adapter['dummy_file']
    dfile_uid = dummy_file.UID()
    self.globs.update({
        'dummy_image': dummy_image,
        'dimage_uid': dimage_uid,
        'dummy_file': dummy_file,
        'dfile_uid': dfile_uid,
    })

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
        DocFileSuite('functional/content_types_functional.txt'),
        DocFileSuite('functional/form_functional.txt')])
