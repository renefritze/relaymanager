import string
import tasbot
from tasbot.Plugin import IPlugin
from tasbot.utilities import *
class Main(IPlugin):
	def __init__(self,name,tasclient):
		IPlugin.__init__(self,name,tasclient)
	def onload(self,tasc):
		self.app = tasc.main
	def oncommandfromserver(self,command,args,socket):
		if command == "SAIDPRIVATE" and len(args) >= 2:
			if args[1].lower() == "!listmanagers":
				socket.send("SAYPRIVATE %s managerlist %s\n" % ( args[0] , '\t'.join(tasbot.ParseConfig.parselist(self.app.config["managerlist"],','))))
			elif args[1].lower() == "!lm":
				socket.send("SAYPRIVATE %s list %s\n" % ( args[0] , '\t'.join(parselist(self.app.config["managerlist"],','))))
			elif args[0] in tasbot.ParseConfig.parselist(self.app.config["admins"],',') and len(args) >= 3:
				cmns = tasbot.ParseConfig.parselist(self.app.config["managerlist"],',')
				if args[1].lower() == "!addmanager":
					if args[2] in cmns:
						socket.send("SAYPRIVATE %s %s\n" % ( args[0] , "Manager already in the list"))
					else:
						cmns.append(args[2])
						self.app.config["managerlist"] = ','.join(cmns)
						self.app.SaveConfig()
					socket.send("SAYPRIVATE %s %s\n" % ( args[0] , "Manager added"))
				if args[1].lower() == "!removemanager":
					if not args[2] in cmns:
						socket.send("SAYPRIVATE %s %s\n" % ( args[0] , "Manager doesn't exist in list"))
					else:
						cmns.remove(args[2])
						self.app.config["managerlist"] = ','.join(cmns)
						self.app.SaveConfig()
						socket.send("SAYPRIVATE %s %s\n" % ( args[0] , "Manager removed"))
	def onloggedin(self,socket):
		socket.send("JOIN autohost\n")

