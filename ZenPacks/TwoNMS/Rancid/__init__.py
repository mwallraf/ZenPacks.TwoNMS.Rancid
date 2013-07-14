import Globals
import os
import shutil
import logging
import sys

from Products.ZenModel.ZenPack import ZenPackBase
from Products.ZenUtils.Utils import zenPath
from Products.ZenModel.ZenossSecurity import ZEN_VIEW
from Products.ZenModel.Device import Device
#from ZenRancid import ZenRancid
from rancidd import rancidd
from Products.ZenUtils.ZenScriptBase import ZenScriptBase
from Products.CMFCore.utils import getToolByName
from Products.ExternalMethod.ExternalMethod import manage_addExternalMethod
from transaction import commit
from Products.ZenRelations.RelSchema import ToManyCont, ToOne

from Products.ZenModel.OperatingSystem import OperatingSystem

"""
skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())
""" 
   
# TODO: START DAEMON AFTER INSTALLATION


log = logging.getLogger('zen.rancidd')
OperatingSystem._relations += (("rancidrevs", ToManyCont(ToOne, "ZenPacks.TwoNMS.Rancid.RancidRevision", "os")),)

## TODO: copy wrapper to $ZENHOME/Extensions folder

class ZenPack(ZenPackBase):

    # RANCID VERSION (available on shrubbery.net)
    RANCID_VERSION = ""

    # Rancid base_path = $ZENHOME/rancid
    base_path = zenPath('rancid')
    zenpack_path = os.path.dirname(__file__)
    rancid_tar = ""
    # find the zenoss homedir to store .cloginrc
    homedir_path = os.path.expanduser('~zenoss')

    ## TODO: new method for this ??
    # add extra zProperties    
    packZProperties = [
            ('zRancidGroup', 'Routers', 'string'),
            ('zRancidUser', '', 'string'),
            ('zRancidPassword', '', 'password'),
            ('zRancidEnablePassword', '', 'password'),
            ('zRancidDeviceType', 'cisco', 'string'),
            ('zRancidIgnore', True, 'boolean'),
            ('zRancidSSH', False, 'boolean'),
            ('zRancidViewerPath', '', 'string')
            ]

    def __init__(self, *args):
        ## Verify installation pre-requisites before trying to install the package
        try:
          log.debug('Checking pre-requisites')
          self.check_prereqs()
        except:
            log.error('Installation failed because. Make sure you have at least the following installed: expect, tar, make, gcc, subversion')
            log.critical('--- INSTALLATION OF ZenPacks.TwoNMS.Rancid FAILED ---')
            sys.exit(0)

        super(ZenPack,self).__init__(*args)
        self.RANCID = rancidd(False)
        self.RANCID_VERSION = self.RANCID.getRancidVersion()
        self.rancid_tar = os.path.join(self.zenpack_path, 'resources', "rancid-" + self.RANCID_VERSION + ".tar.gz")



    def install(self, app):
        ZenPackBase.install(self, app)
        log.info("Starting installation of ZenPacks.TwoNMS.Rancid (rancid v" + self.RANCID_VERSION + ")")
        self.install_rancid(app)

        for d in self.dmd.Devices.getSubDevices():
            d.os.buildRelations()

            
    #  TODO: extra checks
    #          OS - unix only !!
    def check_prereqs(self):
        ## testing
        ##raise Exception("TEST FAIL")
        
        ## verify expect
        log.debug('Looking for excpect')
        cmd = 'expect -v'
        if os.system(cmd + ' 2>&1 > /dev/null'):
            raise Exception("Cannot find 'expect': install expect or verify PATH and try again")

        ## verify tar
        log.debug('Looking for tar')
        cmd = 'tar --version'
        if os.system(cmd + ' 2>&1 > /dev/null'):
            raise Exception("Cannot find 'tar': install tar or verify PATH and try again")

        ## verify make
        log.debug('Looking for make')
        cmd = 'make -v'
        if os.system(cmd + ' 2>&1 > /dev/null'):
            raise Exception("Cannot find 'make': install make or verify PATH and try again")

        ## verify gcc
        log.debug('Looking for gcc')
        cmd = 'gcc --help'
        if os.system(cmd + ' 2>&1 > /dev/null'):
            raise Exception("Cannot find 'gcc': install gcc or verify PATH and try again")

        ## verify svn
        ## TODO: check for svn or cvs + check for svn-devel
        log.debug('Looking for Subversion')
        cmd = 'svn --version --quiet'
        if os.system(cmd + ' 2>&1 > /dev/null'):
            raise Exception("Cannot find 'svn': install subversion or verify PATH and try again")



    def install_rancid(self, app):            
      ## extract + build rancid to make sure it runs on each installation
      tarfile = self.rancid_tar
      tmpDir = "/tmp"
      installDir = "rancid-%s" % (self.RANCID_VERSION)
      
      # extract rancid tarfile to tmpdir
      cmd = 'tar xzfC %s %s' % (tarfile, tmpDir)
      log.debug("Unpacking rancid : %s" % cmd)
      if os.system(cmd): return -1
      
      # configure + make rancid
      #cmd = 'cd /' + tmpDir + '/' + installDir + ';./configure --prefix=' + self.base_path + ' 2>&1 > /dev/null;make 2>&1 > /dev/null;make install 2>&1 > /dev/null'
      cmd = 'cd /%s/%s;./configure --prefix=%s  2>&1 > /dev/null;make 2>&1 > /dev/null;make install 2>&1 > /dev/null' % (tmpDir, installDir, self.base_path)
      log.info("Compiling rancid - this may take a few minutes")
      if os.system(cmd): return -1
      log.debug("%s" % cmd)

      # remote the temp dir
      try:
          shutil.rmtree(tmpDir + "/" + installDir)
      except OSError:
          log.error("FAILED - unable to remove temp dir")
      finally:
          log.debug("removing temp dir %s" % tmpDir + "/" + self.rancid_tar)
      
      # create empty daemon config file
      configFileName = zenPath('etc', 'zenrancid.conf')
      if not os.path.exists(configFileName):
          configFile = open(configFileName, 'w')
          configFile.write('# populate this file by running $ZENHOME/bin/zenrancid genconf > $ZENHOME/etc/zenrancid.conf\n')
          configFile.close()
          
      # initialize rancid files
      self.RANCID.setup()
      
      # create a symlink for libexec/zenrancid-cvs.sh
      self.installFile('libexec/zenrancid-cvs.sh', overwriteIfExists=True, symLink=True)




    def upgrade(self, app):
        ZenPackBase.upgrade(self, app)



    def remove(self, app, leaveObjects=False):
        ZenPackBase.remove(self, app, leaveObjects=False)

        OperatingSystem._relations = tuple([x for x in OperatingSystem._relations if x[0] not in ['rancidrevs']])
        for d in self.dmd.Devices.getSubDevices():
            d.os.buildRelations()

        if not leaveObjects:
            ## remove the rancid path entirely
            if os.path.exists(self.base_path):
                shutil.rmtree(self.base_path)

            ## remove .cloginrc file
            if os.path.exists(os.path.join(self.homedir_path, ".cloginrc")):
                os.remove(os.path.join(self.homedir_path, ".cloginrc"))
                
            # create a symlink for libexec/zenrancid-cvs.sh
            self.removeFile('libexec/zenrancid-cvs.sh')



