import os
import variables
from django.core.management.utils import get_random_secret_key as SECRET

class RETURNEE:

	def __init__(self, bpath):
		self.bpath = bpath

	def r_database(self, dbname, dbserv, dbuser, dbpassw):
		dbs = {
    		'default': {
        		'ENGINE': 'django.db.backends.mysql',
        		'NAME': dbname,
        		'USER': dbuser,
        		'PASSWORD': dbpassw,
        		'HOST': dbserv,
        		'PORT': ''
    		}
		}
		return dbs

	def r_static_dirs(self):
		retval = [
			os.path.join(self.BASEPATH, "static")
		]

		return retval

	def r_templates(self):
		retval = [
			os.path.join(self.BASEPATH, "templates")
		]

		return retval

class CONFIG:

	VARIABLES={}
	BASEPATH=os.path.dirname(os.path.abspath(__file__))
	SETRPATH=os.path.join(os.path.dirname(os.path.abspath(__file__)), "setter.py")
	SETTPATH=os.path.join(os.path.dirname(os.path.abspath(__file__)), "Snarl/settings.py")

	TOWRITTEN = [
		'SECRET_KEY',
		'DEBUG',
		'ALLOWED_HOSTS',
		'INSTALLED_APPS',
		'MIDDLEWARE',
		'ROOT_URLCONF',
		'TEMPLATES',
		'WSGI_APPLICATIUON',
		'DATABASES',
		'AUTH_PASSWORD_VALIDATORS',
		'LANGUAGE_CODE',
		'TIME_ZONE',
		'USE_I18N',
		'USE_L10N'
		'USE_TZ',
		'STATIC_URL',
		'STATICFILES_DIRS',
		'JET_DEFAULT_THEME',
		'JET_SIDE_MENU_ITEMS',
		'LOGGING_CONFIG',
		'LOGGING'
	]

	def __init__(self):
		self.returnee = RETURNEE(
			self.BASEPATH
		)

	def read_variables(self):
		if os.path.isfile( self.SETRPATH ):
			import setter
			attrs = vars(setter)
		else:
			attrs = vars(variables)

		for attr in list(attrs.keys()):
			if not attr.startswith( "__" ):
				self.VARIABLES[ attr ] = attrs[ attr ]

	def write_variables(self):
		fpath = os.path.join( self.BASEPATH, 'setter.py' )
		ffile = open( fpath, "w" )
		for key in list(self.VARIABLES.keys()):
			ffile.write( key + "=" + repr(self.VARIABLES[key]) + "\n" )
		ffile.close()

	def generate_key(self):
		key = self.VARIABLES.get( "SECRET_KEY" )

		if not key:
			self.VARIABLES[ "SECRET_KEY" ] = SECRET()

	def db_create(self, dbse, serv, user, passw):
		self.VARIABLES[ "DBNAME" ] = dbse
		self.VARIABLES[ "DBSVER" ] = serv
		self.VARIABLES[ "DBUSER" ] = user
		self.VARIABLES[ "DBPASS" ] = passw

	def generate(self):
		ffile = open(self.SETTPATH, "w")

		ffile.write('import os\n\n')
		ffile.write('BASE_DIR="{}"\n'.format(self.BASEPATH))

		keys = list(self.VARIABLES.keys())

		for key in keys:
			if key in self.TOWRITTEN:
				ffile.write(
					"{key}={value}\n".format(
						key=key,
						repr(self.VARIABLES[key])
					)
				)

		ffile.close()

	def extend(self, addr, debug):
		if self.VARIABLES["DBNAME"] and self.VARIABLES["DBSVER"] and self.VARIABLES["DBUSER"] and self.VARIABLES["DBPASS"]:
			self.VARIABLES["DATABASES"] = self.returnee.r_database(
					self.VARIABLES["DBNAME"],
					self.VARIABLES["DBSVER"],
					self.VARIABLES["DBUSER"],
					self.VARIABLES["DBPASS"]
				)

		if debug:
			del self.VARIABLES["LOGGING"]
			del self.VARIABLES["LOGGING_CONFIG"]
			self.VARIABLES["DEBUG"] = True
		else:
			self.VARIABLES["LOGGING"] = {}
			self.VARIABLES["LOGGING_CONFIG"] = None
			self.VARIABLES["DEBUG"] = False

		self.VARIABLES["STATICFILES_DIRS"] = self.returnee.r_static_dirs()
		self.VARIABLES["TEMPLATES"][0][ "DIRS" ] = self.returnee.r_templates()
		self.VARIABLES["ALLOWED_HOSTS"] = (
				([addr]) if addr else [] 
			)

