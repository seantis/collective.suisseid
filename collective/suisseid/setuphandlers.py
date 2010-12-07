from zope.component import queryUtility
from zope.component import getMultiAdapter
from StringIO import StringIO
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager
from Products.CMFCore.utils import getToolByName
from collective.suisseid.portlets.login import Assignment as LoginAssignment

def hasSuisseIDPlugin(portal):
    acl = getToolByName(portal, "acl_users")
    return 'suisseid' in acl.plugins.keys()


def createSuisseIDPlugin(portal, out):
    print >> out, "Adding suisseID plugin"
    acl = getToolByName(portal, "acl_users")
    acl.manage_addProduct["pas.plugins.suisseid"].addSuisseIDPlugin(
            id="suisseid", title="suisseID authentication plugin")
            
            
def configureSuisseIDPlugin(portal, out):
    print >> out, "Configuring suisseID plugin"
    acl = getToolByName(portal, "acl_users")
    plugin = getattr(acl, 'suisseid')
    plugin.changeConfiguration(portal.Title(), 
                               portal.absolute_url(), 
                               '', 
                               'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname\r\nhttp://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname',
                               '',
                               '', 
                               '', 
                               '/usr/bin/xmlsec1',
                               '')


def activatePlugin(portal, out, plugin):
    print >> out, "Activating %s plugin" % plugin
    acl = getToolByName(portal, "acl_users")
    plugin = getattr(acl, plugin)

    activate=[]

    for info in acl.plugins.listPluginTypeInfo():
        interface=info["interface"]
        interface_name=info["id"]
        if plugin.testImplements(interface):
            activate.append(interface_name)
            print >>out, "Activating interface %s for plugin %s" % \
                    (interface_name, info["title"])

    plugin.manage_activateInterfaces(activate)


def addLoginPortlet(portal, out):
    leftColumn = queryUtility(IPortletManager, name=u'plone.leftcolumn', context=portal)
    if leftColumn is not None:
        left = getMultiAdapter((portal, leftColumn,), IPortletAssignmentMapping, context=portal)
        if u'suisseid-login' not in left:
            print >>out, "Adding suisseID login portlet to the left column"
            left[u'suisseid-login'] = LoginAssignment()


def importVarious(context):
    # Only run step if a flag file is present (e.g. not an extension profile)
    if context.readDataFile('suisseid-pas.txt') is None:
        return

    site = context.getSite()
    out = StringIO()
    if not hasSuisseIDPlugin(site):
        createSuisseIDPlugin(site, out)
        configureSuisseIDPlugin(site, out)
        activatePlugin(site, out, "suisseid")

    addLoginPortlet(site, out)

