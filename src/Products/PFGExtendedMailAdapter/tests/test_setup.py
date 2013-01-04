from Products.CMFCore.utils import getToolByName
from Products.PFGExtendedMailAdapter.tests.base import IntegrationTestCase


class TestSetup(IntegrationTestCase):

    def setUp(self):
        self.portal = self.layer['portal']

    def test_package_installed(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.assertTrue(installer.isProductInstalled('PFGExtendedMailAdapter'))

    def test_pfg_installed(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.assertTrue(installer.isProductInstalled('PloneFormGen'))

    def test_factorytool__PFGExtendedMailAdapter(self):
        factory = getToolByName(self.portal, 'portal_factory')
        self.assertTrue(factory.getFactoryTypes()['PFGExtendedMailAdapter'])

    def test_metadata__version(self):
        setup = getToolByName(self.portal, 'portal_setup')
        self.assertEqual(
            setup.getVersionForProfile('profile-Products.PFGExtendedMailAdapter:default'), u'1')

    def test_propertiestool__not_searchable(self):
        properties = getToolByName(self.portal, 'portal_properties')
        site_properties = getattr(properties, 'site_properties')
        self.assertIn('PFGExtendedMailAdapter', list(site_properties.getProperty('types_not_searched')))

    def test_propertiestool__use_folder_tabs(self):
        properties = getToolByName(self.portal, 'portal_properties')
        site_properties = getattr(properties, 'site_properties')
        self.assertNotIn('PFGExtendedMailAdapter', site_properties.getProperty('use_folder_tabs'))

    def test_proepertiestool__typesLinkToFolderContentsInFC(self):
        properties = getToolByName(self.portal, 'portal_properties')
        site_properties = getattr(properties, 'site_properties')
        self.assertNotIn('PFGExtendedMailAdapter', site_properties.getProperty('typesLinkToFolderContentsInFC'))

    def test_propertiestool__not_in_navtree(self):
        properties = getToolByName(self.portal, 'portal_properties')
        navtree_properties = getattr(properties, 'navtree_properties')
        self.assertIn('PFGExtendedMailAdapter', list(navtree_properties.getProperty('metaTypesNotToList')))

    def test_rolemap__Add_PFGExtendedMailAdapter__rolesOfPermission(self):
        permission = "Add PFGExtendedMailAdapter"
        roles = [
            item['name'] for item in self.portal.rolesOfPermission(
                permission) if item['selected'] == 'SELECTED']
        roles.sort()
        self.assertEqual(
            roles, ['Editor', 'Manager', 'Site Administrator'])

    def test_rolemap__Add_PFGExtendedMailAdapter__acquiredRolesAreUsedBy(self):
        permission = "Add PFGExtendedMailAdapter"
        self.assertEqual(
            self.portal.acquiredRolesAreUsedBy(permission), '')

    def test_types__PFGExtendedMailAdapter__metatype(self):
        types = getToolByName(self.portal, 'portal_types')
        ctype = types.getTypeInfo('PFGExtendedMailAdapter')
        self.assertEqual(ctype.meta_type, 'Factory-based Type Information with dynamic views')

    def test_types__PFGExtendedMailAdapter__title(self):
        types = getToolByName(self.portal, 'portal_types')
        ctype = types.getTypeInfo('PFGExtendedMailAdapter')
        self.assertEquals(ctype.title, 'Extended Mail Adapter')

    def test_types__PFGExtendedMailAdapter__description(self):
        types = getToolByName(self.portal, 'portal_types')
        ctype = types.getTypeInfo('PFGExtendedMailAdapter')
        self.assertEquals(ctype.description, '')

    def test_types__PFGExtendedMailAdapter__content_meta_type(self):
        types = getToolByName(self.portal, 'portal_types')
        ctype = types.getTypeInfo('PFGExtendedMailAdapter')
        self.assertEquals(ctype.content_meta_type, 'PFGExtendedMailAdapter')

    def test_types__PFGExtendedMailAdapter__factory(self):
        types = getToolByName(self.portal, 'portal_types')
        ctype = types.getTypeInfo('PFGExtendedMailAdapter')
        self.assertEquals(ctype.factory, 'addPFGExtendedMailAdapter')

    def test_types__PFGExtendedMailAdapter__immediate_view(self):
        types = getToolByName(self.portal, 'portal_types')
        ctype = types.getTypeInfo('PFGExtendedMailAdapter')
        self.assertEquals(ctype.immediate_view, 'base_view')

    def test_types__PFGExtendedMailAdapter__global_allow(self):
        types = getToolByName(self.portal, 'portal_types')
        ctype = types.getTypeInfo('PFGExtendedMailAdapter')
        self.assertFalse(ctype.global_allow)

    def test_types__PFGExtendedMailAdapter__filter_content_types(self):
        types = getToolByName(self.portal, 'portal_types')
        ctype = types.getTypeInfo('PFGExtendedMailAdapter')
        self.assertFalse(ctype.filter_content_types)

    def test_types__PFGExtendedMailAdapter__allowed_content_types(self):
        types = getToolByName(self.portal, 'portal_types')
        ctype = types.getTypeInfo('PFGExtendedMailAdapter')
        self.assertEqual(ctype.allowed_content_types, ())

    def test_types__PFGExtendedMailAdapter__default_view(self):
        types = getToolByName(self.portal, 'portal_types')
        ctype = types.getTypeInfo('PFGExtendedMailAdapter')
        self.assertEqual(ctype.default_view, 'base_view')

    def test_types__PFGExtendedMailAdapter__view_methods(self):
        types = getToolByName(self.portal, 'portal_types')
        ctype = types.getTypeInfo('PFGExtendedMailAdapter')
        self.assertEqual(ctype.view_methods, ('base_view',))

    def test_types__PFGExtendedMailAdapter__aliases(self):
        types = getToolByName(self.portal, 'portal_types')
        ctype = types.getTypeInfo('PFGExtendedMailAdapter')
        self.assertEqual(ctype.getMethodAliases(), {
            '(Default)': '(dynamic view)',
            'edit': 'atct_edit',
            'sharing': '@@sharing',
            'view': '(selected layout)'
        })

    def test_types__FormFolder__allowed_content_types(self):
        types = getToolByName(self.portal, 'portal_types')
        ctype = types.getTypeInfo('FormFolder')
        self.assertIn('PFGExtendedMailAdapter', ctype.allowed_content_types)

    def test_workflow(self):
        workflow = getToolByName(self.portal, 'portal_workflow')
        self.assertEquals((), workflow.getChainForPortalType('PFGExtendedMailAdapter'))

    def test_uninstall__package(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        installer.uninstallProducts(['PFGExtendedMailAdapter'])
        self.assertFalse(installer.isProductInstalled('PFGExtendedMailAdapter'))

    def test_uninstall__types__PFGExtendedMailAdapter(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        installer.uninstallProducts(['PFGExtendedMailAdapter'])
        types = getToolByName(self.portal, 'portal_types')
        self.assertIsNone(types.getTypeInfo('PFGExtendedMailAdapter'))
