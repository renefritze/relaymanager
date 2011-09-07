import string

import tasbot
from tasbot.plugin import IPlugin
from tasbot.utilities import *


class Main(IPlugin):
	def __init__(self,name,tasclient):
		IPlugin.__init__(self,name,tasclient)

	def onload(self,tasc):
		self.app = tasc.main

	def oncommandfromserver(self, command, args, socket):
		if command == "SAIDPRIVATE" and len(args) >= 2:
			if args[1].lower() == "!listmanagers":
				socket.send("SAYPRIVATE %s managerlist %s\n" % ( args[0] , '\t'.join(self.app.config.get_optionlist('relaymanager', "managerlist"))))
			elif args[1].lower() == "!lm":
				socket.send("SAYPRIVATE %s list %s\n" % ( args[0] , '\t'.join(self.app.config.get_optionlist('relaymanager', "managerlist"))))
			elif args[0] in self.app.config.get_optionlist('tasbot',"admins") and len(args) >= 3:
				cmns = self.app.config.get_optionlist('relaymanager',"managerlist")
				if args[1].lower() == "!addmanager":
					if args[2] in cmns:
						socket.send("SAYPRIVATE %s %s\n" % ( args[0] , "Manager already in the list"))
					else:
						cmns.append(args[2])
						self.app.config.set('relaymanager',"managerlist", ','.join(cmns) )
						self.app.save_config()
					socket.send("SAYPRIVATE %s %s\n" % ( args[0] , "Manager added"))
				if args[1].lower() == "!removemanager":
					if not args[2] in cmns:
						socket.send("SAYPRIVATE %s %s\n" % ( args[0] , "Manager doesn't exist in list"))
					else:
						cmns.remove(args[2])
						self.app.config.set('relaymanager',"managerlist", ','.join(cmns) )
						self.app.save_config()
						socket.send("SAYPRIVATE %s %s\n" % ( args[0] , "Manager removed"))

	def onloggedin(self,socket):
		socket.send("JOIN autohost\n")

