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
			ffile.write( key + "=" + repr(self.VARIABLES[key]) + "\n" )
		ffile.close()

	def generate(self):
		ffile = open(self.SETTPATH, "w")
		ffile.write( 'import os\n\n' )
		ffile.write( 'BASE_DIR="{}"\n'.format( self.BASEPATH ) )
		for key in list( self.VARIABLES.keys() ):
			if key == "SECKEY":
				ffile.write('SECRET_KEY={}\n'.format(repr(self.VARIABLES[ "SECKEY" ])))
			elif key == "DEBUG":
				ffile.write('DEBUG={}\n'.format(repr(self.VARIABLES[ "DEBUG" ])))
			elif key == "ALLHOS":
				ffile.write('ALLOWED_HOSTS={}\n'.format(repr(self.VARIABLES[ "ALLHOS" ])))
			elif key == "INAPPS":
				ffile.write('INSTALLED_APPS={}\n'.format(repr(self.VARIABLES[ "INAPPS" ])))
			elif key == "MDWARE":
				ffile.write('MIDDLEWARE={}\n'.format(repr(self.VARIABLES[ "MDWARE" ])))
			elif key == "ULCONF":
				ffile.write('ROOT_URLCONF={}\n'.format(repr(self.VARIABLES["ULCONF"])))
			elif key == "TEMPLS":
				ffile.write('TEMPLATES={}\n'.format(repr(self.VARIABLES["TEMPLS"])))
			elif key == "WSGAPP":
				ffile.write('WSGI_APPLICATIUON={}\n'.format(repr(self.VARIABLES["WSGAPP"])))
			elif key == "DBASES":
				ffile.write('DATABASES={}\n'.format(repr(self.VARIABLES["DBASES"])))
			elif key == "AUVALI":
				ffile.write('AUTH_PASSWORD_VALIDATORS={}\n'.format(repr(self.VARIABLES["AUVALI"])))
			elif key == "LNCODE":
				ffile.write('LANGUAGE_CODE={}\n'.format(repr(self.VARIABLES["LNCODE"])))
			elif key == "TMZONE":
				ffile.write('TIME_ZONE={}\n'.format(repr(self.VARIABLES["TMZONE"])))
			elif key == "USIIBN":
				ffile.write('USE_I18N={}\n'.format(repr(self.VARIABLES["USIIBN"])))
			elif key == "USETZI":
				ffile.write('USE_L10N={}\n'.format(repr(self.VARIABLES["USETZI"])))
			elif key == "STAURL":
				ffile.write('STATIC_URL={}\n'.format(repr(self.VARIABLES['STAURL'])))
			elif key == "STROOT":
				ffile.write('STATIC_ROOT={}\n'.format(repr(self.VARIABLES['STROOT'])))
			elif key == "JMENUI":
				ffile.write('JET_SIDE_MENU_ITEMS={}\n'.format(repr(self.VARIABLES['JMENUI'])))
			elif key == "JDEFTH":
				ffile.write('JET_DEFAULT_THEME={}\n'.format(repr(self.VARIABLES['JDEFTH'])))
		ffile.close()

	def extend(self, addr):
		if self.VARIABLES[ "DBNAME" ] and self.VARIABLES[ "DBSVER" ] and self.VARIABLES[ "DBUSER" ] and self.VARIABLES[ "DBPASS" ]:
			self.VARIABLES[ "DBASES" ] = {
    			'default': {
        			'ENGINE': 'django.db.backends.mysql',
        			'NAME': self.VARIABLES[ "DBNAME" ],
        			'USER': self.VARIABLES[ "DBUSER" ],
        			'PASSWORD': self.VARIABLES[ "DBPASS" ],
        			'HOST': self.VARIABLES[ "DBSVER" ],
        			'PORT': ''
    			}
			}
		else:
			self.VARIABLES[ "DBASES" ] = {
    			'default': {
        			'ENGINE': 'django.db.backends.sqlite3',
        			'NAME': os.path.join(self.BASEPATH, 'db.sqlite3'),
    				}
			}
		self.VARIABLES[ "STROOT" ] = os.path.join( self.BASEPATH, "static" )
		self.VARIABLES[ "ALLOWED_HOSTS" ] = []
		if addr:
			self.VARIABLES[ "ALLOWED_HOSTS" ].append( addr )


