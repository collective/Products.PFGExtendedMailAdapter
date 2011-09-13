## BBB for CMF 1.4
#try:
#    from Products.CMFCore.permissions import setDefaultRoles
#except ImportError:
#    from Products.CMFCore.CMFCorePermissions import setDefaultRoles

#PROJECTNAME = "PFGExtendedMailAdapter"
#DEFAULT_ADD_CONTENT_PERMISSION = "Add PFGExtendedMailAdapter"
#product_globals=globals()

#setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner',))

from Products.CMFCore.permissions import setDefaultRoles
PROJECTNAME = "PFGExtendedMailAdapter"

setDefaultRoles("Add PFGExtendedMailAdapter", ('Manager', 'Owner',))

ADD_PERMISSIONS = {
    "PFGExtendedMailAdapter" : "Add PFGExtendedMailAdapter",
}
