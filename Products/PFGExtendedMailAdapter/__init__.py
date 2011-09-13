#from Products.CMFCore import utils#, DirectoryView
#from Products.Archetypes.public import (
#    process_types,
#)
#from Products.Archetypes import listTypes
#from Products.PFGExtendedMailAdapter.config import (
#    DEFAULT_ADD_CONTENT_PERMISSION,
#    PROJECTNAME,
#)

#from zope.i18nmessageid import MessageFactory
#PFGExtendedMailAdapterMessageFactory = MessageFactory(PROJECTNAME)

#def initialize(context):

#    # Import the type, which results in registerType() being called
#    from content import PFGExtendedMailAdapter

#    # initialize the content, including types and add permissions
#    content_types, constructors, ftis = process_types(
#        listTypes(PROJECTNAME),
#        PROJECTNAME)

#    utils.ContentInit(
#        PROJECTNAME + ' Content',
#        content_types      = content_types,
#        permission         = DEFAULT_ADD_CONTENT_PERMISSION,
#        extra_constructors = constructors,
#        fti                = ftis,
#        ).initialize(context)

from zope.i18nmessageid import MessageFactory
from Products.Archetypes import atapi
from Products.CMFCore import utils
from Products.PFGExtendedMailAdapter.config import ADD_PERMISSIONS, PROJECTNAME

PFGExtendedMailAdapterMessageFactory = MessageFactory(PROJECTNAME)

def initialize(context):
    """Initializer called when used as a Zope 2 product."""

    content_types, constructors, ftis = atapi.process_types(
        atapi.listTypes(PROJECTNAME),
        PROJECTNAME)

    for atype, constructor in zip(content_types, constructors):
        utils.ContentInit("%s: %s" % (PROJECTNAME, atype.portal_type),
            content_types      = (atype,),
            permission         = ADD_PERMISSIONS[atype.portal_type],
            extra_constructors = (constructor,),
            ).initialize(context)
