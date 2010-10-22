import unittest
from zope.component import getUtility, getMultiAdapter
from Products.Five import zcml
from Products.Five import fiveconfigure
from OFS.Application import install_package
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

from Products.PluggableAuthService.interfaces.plugins import IExtractionPlugin
from Products.PluggableAuthService.interfaces.plugins import IAuthenticationPlugin

from plone.portlets.interfaces import IPortletManager, IPortletAssignmentMapping

@onsetup
def setup_product():
    fiveconfigure.debug_mode = True
    import collective.suisseid
    zcml.load_config('configure.zcml', collective.suisseid)
    fiveconfigure.debug_mode = False
    
    ztc.installPackage('collective.suisseid')

setup_product()
ptc.setupPloneSite(products=[])

class TestSuisseIdInstallation(ptc.PloneTestCase):
    
    def afterSetUp(self):
        import pas.plugins.suisseid
        # Since Zope 2.10.4 we need to install our package manually
        install_package(self.app, pas.plugins.suisseid, pas.plugins.suisseid.initialize)
    
    def test_pas_plugins(self):
        # Install suisseId
        self.portal.portal_setup.runAllImportStepsFromProfile('profile-collective.suisseid:default')
            
        pas = self.portal.acl_users
        self.assertTrue(u'suisseid' in pas.plugins.keys())
        extractor_names = [ item[0] for item in pas.plugins.listPlugins(IExtractionPlugin) ]
        self.assertTrue(u'suisseid' in extractor_names)
        authenticator_names = [ item[0] for item in pas.plugins.listPlugins(IAuthenticationPlugin) ]
        self.assertTrue(u'suisseid' in authenticator_names)
        
    def test_login_portlet(self):
        # Install suisseId
        self.portal.portal_setup.runAllImportStepsFromProfile('profile-collective.suisseid:default')
        
        manager = getUtility(IPortletManager, name=u"plone.leftcolumn")
        assignment_mapping = getMultiAdapter((self.portal, manager), IPortletAssignmentMapping)
        self.assertTrue(u'suisseid-login' in assignment_mapping.keys())
    
def test_suite():
    suite=unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSuisseIdInstallation))
    return suite