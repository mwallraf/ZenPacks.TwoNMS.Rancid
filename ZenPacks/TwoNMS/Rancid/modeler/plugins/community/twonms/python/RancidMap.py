###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2009, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################

__doc__ = """
Show each revision of the Rancid file
"""

import re
from Products.DataCollector.plugins.CollectorPlugin import PythonPlugin
from twisted.internet.utils import getProcessOutput
from Products.ZenUtils.ZenTales import talesCompile, getEngine
from Products.ZenUtils.Utils import zenPath
from Products.DataCollector.plugins.DataMaps import ObjectMap, RelationshipMap
from xml.dom.minidom import parseString
from datetime import datetime

class RancidMap(PythonPlugin):
    """
    Show each revision of the Rancid file
    """
    command = zenPath('libexec', 'zenrancid-cvs.sh')
    
    compname = "os"
    relname = "rancidrevs"
    modname = "ZenPacks.TwoNMS.Rancid.RancidRevision"
    deviceProperties = PythonPlugin.deviceProperties + (
        'zRancidIgnore', 'zRancidGroup', 'zRancidViewerPath', 'zRancidDeviceType')


    def condition(self, device, log):
        if (not device.zRancidIgnore) and device.zRancidGroup:
            return True
        log.debug("Skip device %s because zRancidIgnore or zRancidGroup are not set", device)


    def collect(self, device, log):
        log.debug("Collect (self, device) = %s, %s", self, device)
        return getProcessOutput(self.command, args=("log", device.zRancidGroup, device.id.lower()))


    # example output of "svnlook history"
    # REVISION   PATH <ID>
    # --------   ---------
    # 5   /Printers/configs/hp2600n <2-5.0.r5/0>
    def process(self, device, results, log):
        log.debug('Process (self, device, results) %s, %s, %s', self, device, results)

        rm = self.relMap()

        svnLog = []
        try:
            dom = parseString(results)
            logEntries = dom.getElementsByTagName('logentry')
            for entry in logEntries:
                om = self.objectMap()
                logId = entry.attributes['revision'].value
                logDate = entry.getElementsByTagName('date')[0].childNodes[0].data
                logDate = datetime.strptime(logDate, '%Y-%m-%dT%H:%M:%S.%fZ')
                log.debug("New SVN log: %s, %s", logId, logDate)
                
                om.id = self.prepId(logId)
                om.rRevisionId = om.id
                om.rRevisionDate = str(logDate)
                om.rRancidViewerLink = ""
                ## substitute %id% %group% %device% %type%
                if device.zRancidViewerPath:
                    om.rRancidViewerLink = device.zRancidViewerPath
                    if device.id: om.rRancidViewerLink = re.sub('\%device\%', device.id.lower(), om.rRancidViewerLink)
                    om.rRancidViewerLink = re.sub('\%id\%', om.id, om.rRancidViewerLink)
                    if device.zRancidGroup: om.rRancidViewerLink = re.sub('\%group\%', device.zRancidGroup, om.rRancidViewerLink)
                    if device.zRancidDeviceType: om.rRancidViewerLink = re.sub('\%type\%', device.zRancidDeviceType, om.rRancidViewerLink)
                    #om.rRancidViewerLink = "%s%s/%s" % (device.zRancidViewerPath, device.zRancidGroup, device.id.lower())
                rm.append(om)
        except:
            pass
        log.debug("RelationMap = %s", rm)
        return rm
