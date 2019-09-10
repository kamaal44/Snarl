import re
import os
import sys
import time
import signal
import django
import socket
import psutil
import pymysql
import logging
import argparse
import threading
import subprocess
from pull import PULL
from config import CONFIG
from django.core.wsgi import get_wsgi_application as GETWSGI
from django.core.management import call_command as DJANGOCALL

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Snarl.settings')
pull = PULL()

class EXECUTIONER:

	def __init__(self, bd, pt, npt, dbg):
		self.address  = bd
		self.port     = pt
		self.npointer = npt
		self.debug    = dbg

	def bind(self):
		application = GETWSGI()
		pull.print("^", "Binding the Server to Address: %s:%s" % (self.address, self.port), pull.DARKCYAN)
		pull.print("*", "You can Access Your Application Now!", pull.YELLOW)
		if self.debug:
			pull.linebreak(1)
			DJANGOCALL(
				'runserver', 
				"{}:{}".format(self.address, self.port),
				stdout=sys.stdout
			)
		else:
			DJANGOCALL(
				'runserver', 
				"{}:{}".format(self.address, self.port),
				'--noreload',
				stdout=self.npointer
			)

class PARSER:

	def __init__(self, opts):
		self.help      = self.help( opts.help )

		self.npointer  = open(os.devnull, "w")
		self.verbose   = opts.verbose
		self.debug     = opts.debug
		self.bind      = self.bind(    opts.bind     )
		self.port      = self.port(    opts.port     )

		self.signal    = signal.signal( signal.SIGINT, self.handler )

		self.configure = self.configure( opts.configure )
		self.migrate   = self.migrate( opts.migrate  )
		self.init      = self.initialize( self.bind )
		self.cuser     = self.create( opts.cuser )
		self.conn      = self.conn(    self.bind, self.port )

	def handler(self, sig, fr):
		pull.halt(
			"Cleaning Processes and Exiting ...", (True if not self.debug else False), "\r", pull.RED
			)
		for proc in psutil.process_iter():
			try:
				pname = proc.name()
				piden = proc.pid

				if pname == "python" or pname == "python3":
					os.kill( piden, signal.SIGKILL )
			except:
				pass

	def help(self, bl):
		if bl:
			pull.help()

	def configure(self, conf):
		if conf:
			toset = pull.input("-", "Do you Want To Configure Your Database Credentials? [Y/n] ", ("y", "n"), pull.BLUE)
			if toset:

				dbase = pull.input("?", "Enter Your Database Name: ", False, pull.GREEN)
				serve = pull.input("?", "Enter Your Server Name [localhost]: ", False, pull.GREEN)
				uname = pull.input("?", "Enter Database Username: ", False, pull.GREEN)
				passw = pull.input("?", "Enter Database Password: ", False, pull.GREEN)

				pull.print("^", "Checking Database Connection. Connecting!", pull.DARKCYAN )
				try:
					pymysql.connect(serve, uname, passw, dbase)
				except pymysql.err.OperationalError:
					pull.halt("Access Denied for the user. Check Credentials and Server Status!", True, pull.RED)

				config = CONFIG()
				config.read_variables()
				config.db_create(dbase, serve, uname, passw)
				config.write_variables()

			else:
				pull.print("*", "Skipped Configuration of Database. Proceeding now. ", pull.YELLOW)

			pull.halt("Done Configurations. Exiting", True, pull.RED)

	def migrate(self, mig):
		if mig:
			pull.print(
				"*", "Migration Phase. Initializing File & Configurations.", pull.YELLOW
			)

			config = CONFIG()
			config.read_variables()
			config.generate_key()
			config.write()

			time.sleep( 3 )
			application = GETWSGI()

			pull.print("^", "Configuration Done. Uprnning Migrations Now. ", pull.DARKCYAN)
			DJANGOCALL('makemigrations', stdout=(sys.stdout if self.debug else self.npointer))
			pull.verbose("*", "Files Modified. Running Into Final Stage. ", self.verbose, pull.YELLOW)
			DJANGOCALL('migrate', stdout=(sys.stdout if self.debug else self.npointer))
			pull.halt("Migrations Applied Successfuly. Exiting Now!", True, pull.GREEN)

			return True
		return False

	def create(self, cuser):
		if cuser:
			django.setup()
			from django.contrib.auth.models import User as SUPERUSER
			uname = pull.input("?", "Enter Username for the admin user: ", False, pull.YELLOW )
			email = pull.input("?", "Enter Email for the user: ", False, pull.YELLOW )
			passw = pull.input("?", "Enter Password for the user: ", False, pull.YELLOW )

			if uname and passw:
				SUPERUSER.objects.create_superuser( uname, email, passw )
				pull.halt( "User Created Successfuly", True, pull.GREEN )
			else:
				pull.halt( "Username & Password Fields Are Mandatory & Must be Supplied", True, pull.RED )

	def initialize(self, addr=""):
		config = CONFIG()

		if os.path.isfile(config.SETTPATH) or self.migrate:
			config.read()
			config.extend(
				addr,
				self.debug
			)
			config.generate()
		else:
			pull.halt("Migrations aren't applied. Apply them first!", True, pull.RED)

	def bind(self, bd):
		if bd:
			if re.match( r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", bd ):
				return bd
			else:
				pull.halt( "Not a Valid IP Address.", True, pull.RED, pull.BOLD )
		else:
			pull.halt( "Halt! Binding Address Not Provided. See Manual", True, pull.RED, pull.BOLD )

	def port(self, pt):
		if pt > 0 and pt < 65536:
			return pt
		else:
			pull.halt( "Invalid Port! Must be in Range 1-65535", True, pull.RED, pull.BOLD )

	def conn(self, bd, pt):
		try:
			s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
			s.bind((bd, pt))
			s.close()
		except:
			pull.halt( "Not able to Bind to Address. Check Your Address & Port!", True, pull.RED, pull.BOLD )

def main():
	parser = argparse.ArgumentParser( add_help=False )

	parser.add_argument( '-h', '--help'   , dest="help"     , default=False, action="store_true" )
	parser.add_argument( '-b', '--bind'   , dest="bind"     , default=None , type=str            )
	parser.add_argument( '-p', '--port'   , dest="port"     , default=8080 , type=int            )
	parser.add_argument( '-v', '--verbose', dest="verbose"  , default=False, action="store_true" )
	parser.add_argument( '-d', '--debug'  , dest="debug"    , default=False, action="store_true" )
	parser.add_argument( '--migrate'      , dest="migrate"  , default=False, action="store_true" )
	parser.add_argument( '--configure'    , dest="configure", default=False, action="store_true" )
	parser.add_argument( '--create-user'  , dest="cuser"    , default=False, action="store_true" )

	pull.print("^", "Parsing Uplifting Configurations and Files. ", pull.DARKCYAN)
	options = parser.parse_args()
	parser = PARSER( options )
	pull.print("*", "Got Clean Status. Processing now. ", pull.YELLOW)

	pull.print(">", "Firing UP Snarl. Have a Seat! ", pull.DARKCYAN )
	picker = EXECUTIONER(
		parser.bind,
		parser.port,
		parser.npointer,
		parser.debug
	)
	picker.bind()
	pull.print("<", "Exiting!", pull.RED )

if __name__ == "__main__":
	pull.logo()
	main()