import unittest2 as unittest


class TestPFGExtendedMailAdapter(unittest.TestCase):
    """Test PFGExtendedMailAdapter content type."""

    def createPFGExtendedMailAdapter(self):
        from Products.Archetypes.Schema.factory import instanceSchemaFactory
        from zope.component import provideAdapter
        provideAdapter(instanceSchemaFactory)
        from Products.PFGExtendedMailAdapter.content.adapter import PFGExtendedMailAdapter
        return PFGExtendedMailAdapter('adapter')

    def test_instance(self):
        from Products.PFGExtendedMailAdapter.content.adapter import PFGExtendedMailAdapter
        item = self.createPFGExtendedMailAdapter()
        isinstance(item, PFGExtendedMailAdapter)

    def test_portal_type(self):
        item = self.createPFGExtendedMailAdapter()
        self.assertEqual(item.portal_type, 'PFGExtendedMailAdapter')

    def test_interface(self):
        from Products.PFGExtendedMailAdapter.interfaces import IPFGExtendedMailAdapterContentType
        item = self.createPFGExtendedMailAdapter()
        self.assertTrue(IPFGExtendedMailAdapterContentType.providedBy(item))

    def test_schema_fields(self):
        item = self.createPFGExtendedMailAdapter()
        names = [
            'id',
            'title',
            'description',
            'constrainTypesMode',
            'locallyAllowedTypes',
            'immediatelyAddableTypes',
            'recipient_name',
            'recipient_email',
        ]
        self.assertEqual(
            [field.getName() for field in item.schema.getSchemataFields('default')],
            names
        )

    def test_field__msg_attachments(self):
        item = self.createPFGExtendedMailAdapter()
        field = item.schema['msg_attachments']
        from Products.PloneFormGen.content.actionAdapter import LinesField
        isinstance(field, LinesField)
        self.assertFalse(field.required)
        self.assertFalse(field.searchable)
        self.assertTrue(field.languageIndependent)
        from Products.Archetypes.public import AnnotationStorage
        isinstance(field.storage, AnnotationStorage)
        widget = field.widget
        from Products.Archetypes.public import SelectionWidget
        isinstance(widget, SelectionWidget)
        self.assertEqual(widget.label, u'E-mail Attachments')
        self.assertEqual(
            widget.description,
            u'Please select the attachments to be sent with email when one has successfully finished inputs of the form.'
        )
        self.assertEqual(field.default, ())
        self.assertEqual(field.vocabulary, 'attachments')
        self.assertTrue(field.enforceVocabulary)

    def test_field__body_pt(self):
        item = self.createPFGExtendedMailAdapter()
        field = item.schema['body_pt']
        from Products.PFGExtendedMailAdapter.content.adapter import ZPTField
        isinstance(field, ZPTField)
        self.assertEqual(field.schemata, 'template')
        self.assertTrue(field.required)
        self.assertFalse(field.searchable)
        self.assertFalse(field.languageIndependent)
        from Products.PloneFormGen.config import EDIT_TALES_PERMISSION
        self.assertEqual(field.write_permission, EDIT_TALES_PERMISSION)
        from Products.CMFCore.permissions import ModifyPortalContent
        self.assertEqual(field.read_permission, ModifyPortalContent)
        self.assertEqual(field.default_method, 'getMailBodyDefault')
        from Products.Archetypes.public import AnnotationStorage
        isinstance(field.storage, AnnotationStorage)
        widget = field.widget
        from Products.Archetypes.public import TextAreaWidget
        isinstance(widget, TextAreaWidget)
        self.assertEqual(widget.label, 'Mail-Body Template')
        self.assertEqual(
            widget.description,
            "This is a Zope Page Template used for rendering of the mail-body. You don't need to modify it, but if you know TAL (Zope's Template Attribute Language) you have the full power to customize your outgoing mails."
        )
        self.assertEqual(widget.rows, 20)
        self.assertEqual(widget.visible, {'edit': 'visible', 'view': 'invisible'})
