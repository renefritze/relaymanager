import string
helptext = "Relayed Host Bot\n Documentation is at http://springlobby.info/wiki/1/HostManagerProtocol"
from tasbot.plugin import IPlugin

class Main(IPlugin):
        def __init__(self,name,tasclient):
                IPlugin.__init__(self,name,tasclient)

	def oncommandfromserver(self,command,args,socket):
		
		if command == "SAIDPRIVATE" and len(args) > 1 and args[1] == "!help":
			for l in helptext.split("\n"):
				socket.send("SAYPRIVATE %s %s\n" % (args[0],l))
