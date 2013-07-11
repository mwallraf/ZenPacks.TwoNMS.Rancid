from Products.ZenReports.Utils import Record
import re


# Revisions count report
class rancid_rvscnt_report_plugin(object):

    # The run method will be executed when your report calls the plugin.
    def run(self, dmd, args):
        report = []
        for dev in dmd.Devices.getSubDevicesGen():
            revcount = dev.os.rancidrevs.countObjects() or 0
            if not dev.getProperty('zRancidIgnore') and revcount > 1:
                lastrevid = dev.os.rancidrevs()[-1].id
                report.append(Record(
                    device=dev.titleOrId(),
                    devicelink=dev.getDeviceUrl(),
                    ip=dev.manageIp,
                    revisions=("%s" % (revcount)),
                    lastrevision=("%s" % (lastrevid)),
                    lastrevisionlink=("%s" % (self.generateLink(dev, lastrevid)))
                    ))
                #report.append(Record(device=dev.titleOrId(), devicelink=dev.getDeviceUrl(), ip=dev.manageIp, lastrevision="test", lastrevisionlink="test"))
        return report

    def generateLink(self, dev, lastrev):
        l = dev.getProperty('zRancidViewerPath')
        g = dev.getProperty('zRancidGroup')
        d = dev.id.lower()
        if not l:
            return lastrev
        if g:
            l = re.sub('\%group\%', g, l)
        l = re.sub('\%device\%', d, l)
        # TODO: this assumes VIEWVC links
        l = re.sub('\?.*', '', l)
        return "%s?view=markup&revision=%s" % (l, lastrev)
        #return "<a href=\"%s?view=markup&revision=%s\" target=\"_blank\">%s</a>" % (l, lastrev, lastrev)
        

