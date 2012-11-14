from Products.Archetypes import atapi
from Products.CMFCore import utils
from zope.i18nmessageid import MessageFactory


PROJECTNAME = "PFGExtendedMailAdapter"


ADD_PERMISSIONS = {
    PROJECTNAME: "Add PFGExtendedMailAdapter",
}

_ = MessageFactory('Products.PFGExtendedMailAdapter')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""

    content_types, constructors, ftis = atapi.process_types(
        atapi.listTypes(PROJECTNAME),
        PROJECTNAME
    )

    for atype, constructor in zip(content_types, constructors):
        utils.ContentInit(
            '{}: {}'.format(PROJECTNAME, atype.portal_type),
            content_types=(atype,),
            permission=ADD_PERMISSIONS[atype.portal_type],
            extra_constructors=(constructor,),
        ).initialize(context)
