#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tasbot,sys
from tasbot.customlog import Log

if __name__=="__main__":			
	configfile = "Main.conf"
	config = tasbot.ParseConfig.Config(configfile)
	Log.Init( config['logfile'], 'info', True )
	
	r = False
	for arg in sys.argv:
		if arg.strip() == "-r":
			r = True
			Log.Notice("Registering account")
	pidfile = config['pidfile']
	print 'using pidfile %s'%pidfile
	inst = tasbot.DefaultApp(configfile,pidfile,r,True)
	if bool(config.GetSingleOption( 'debug', False )):
		inst.run()#exec in fg
	else:
		inst.start()

