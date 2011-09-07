#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

import tasbot
from tasbot.customlog import Log

if __name__=="__main__":
	tasbot.check_min_version((1,))
	configfile = "Main.conf"
	config = tasbot.config.Config(configfile)
	Log.init( config.get('tasbot','logfile','relaymanager.log'), 'info', True )
	
	r = False
	for arg in sys.argv:
		if arg.strip() == "-r":
			r = True
			Log.Notice("Registering account")
	pidfile = config.get('tasbot','pidfile','relaymanager.pid')
	print 'using pidfile %s'%pidfile
	inst = tasbot.DefaultApp(configfile,pidfile,r,True)
	if bool(config.get( 'tasbot','debug', False )):
		inst.run()#exec in fg
	else:
		inst.start()

