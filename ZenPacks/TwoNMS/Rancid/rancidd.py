from Globals import *
from Products.ZenUtils.CyclingDaemon import CyclingDaemon

import logging
log = logging.getLogger('zen.zenrancid')
from twisted.internet import reactor
from Products.ZenUtils.Utils import zenPath
import shutil
import os
from stat import S_IREAD, S_IWRITE, S_IEXEC, S_IRGRP, S_IXGRP
import re


from datetime import datetime
from time import localtime, strftime


# TODO: add daemon statistics
#       clean up code + optimize
class rancidd(CyclingDaemon):
    
    # RANCID VERSION (as downloaded from shrubbery.net)
    RANCID_VERSION = "2.3.8"
    
    startDelay = 0 # in seconds
    standalone = True

    base_path = zenPath()
    rancid_path = zenPath('rancid')
    homedir_path = os.path.expanduser('~zenoss')

    cloginFile = ".cloginrc"
    cCustomLoginFile = "etc/cloginrc-custom"
    configFile = "rancid.conf"
    customConfigFile = "rancid-custom.conf"
    cronFile = "zenoss-rancid.cron"

    _list_of_groups = []  # list of rancid groups
    _rancid = []          # list of all rancid-enabled devices

    def __init__(self, standalone=True):
        if standalone:
            self.initStandalone()
        else:
            self.standalone = False


    def initStandalone(self):
        CyclingDaemon.__init__(self)
        log.info("call init")
        self.name = "zenrancidtest"
        # in daemon mode we only want to run the process once a day by default
        if self.options.daemon:
            self._calcStartDelay()
        log.debug("options: %s", self.options)            
        

    def getRancidVersion(self):
        return self.RANCID_VERSION


    ## override run() to introduce the delay timer
    def run(self):
        reactor.callLater(self.startDelay, self.runCycle)
        reactor.run()


    def main_loop(self):
        #print "MAIN LOOP STARTED"
        log.info("main_loop started in rancidd")
                
        # find out which devices to use
        self.getRancidDevices()

        # always re-create the rancid config file
        self.generate_conf()

        # always re-recreate the default .cloginrc file
        self.generate_cloginrc()

        # always run rancid-cvs to update CVS dirs before running rancid-run
        # needed in case new groups have been added to the rancid config file
        self.run_rancid_cvs()
        
        # generate the router.db file
        self.generate_router_db()
        
        # rancid-run to get all configs
        self.run_rancid()



    def setup(self):
        # find out which devices to use
        #_devices, _groups = self.getRancidDevices()
        #self.generate_crontab()
        self.generate_cloginrc()
        self.generate_conf()
        self.generateCustomDbPath()
        #self.generate_rancid_svn_binary()
        self.generate_rancid_logrotate_file()


        
        
    def buildOptions(self):
        CyclingDaemon.buildOptions(self)
        self.parser.add_option( '--device', dest='rDevice', type='string', default='', help='Run Rancid for a single device')
        self.parser.add_option( '--rcssys', dest='rancid_rcssys', type='string', default="svn", help='Rancid repository, use either SVN or CVS - default SVN (not yet supported)')
        self.parser.add_option( '--starttime', dest='starttime', type='string', default="02:00", help='Rancid start time. Format = HH:MM (default 02:00)')
        self.parser.add_option( '--repeat', dest='repeat', type='int', default=86400, help='Rancid cycle time in seconds, run only once a day by default. (default 86400)')


    # by default we want to run Rancid only once a day at 02:00
    # cycle and starttime can be configured in the daemon conf file or set using commandline parameters
    def _calcStartDelay(self):
        currTime = strftime("%H:%M", localtime())
        #startTime = '23:58'
        startTime = self.options.starttime or '02:00'
        self.options.cycletime = self.options.repeat or 60*60*4
        FMT = '%H:%M'
        delta = datetime.strptime(startTime, FMT) - datetime.strptime(currTime, FMT)
        self.startDelay = delta.seconds
        log.info("Rancid will start at %s (%s seconds to go). Cycle time = %s", startTime, self.startDelay, self.options.cycletime)


    def getRancidDevices(self):
        # initialize variables
        self._list_of_groups = []
        self._rancid = []
        
        devs = self.dmd.Devices
        devlist = devs.getSubDevices()
        for dev in devlist:
            log.debug("Found device: %s", dev)
            ## only use monitored devices
            if not dev.monitorDevice(): continue
            ## only continue if Rancid is configured and enabled
            if dev.getProperty("zRancidIgnore", False): continue
            d = { 'id': dev.id, 
                  'user': dev.getProperty("zRancidUser"), 
                  'password': self.generate_password(dev.getProperty("zRancidPassword")), 
                  'enablePassword': self.generate_password(dev.getProperty("zRancidEnablePassword")), 
                  'group': dev.getProperty("zRancidGroup"), 
                  'deviceType': dev.getProperty("zRancidDeviceType"),
                  'useSSH': dev.getProperty("zRancidSSH")
                  }
            self._rancid.append(d)
            if dev.getProperty("zRancidGroup") is not None:
                self._list_of_groups.append(dev.getProperty("zRancidGroup"))
        # make list unique
        self._list_of_groups = list(set(self._list_of_groups))
        log.debug("_rancid list = %s", self._rancid)
        log.debug("_list_of_groups list = %s", self._list_of_groups)



    def generate_password(self, password):
        pwd = re.sub('\$', '\\$', password)
        return pwd



    def generate_cloginrc(self):
        clogin = os.path.join(self.homedir_path, self.cloginFile)
        out = open(clogin, "w")

        ## generate device specific info
        for dev in self._rancid:
            if not dev['id']: continue
            dev_lc = dev['id'].lower()
            out.write("## " + dev_lc + " ##\n")
            if dev['user']:
                out.write("add user " + dev_lc + " " + dev['user'] + "\n")
            if dev['password']:
                out.write("add password " + dev_lc + " " + dev['password'])
                if dev['enablePassword']:
                    out.write(" " + dev['enablePassword'])
                out.write("\n")
            if dev['useSSH']:
                out.write("add method %s ssh telnet\n" % (dev_lc))
            out.write("\n")
          
        ## generate global defaults
        out.write("include " + os.path.join(self.rancid_path, self.cCustomLoginFile) + "\n")
        out.write("## GLOBAL DEFAULT ##\n")
        out.write("add method     *    telnet ssh\n")
        out.close
        os.chmod(clogin, S_IREAD | S_IWRITE)

        ## generate a cloginrc that can be used for customized settings
        self.generate_customized_cloginrc()

    # create the framework for the custom DB files
    def generateCustomDbPath(self):
        path = zenPath('rancid', 'etc','customdb')
        if not os.path.isdir(path):
            os.mkdir(path, 0750)
        out = open(zenPath('rancid', 'etc','customdb', 'readme'), 'w')
        out.write("# create your own custom router.db files for devices which are not managed in Zenoss\n")
        out.write("# create the same folder structure as exists in rancid/var and put your own router.db file inside\n")
        out.close()

    # TODO: add custom router.db
    def generate_router_db(self):
        db_files = {}
        customdb_files = {}
        for dev in self._rancid:
            if not (dev['id'] and dev['group'] and dev['deviceType']): continue
            
            groupDir = zenPath('rancid', 'var', dev['group'])
            routerDbFile = os.path.join(groupDir, "router.db")
            
            if os.path.exists(groupDir):
                if not routerDbFile in db_files:
                    db_files[routerDbFile] = []
                # store router.db in lower case
                db_files[routerDbFile].append(":".join((dev['id'], dev['deviceType'], "up")))

        for file in db_files:
            # hack to force lower case
            out = open(file, 'w')
            for router in db_files[file]:
                out.write(str(router).lower() + "\n")

            # check if a custom router.db file exists in rancid/etc/customdb
            customDbFile = re.sub(zenPath('rancid', 'var'), zenPath('rancid', 'etc', 'customdb'), file)
            if os.path.exists(customDbFile):
                with open(customDbFile) as f:
                    for line in f.readlines():
                        out.write(str(line))


            out.close()


    def generate_customized_cloginrc(self):
        custom_clogin = os.path.join(self.rancid_path, self.cCustomLoginFile)
        if not os.path.exists(custom_clogin):
            out = open(custom_clogin, 'w')
            out.write("## save customized changes to .cloginrc below this line ##\n")
            out.close()
        os.chmod(custom_clogin, S_IREAD | S_IWRITE)


    def generate_rancid_logrotate_file(self):
        file = os.path.join(self.rancid_path, 'etc', 'zenoss-rancid.logrotate')
        logfiles = os.path.join(self.rancid_path, 'var/logs/')
        rotateFile = "%s {\n" \
                    "missingok\n" \
                    "weekly\n" \
                    "rotate 2\n" \
                    "copytruncate\n" \
                    "}" % (logfiles)

        if os.path.exists(os.path.join(self.rancid_path, 'etc')):
            out = open(file, 'w')
            out.write(rotateFile)
            out.close()


    # TODO: create rancid events
    def run_rancid(self, dev='', grp=''):
        if self.options.rDevice:
            # try to find the device in zenoss
            device = self.dmd.Devices.findDevice(self.options.rDevice)
            if not device:
                log.error('FAILED: device not found in Zenoss: %s', self.options.rDevice)
                return False
            group = device.zRancidGroup
            id = device.id.lower()
            type = device.zRancidDeviceType
            log.info('Starting Rancid for device %s', id)
            cmd = os.path.join(self.rancid_path, 'bin/rancid-run') + ' -r ' + id + ' ' + group
        else:
            cmd = os.path.join(self.rancid_path, 'bin/rancid-run')
        #os.system("$ZENHOME/bin/zensendevent --severity Info -p rancid -c /App/Rancid rancid-cvs has finished")
        log.debug('running command: "%s"', cmd)
        if os.system(cmd): 
            os.system("$ZENHOME/bin/zensendevent --severity Error -p rancid -c /App/Rancid rancid-run has failed")
            return - 1
        else:
            os.system("$ZENHOME/bin/zensendevent --severity Info -p rancid -c /App/Rancid rancid-run has finished successfully")



    def run_rancid_cvs(self):
        cmd = os.path.join(self.rancid_path, 'bin/rancid-cvs')
        if os.system(cmd): 
            os.system("$ZENHOME/bin/zensendevent --severity Error -p rancid -c /App/Rancid rancid-cvs has failed")
            return - 1
        else:
            os.system("$ZENHOME/bin/zensendevent --severity Info -p rancid -c /App/Rancid rancid-cvs has finished successfully")


    def generate_conf(self):
        rcssys = "svn"
        if self.standalone:
            rcssys = self.options.rancid_rcssys
            
        ## TODO: add version parameter here
        template = "# rancid %s\n" \
            "LD_LIBRARY_PATH=;\n" \
            "TERM=network;export TERM\n" \
            "umask 027\n" \
            "TMPDIR=/tmp; export TMPDIR\n" \
            "RANCIDDIR=%s; export RANCIDDIR\n" \
            "BASEDIR=$RANCIDDIR/var; export BASEDIR\n" \
            "PATH=$PATH:$RANCIDDIR/bin:/usr/bin:/usr/sbin:.:/bin:/usr/local/bin:/usr/bin; export PATH\n" \
            "CVSROOT=$BASEDIR/CVS; export CVSROOT\n" \
            "LOGDIR=$BASEDIR/logs; export LOGDIR\n" \
            "RCSSYS=%s; export RCSSYS\n" \
            "#NOPIPE=YES; export NOPIPE\n" \
            "#FILTER_PWDS=YES; export FILTER_PWDS\n" \
            "#NOCOMMSTR=YES; export NOCOMMSTR\n" \
            "#MAX_ROUNDS=4; export MAX_ROUNDS\n" \
            "#OLDTIME=4; export OLDTIME\n" \
            "#LOCKTIME=4; export LOCKTIME\n" \
            "#PAR_COUNT=5; export PAR_COUNT\n" \
            "LIST_OF_GROUPS=\"%s\"\n" \
            "#   rancid-group:    joe,moe@foo\n" \
            "#   rancid-admin-group:    hostmaster\n" \
            "#MAILDOMAIN=\"@example.com\"; export MAILDOMAIN\n" \
            "#MAILHEADERS=\"Precedence: bulk\"; export MAILHEADERS\n" \
            "# this file will be overwritten, if you want to customize it, override changes in the following file\n" \
            ". $RANCIDDIR/etc/%s\n" % (self.RANCID_VERSION, self.rancid_path, rcssys, " ".join(set(self._list_of_groups)), self.customConfigFile )

        out = open(os.path.join(self.rancid_path, 'etc', self.configFile), 'w')
        out.write(template)
        out.close()

        ## make sure the imported customized conf file exists
        self.generate_customized_conf()
      

    def generate_customized_conf(self):
        confFile = os.path.join(self.rancid_path, 'etc', self.customConfigFile)
        if not os.path.exists(confFile):
            out = open(confFile, 'w')
            out.write("## save customized changes to rancid.conf below this line ##\n")
            out.close()



if __name__ == '__main__':
    #import logging
    #logging.getLogger('zen.rancidtest').setLevel(80)
    rancidDaemon = rancidd()
    rancidDaemon.run()

