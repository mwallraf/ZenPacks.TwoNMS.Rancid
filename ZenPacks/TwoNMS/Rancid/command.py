import Globals
import os
import commands
from Products.ZenUtils.Utils import executeCommand
from Products.ZenUtils.jsonutils import unjson
from Products.Zuul import getFacade
from Products.ZenUI3.browser.streaming import StreamingView
import logging
log = logging.getLogger('zen.ZenPack')



class MyPredefinedCommandView(StreamingView):

    def __init__(self, context, request, test="None"):
        super(MyPredefinedCommandView, self).__init__(context, request)

    def stream(self):
# Setup a logging file
        logfile = open('/opt/zenoss/log/rancid_example_logging.log', 'a')
        logfile.write('Start logging')
        # data is a list that will contain 2 elemets:
        #   the url argument and the uid

        
        #self.write('TEST parameter = %s\n' % (self.request.arguments()))
        
        data = unjson(self.request.get('data'))
        self.write('data stream = %s\n' % (data))
        
        #data = ""
        
        logfile.write(' data is %s \n' % (data))
        try:
            args = data['args']
            logfile.write('Argument is %s \n' % (args))
            arg3 = args
        except:
            logfile.write(' No args \n')
            arg3 = ''
        try:
            uids = data['uids']
            logfile.write('uids is %s \n' % (uids))
            arg4 = uids
        except:
            logfile.write('No uids \n')
            arg4 = ''

        libexec = os.path.join(os.path.dirname(__file__), 'libexec')

        arg1 = "Hello"
        arg2 = "World"
        
# Put the  script in the libexec directory of the ZenPack
        myPredefinedCmd1 = [
             #libexec + '/mywrapper_script1',
             #"ls -a"
            #arg1, arg2, arg3, arg4
            "find",
            "/tmp"
        ]
        logfile.write(' myPredefinedCmd1 is %s ' % (myPredefinedCmd1))
        self.write('Preparing my command...')
        result = executeCommand(myPredefinedCmd1, None, write=self.write)
        #logfile.write(result)
        #self.write(result)
        self.write('End of command...')
        logfile.close()
        return result


