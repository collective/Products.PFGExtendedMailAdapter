import mock
import unittest


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
            'recipient_email']
        self.assertEqual(
            [field.getName() for field in item.schema.getSchemataFields('default')],
            names)

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
            u'Please select the attachments to be sent with email.')
        self.assertEqual(field.default, ())
        self.assertEqual(field.vocabulary, 'attachments')
        self.assertTrue(field.enforceVocabulary)

    @mock.patch('Products.PFGExtendedMailAdapter.content.adapter.getToolByName')
    def test_get_mail_text(self, getToolByName):
        ## Test need to be done.
        item = self.createPFGExtendedMailAdapter()
        item.get_header_body_tuple = mock.Mock()
        headerinfo = {
            'From': '',
            u'X-HTTP_X_FORWARDED_FOR': '',
            u'X-REMOTE_ADDR': '',
            'To': ' <recipient@abita.fi>',
            'Subject': '=?utf-8?q?Form_Submission?=',
            u'X-PATH_INFO': '/plone/form',
            'MIME-Version': '1.0'
        }
        body = '<html><head><title></title></head><body>Message</body></html>'
        item.get_header_body_tuple.return_value = (headerinfo, (), body)
        item._site_encoding = mock.Mock()
        item._site_encoding.return_value = 'utf-8'
        portal = mock.Mock()
        getToolByName().getPortalObject.return_value = portal
        portal.getProperty.return_value = 'utf-8'
        item.body_type = None
        item.get_attachments = mock.Mock()
        item.get_attachments.return_value = []
        fields = mock.Mock()
        request = mock.Mock()
        text = 'Content-Type: text/html; charset="utf-8"\nMIME-Version: 1.0\nContent-Transfer-Encoding: quoted-printable\nFrom: \nX-HTTP_X_FORWARDED_FOR: \nX-REMOTE_ADDR: \nTo: <recipient@abita.fi>\nMIME-Version: 1.0\nX-PATH_INFO: /plone/form\nSubject: =?utf-8?q?Form_Submission?=\n\n<html><head><title></title></head><body>Message</body></html>'
        self.assertEqual(item.get_mail_text(fields, request), text)

    @mock.patch('Products.PFGExtendedMailAdapter.content.adapter.getToolByName')
    @mock.patch('Products.PFGExtendedMailAdapter.content.adapter.DisplayList')
    def test_attachements(self, DisplayList, getToolByName):
        item = self.createPFGExtendedMailAdapter()
        catalog = mock.Mock()
        getToolByName.return_value = catalog
        catalog.return_value = [mock.Mock(), mock.Mock()]
        dl = mock.Mock()
        DisplayList.return_value = dl
        item.attachments()
        self.assertTrue(DisplayList.called)
        self.assertTrue(dl.add.called)

    @mock.patch('Products.PFGExtendedMailAdapter.content.adapter.aq_parent')
    def test_field_ids(self, aq_parent):
        item = self.createPFGExtendedMailAdapter()
        parent = mock.Mock()
        parent.contentValues.return_value = []
        aq_parent.return_value = parent
        self.assertEqual(item.field_ids(), [])
        parent.contentValues.return_value = [mock.Mock(), mock.Mock()]
        aq_parent.return_value = parent
        self.assertEqual(item.field_ids(), [])
        from Products.PloneFormGen.content.fieldsBase import BaseFormField
        parent.contentValues.return_value = [BaseFormField('field01'), BaseFormField('field02')]
        aq_parent.return_value = parent
        self.assertEqual(item.field_ids(), ['field01', 'field02'])
