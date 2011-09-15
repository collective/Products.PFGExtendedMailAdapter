from AccessControl import ClassSecurityInfo
from Acquisition import aq_inner
from Acquisition import aq_parent
from Products.ATContentTypes.content.base import registerATCT
from Products.ATContentTypes.content.document import finalizeATCTSchema
from Products.ATContentTypes.content.folder import ATFolderSchema, ATFolder
from Products.Archetypes.public import DisplayList
from Products.Archetypes.public import ObjectField
from Products.Archetypes.public import Schema
from Products.CMFCore.permissions import ModifyPortalContent
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from Products.PFGExtendedMailAdapter import PFGExtendedMailAdapterMessageFactory as _
from Products.PFGExtendedMailAdapter.config import PROJECTNAME
from Products.PFGExtendedMailAdapter.interfaces import IPFGExtendedMailAdapterContentType
from Products.PloneFormGen.config import EDIT_TALES_PERMISSION
from Products.PloneFormGen.content.actionAdapter import AnnotationStorage
from Products.PloneFormGen.content.actionAdapter import LinesField
from Products.PloneFormGen.content.actionAdapter import MultiSelectionWidget
from Products.PloneFormGen.content.actionAdapter import TextAreaWidget
from Products.PloneFormGen.content.fieldsBase import BaseFormField
from Products.PloneFormGen.content.formMailerAdapter import FormMailerAdapter
from Products.PloneFormGen.content.formMailerAdapter import formMailerAdapterSchema
from Products.TemplateFields import ZPTField
from email import Encoders
from email.MIMEAudio import MIMEAudio
from email.MIMEBase import MIMEBase
from email.MIMEImage import MIMEImage
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from zope.interface import implements

_marker = []

def check_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
    except TypeError:
        return False

class ZPTField(ZPTField):

    security  = ClassSecurityInfo()

    security.declarePrivate('getRaw')
    def getRaw(self, instance, **kwargs):
        zpt = ObjectField.get(self, instance, **kwargs)
        if getattr(zpt, 'read', _marker) is not _marker:
            return safe_unicode(zpt.read()).encode('utf8')
        else:
            return zpt

PFGExtendedMailAdapterSchema = ATFolderSchema.copy() + formMailerAdapterSchema.copy() + Schema((

    LinesField(
        name='msg_attachments',
        schemata='message',
        required=False,
        searchable=False,
        languageIndependent=True,
        storage=AnnotationStorage(),
        widget=MultiSelectionWidget(
            label=_(u'E-mail Attachments'),
            description=_(u'Please select the attachments to be sent with email when one has successfully finished inputs of the form.'),
            format='checkbox',
        ),
        vocabulary='attachments',
        enforceVocabulary=True,
    ),

    ZPTField(
        name='body_pt',
        schemata='template',
        write_permission=EDIT_TALES_PERMISSION,
        default_method = 'getMailBodyDefault',
        read_permission=ModifyPortalContent,
        widget=TextAreaWidget(description = 'This is a Zope Page Template '
            'used for rendering of the mail-body. You don\'t need to modify '
            'it, but if you know TAL (Zope\'s Template Attribute Language) '
            'you have the full power to customize your outgoing mails.',
            description_msgid = "help_formmailer_body_pt",
            label = 'Mail-Body Template',
            label_msgid = "label_formmailer_body_pt",
            i18n_domain = "ploneformgen",
            rows = 20,
            visible = {'edit':'visible','view':'invisible'},
            ) ,
        validators=('zptvalidator',),
        ),


    ),)

finalizeATCTSchema(PFGExtendedMailAdapterSchema, folderish=True, moveDiscussion=False)

class PFGExtendedMailAdapter(ATFolder, FormMailerAdapter):
    """Extended Mail Adapter"""

    schema = PFGExtendedMailAdapterSchema
    _at_rename_after_creation = True

#    __implements__ = (ATFolder.__implements__, )
    # implements = IPFGExtendedMailAdapterContentType
    implements(IPFGExtendedMailAdapterContentType)


    def send_form(self, fields, request, **kwargs):
        """Send the form.
        """
        (headerinfo, additional_headers, body) = self.get_header_body_tuple(fields, request, **kwargs)
        if not isinstance(body, unicode):
            body = unicode(body, self._site_encoding())
        portal = getToolByName(self, 'portal_url').getPortalObject()
        email_charset = portal.getProperty('email_charset', 'utf-8')
        mime_text = MIMEText(body.encode(email_charset , 'replace'),
                _subtype=self.body_type or 'html', _charset=email_charset)

        attachments = self.get_attachments(fields, request)
        uids = self.getMsg_attachments()
        if uids:
            reference_catalog = getToolByName(self, 'reference_catalog')
            for uid in uids:
                obj = reference_catalog.lookupObject(uid)
                data = obj.data
                mimetype = obj.content_type
                filename = obj.getRawTitle()
                enc = None
                attachments.append((filename, mimetype, enc, data))

        if attachments:
            outer = MIMEMultipart()
            outer.attach(mime_text)
        else:
            outer = mime_text

        # write header
        for key, value in headerinfo.items():
            outer[key] = value

        # write additional header
        for a in additional_headers:
            key, value = a.split(':', 1)
            outer.add_header(key, value.strip())

        for attachment in attachments:
            filename = attachment[0]
            ctype = attachment[1]
            content = attachment[3]

            if ctype is None:
                ctype = 'application/octet-stream'

            maintype, subtype = ctype.split('/', 1)

            if maintype == 'text':
                msg = MIMEText(content, _subtype=subtype)
            elif maintype == 'image':
                msg = MIMEImage(content, _subtype=subtype)
            elif maintype == 'audio':
                msg = MIMEAudio(content, _subtype=subtype)
            else:
                msg = MIMEBase(maintype, subtype)
                msg.set_payload(content)
                # Encode the payload using Base64
                Encoders.encode_base64(msg)

            # Set the filename parameter
            msg.add_header('Content-Disposition', 'attachment', filename=filename)
            outer.attach(msg)

        mailtext = outer.as_string()

        host = self.MailHost
        host.send(mailtext)


    def attachments(self):
        dl = DisplayList()
        catalog = getToolByName(self, 'portal_catalog')
        path = '/'.join(self.getPhysicalPath())
        brains = catalog(
            portal_type=('File','Image',),
            path=dict(query=path, depth=1),
        )
        for brain in brains:
            dl.add(brain.UID, brain.Title)
        return dl

    def field_ids(self):
        parent = aq_parent(aq_inner(self))
        ids = [obj.id for obj in parent.contentValues() if isinstance(obj, BaseFormField)]
        return ids

registerATCT(PFGExtendedMailAdapter, PROJECTNAME)
