#!/usr/bin/python

import os
import sys
import time
import update

def daemon():
	try:
		pid = os.fork()
		if pid > 0:
			print 'Daemon father 1 exit'
			os._exit(0)
	except OSError, error:
		print 'fork 1 error'
		os._exit(1)
	
	os.setsid()
	os.umask(0)

	try:
		pid = os.fork()
		if pid > 0:
			print 'Daemon father 2 exit'
			os._exit(0)
	except OSError, error:
		print 'fork 2 failed'
		os._exit(1)

	sys.stdout.flush()
	sys.stderr.flush()
	si = file('/dev/null', 'r')
	so = file('/dev/null', 'a+')
	se = file('/dev/null', 'a+', 0)
	os.dup2(si.fileno(), sys.stdin.fileno())
	os.dup2(so.fileno(), sys.stdout.fileno())
	os.dup2(se.fileno(), sys.stderr.fileno())

def function():
	while True:
		time.sleep(660)
		update.mainloop()
		time.sleep(720)
		
if __name__ == '__main__':
	daemon()
	function()
