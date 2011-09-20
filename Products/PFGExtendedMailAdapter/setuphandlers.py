from Products.CMFCore.utils import getToolByName

def setupExtendedMailAdapterProperties(portal):
    name = 'PFGExtendedMailAdapter'
    properties = getToolByName(portal, 'portal_properties')

    ## Site Properties
    site_properties = getattr(properties, 'site_properties')

    types_not_searched = list(site_properties.getProperty('types_not_searched'))
    if name not in types_not_searched:
        types_not_searched.append(name)
    site_properties.manage_changeProperties(types_not_searched = types_not_searched)

    ## Navtree Properties
    navtree_properties = getattr(properties, 'navtree_properties')
    types_not_listed = list(navtree_properties.getProperty('metaTypesNotToList'))
    if name not in types_not_listed:
        types_not_listed.append(name)
    navtree_properties.manage_changeProperties(metaTypesNotToList = types_not_listed)

    ## Allowed types
    types = getToolByName(portal, 'portal_types')
    allowed_content_types = list(types['FormFolder'].allowed_content_types)
    if name not in allowed_content_types:
        allowed_content_types.append(name)
    types.getTypeInfo('FormFolder').manage_changeProperties(allowed_content_types = allowed_content_types)

def setupVarious(context):

    if context.readDataFile('Products.PFGExtendedMailAdapter_various.txt') is None:
        return

    portal = context.getSite()
    setupExtendedMailAdapterProperties(portal)
