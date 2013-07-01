######################################################################
#
# ZenPacks.TwoNMS.PrinterMIB.Printer object class
#
######################################################################

__doc__=""" 

Main class to describe a single SVN/CVS revision

$Id: $"""

__version__ = "$Revision: $"[11:-2]


from Globals import InitializeClass
from Products.ZenModel.OSComponent import OSComponent
from Products.ZenRelations.RelSchema import ToManyCont, ToOne
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenModel.ZenossSecurity import ZEN_CHANGE_DEVICE, ZEN_VIEW
from Products.ZenUtils.Utils import zenPath
import commands


import logging
log = logging.getLogger('zen.Revision')

class RancidRevision(OSComponent):
    """A Printer Device"""

    command = zenPath('libexec', 'zenrancid-cvs.sh')

    portal_type = meta_type = 'RancidRevision'
    rRevisionId = "" 		 # unsupported if -1
    rRevisionDate = ""
    rRevisionFilePath = ""
    rRevisionCatPath = ""
    rRancidViewerLink = ""  # link to external viewer

    #*************  Those should match this list below *******************
    _properties = OSComponent._properties + (
            {'id':'rRevisionId', 'type':'string', 'mode':''},
            {'id':'rRevisionDate', 'type':'string', 'mode':''},
            {'id':'rRevisionFilePath', 'type':'string', 'mode':''},
            {'id':'rRevisionCatPath', 'type':'string', 'mode':''},
            {'id':'rRancidViewerLink', 'type':'string', 'mode':''},            
        )
    #****************

    _relations = OSComponent._relations + (
        ('os', ToOne(ToManyCont, 'Products.ZenModel.OperatingSystem', 'rancidrevs')),
    )

    
    def rancidShowConfig(self):
        # TODO: check if file exists
        self.rRevisionCatPath = "unknown"
        if self.rRevisionCatPath:
            device = self.device()
            cmd = "%s cat %s %s %s" % (self.command, self.rRevisionId, device.zRancidGroup, device.id.lower())
            return commands.getoutput(cmd)
        else:
            return "No config found"

    def monitored(self):
        return False

    #titleOrId = name = viewName

    # this allows editable fields in the Details pane
    isUserCreatedFlag = True
    def isUserCreated(self):
        return self.isUserCreatedFlag

InitializeClass(RancidRevision)

