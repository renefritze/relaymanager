# -*- coding: utf-8 -*-
from colors import *
import string
import time, datetime
import tasbot
from tasbot.utilities import *
def elapsed_time(seconds, suffixes=['y','w','d','h','m','s'], add_s=False, separator=' '):
	"""
	Takes an amount of seconds and turns it into a human-readable amount of time.
	"""
	# the formatted time string to be returned
	time = []

	# the pieces of time to iterate over (days, hours, minutes, etc)
	# - the first piece in each tuple is the suffix (d, h, w)
	# - the second piece is the length in seconds (a day is 60s * 60m * 24h)
	parts = [(suffixes[0], 60 * 60 * 24 * 7 * 52),
		  (suffixes[1], 60 * 60 * 24 * 7),
		  (suffixes[2], 60 * 60 * 24),
		  (suffixes[3], 60 * 60),
		  (suffixes[4], 60),
		  (suffixes[5], 1)]

	# for each time piece, grab the value and remaining seconds, and add it to
	# the time string
	for suffix, length in parts:
		value = round(seconds / length)
		if value > 0:
			seconds = seconds % length
			time.append('%s%s' % (str(value),
					       (suffix, (suffix, suffix + 's')[value > 1])[add_s]))
		if seconds < 1:
			break

	return separator.join(time)

bstr_nonneg = lambda n: n>0 and bstr_nonneg(n>>1).lstrip('0')+str(n&1) or '0'
class UserStatus:
	def __init__(self, status, nick ):
		sstr = bstr_nonneg( int(status) ).rjust( 31, "0" )
		self.ingame = ( sstr[ -1 : 0 ] == "1" )
		self.nick = nick
		self.decimal = int(status)

from tasbot.Plugin import IPlugin

class Main(IPlugin):
        def __init__(self,name,tasclient):
                IPlugin.__init__(self,name,tasclient)

		self.slavetomanager = dict()
		self.slavetousagecount = dict()
		self.slavetoingamecount = dict()
		self.battlestartingtime = dict()
		self.managerlist = []
		self.statsfilename = "relaystats.txt"
	def onload(self,tasc):
		self.app = tasc.main
		self.tasc = tasc
		self.managerlist = tasbot.ParseConfig.parselist(self.app.config["managerlist"],',')
		self.loadStats()
	def oncommandfromserver(self,command,args,socket):
		if command == "SAIDPRIVATE" and len(args) > 1 and args[1] == "!stats":
			if len(args) > 3:
				return
			managertoingamecount = dict()
			managertousagecount = dict()
			for slavename in self.slavetomanager:
				managername = self.slavetomanager[slavename]
				if not managername in managertoingamecount:
					managertoingamecount[managername] = 0
				if not managername in managertousagecount:
					managertousagecount[managername] = 0
				if slavename in self.slavetoingamecount:
					managertoingamecount[managername] = managertoingamecount[managername] + self.slavetoingamecount[slavename]
				if slavename in self.slavetousagecount:
					managertousagecount[managername] = managertousagecount[managername] + self.slavetousagecount[slavename]
			if len(args) == 2:
				for managername in managertoingamecount:
					ingame = elapsed_time( managertoingamecount[managername] )
					socket.send("SAYPRIVATE %s %s was used %d times, and accumulated %s of ingame time\n"% \
						(args[0], managername, managertousagecount[managername], ingame ) )
			elif len(args) == 3 and args[2] in self.managerlist:
				managername = args[2]
				if managername in managertoingamecount:
					ingame = elapsed_time( managertoingamecount[managername] )
					socket.send("SAYPRIVATE %s %s was used %d times, and accumulated %s of ingame time\n"% \
						(args[0], managername, managertousagecount[managername], ingame ) )
				for slavename in self.slavetomanager:
					if self.slavetomanager[slavename] == managername:
						if slavename in self.slavetousagecount and slavename in self.slavetoingamecount:
							ingame = elapsed_time( self.slavetoingamecount[slavename] )
							socket.send("SAYPRIVATE %s %s was used %d times, and accumulated %s of ingame time\n"% \
								(args[0], slavename, slavetousagecount[managername], ingame ) )
		if command == "SAID" and len(args) > 4 and args[0] == "autohost":
			sender = args[1]
			self.managerlist = tasbot.ParseConfig.parselist(self.app.config["managerlist"],',')
			if sender in self.managerlist and args[2] == "Spawning":
				botname = args[len(args)-1]
				self.slavetomanager[botname] = sender
		if command == "CLIENTSTATUS" and len(args) > 1 and args[0] in self.slavetomanager:
			slavename = args[0]
			ingame = ( int(args[1]) % 2 ) == 1
			print slavename + " got ingame " + str(ingame)
			now = time.time()
			if not ingame and slavename in self.battlestartingtime:
				deltatime = now - self.battlestartingtime[slavename]
				del self.battlestartingtime[slavename]
				managername = self.slavetomanager[slavename]
				if not slavename in self.slavetousagecount:
					self.slavetousagecount[slavename] = 0
				if not slavename in self.slavetoingamecount:
					self.slavetoingamecount[slavename] = 0
				self.slavetousagecount[slavename] = self.slavetousagecount[slavename] + 1
				self.slavetoingamecount[slavename] = self.slavetoingamecount[slavename] + deltatime
				self.saveStats()
			if ingame and not slavename in self.battlestartingtime:
				self.battlestartingtime[slavename] = now
	def loadStats( self ):
		statsfile = open(self.statsfilename,'r')
		content = statsfile.read()
		entries = content.split("\n")
		for line in entries:
			data = line.split("\t")
			if data[0] == "slavetomanager":
				self.slavetomanager[data[1]] = data[2]
			if data[0] == "slavetousagecount":
				self.slavetousagecount[data[1]] = int(data[2])
			if data[0] == "slavetoingamecount":
				self.slavetoingamecount[data[1]] = float(data[2])
		statsfile.close()
	def saveStats( self ):
		statsfile = open(self.statsfilename,'w')
		for key,value in self.slavetomanager.items():
			statsfile.write( "slavetomanager\t" + key + "\t" + str(value) + "\n" )
		for key,value in self.slavetousagecount.items():
			statsfile.write( "slavetousagecount\t" + key + "\t" + str(value) + "\n" )
		for key,value in self.slavetoingamecount.items():
			statsfile.write( "slavetoingamecount\t" + key + "\t" + str(value) + "\n" )
		statsfile.flush()
		statsfile.close()

