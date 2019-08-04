import os
import variables
from django.core.management.utils import get_random_secret_key as SECRET

class CONFIG:

	VARIABLES={}
	BASEPATH=os.path.dirname(os.path.abspath(__file__))
	SETTPATH=os.path.join(os.path.dirname(os.path.abspath(__file__)), "Snarl/settings.py")

	def read(self):
		attrs = vars(variables)
		for attr in list(attrs.keys()):
			if not attr.startswith( "__" ):
				self.VARIABLES[ attr ] = attrs[ attr ]

	def kgen(self):
		key = self.VARIABLES.get( "SECKEY" )
		if not key:
			key = SECRET()
			self.VARIABLES[ "SECKEY" ] = key

	def dgen(self, dbse, serv, user, passw):
		self.VARIABLES[ "DBNAME" ] = dbse
		self.VARIABLES[ "DBSVER" ] = serv
		self.VARIABLES[ "DBUSER" ] = user
		self.VARIABLES[ "DBPASS" ] = passw

	def write(self):
		fpath = os.path.join( self.BASEPATH, 'variables.py' )
		ffile = open( fpath, "w" )
		for key in list(self.VARIABLES.keys()):
			ffile.write(
				'{}="{}"\n'.format(
					key,
					self.VARIABLES[ key ]
				)
			)
		ffile.close()

