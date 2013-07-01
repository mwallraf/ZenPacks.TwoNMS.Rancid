mport os
import commands

#def Test(self):
#    return "TEST VAN TEST"

#base_path = zenPath()
#ancid_path = zenPath('rancid') 
#os.popen("ls")
#return cmd
#return "TEST VAN PYTHON"
#return os.system(cmd)
def TestEen():
  cmd = "$ZENHOME/rancid/bin/rancid-svn cat $ZENHOME/rancid/var/Routers/configs/cisco888"
  a = commands.getoutput(cmd)
  return a
  #return "Dit is test een!"

