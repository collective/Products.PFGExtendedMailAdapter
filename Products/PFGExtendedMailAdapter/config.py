from Products.CMFCore.permissions import setDefaultRoles


PROJECTNAME = "PFGExtendedMailAdapter"

setDefaultRoles("Add PFGExtendedMailAdapter", ('Manager', 'Owner',))

ADD_PERMISSIONS = {
    "PFGExtendedMailAdapter": "Add PFGExtendedMailAdapter",
}
