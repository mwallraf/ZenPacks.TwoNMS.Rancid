from zope.component import adapts
from zope.interface import implements

from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.component import ComponentInfo
from Products.Zuul.infos.template import RRDDataSourceInfo

from ZenPacks.TwoNMS.Rancid.RancidRevision import RancidRevision
from ZenPacks.TwoNMS.Rancid.interfaces \
    import IRancidRevisionInfo



class RancidRevisionInfo(ComponentInfo):
    implements(IRancidRevisionInfo)
    adapts(RancidRevision)

    rRevisionId = ProxyProperty("rRevisionId")
    rRevisionDate = ProxyProperty("rRevisionDate")
    rRancidViewerLink = ProxyProperty("rRancidViewerLink")

    monitor = False
    
    @property
    def monitored(self):
        return ""
    
    @property
    def usesMonitorAttribute(self):
        return False
 