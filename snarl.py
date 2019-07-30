import re
import os
import sys
import socket
import argparse
import threading
import subprocess
from pull import PULL
from web  import APP
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application 

pull = PULL()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Snarl.settings')

class EXECUTIONER:

	def __init__(self, bd, pt):
		self.address = bd
		self.port    = pt

	def bind(self):
		application = get_wsgi_application()

class PARSER:

	def __init__(self, opts):
		self.bind = self.bind( opts.bind )
		self.port = self.port( opts.port )
		self.conn = self.conn( self.bind, self.port )

	def bind(self, bd):
		if bd:
			if re.match( r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", bd ) or re.match(r"^([a-z0-9|-]+\.)*[a-z0-9|-]+\.[a-z]+$", bd):
				return bd
			else:
				pull.halt( "Not a Valid IP Address Or Domain.", pull.RED, pull.BOLD )
		else:
			pull.halt( "Halt! Binding Address Not Provided.", pull.RED, pull.BOLD )

	def port(self, pt):
		if pt > 0 and pt < 65536:
			return pt
		else:
			pull.halt( "Invalid Port! Must be in Range 1-65535", pull.RED, pull.BOLD )

	def conn(self, bd, pt):
		try:
			s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
			s.bind((bd, pt))
			s.close()
		except:
			pull.halt( "Invalid Binding Address. Not able to Bind to: %s:%i" % (bd, pt), pull.RED, pull.BOLD )

def main():
	parser = argparse.ArgumentParser()

	parser.add_argument( '-b', '--bind', dest="bind", default=None, type=str )
	parser.add_argument( '-p', '--port', dest="port", default=8080, type=int )

	options = parser.parse_args()

	parser = PARSER( options )

	pull.gthen( "Firing UP Snarl. Have a Seat! ", pull.DARKCYAN )
	picker = EXECUTIONER( parser.bind, parser.port )
	picker.bind()
	pull.lthen( "Exiting!", pull.RED )

if __name__ == "__main__":
	main()