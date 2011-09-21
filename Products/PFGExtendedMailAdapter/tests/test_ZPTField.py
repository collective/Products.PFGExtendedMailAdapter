import mock
import unittest2 as unittest


class TestZPTField(unittest.TestCase):
    """Test ZPTField."""

    def createZPTField(self):
        from Products.PFGExtendedMailAdapter.content.adapter import ZPTField
        return ZPTField('field')

    def test_instance(self):
        from Products.PFGExtendedMailAdapter.content.adapter import ZPTField
        field = self.createZPTField()
        isinstance(field, ZPTField)
        from Products.TemplateFields import ZPTField
        issubclass(ZPTField, ZPTField)

    @mock.patch('Products.PFGExtendedMailAdapter.content.adapter.safe_unicode')
    def test_getRaw(self, safe_unicode):
        field = self.createZPTField()
        instance = mock.Mock()
        field.getRaw(instance)
        self.assertTrue(safe_unicode.called)
