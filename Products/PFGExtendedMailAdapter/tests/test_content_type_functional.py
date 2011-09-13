import unittest
import doctest
from Testing import ZopeTestCase as ztc
from Products.PFGExtendedMailAdapter.tests import base

class TestSetup(base.PFGExtendedMailAdapterFunctionalTestCase):

    def afterSetUp( self ):
        """After SetUp"""
        self.setRoles(('Manager',))
        ## Set up sessioning objects
        ztc.utils.setupCoreSessions(self.app)

def test_suite():
    return unittest.TestSuite([

        ztc.FunctionalDocFileSuite(
            'tests/functional/content_types_functional.txt',
            package='Products.PFGExtendedMailAdapter',
            test_class=TestSetup,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),

            ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
