import os
import sys

__logo__ = """%s
  ______            _____              ______
 /_/_/__/      |    | \\  \       |     | |  /
"""

class PULL:

	WHITE = '\033[0m'
	PURPLE = '\033[95m'
	CYAN = '\033[96m'
	DARKCYAN = '\033[36m'
	BLUE = '\033[94m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	END = '\033[0m'
	LINEUP = '\033[F'

	MIXTURE = {
		'WHITE': '\033[0m',
		'PURPLE': '\033[95m',
		'CYAN': '\033[96m',
		'DARKCYAN': '\033[36m',
		'BLUE': '\033[94m',
		'GREEN': '\033[92m',
		'YELLOW': '\033[93m',
		'RED': '\033[91m',
		'BOLD': '\033[1m',
		'UNDERLINE': '\033[4m',
		'END': '\033[0m',
		'LINEUP': '\033[F'
	}

	VACANT = {
		'WHITE': '',
		'PURPLE': '',
		'CYAN': '',
		'DARKCYAN': '',
		'BLUE': '',
		'GREEN': '',
		'YELLOW': '',
		'RED': '',
		'BOLD': '',
		'UNDERLINE': '',
		'END': '',
		'LINEUP': ''
	}

	def __init__(self):
		if not self.support_colors:
			self.win_colors()

	def support_colors(self):
		plat = sys.platform
		supported_platform = plat != 'Pocket PC' and (plat != 'win32' or \
														'ANSICON' in os.environ)
		is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
		if not supported_platform or not is_a_tty:
			return False
		return True

	def win_colors(self):
		self.WHITE = ''
		self.PURPLE = ''
		self.CYAN = ''
		self.DARKCYAN = ''
		self.BLUE = ''
		self.GREEN = ''
		self.YELLOW = ''
		self.RED = ''
		self.BOLD = ''
		self.UNDERLINE = ''
		self.END = ''
		self.MIXTURE = {
			'WHITE': '',
			'PURPLE': '',
			'CYAN': '',
			'DARKCYAN': '',
			'BLUE': '',
			'GREEN': '',
			'YELLOW': '',
			'RED': '',
			'BOLD': '',
			'UNDERLINE': '',
			'END': '',
			'LINEUP': ''
		}

		for (key, val) in self.MIXTURE.items():
			self.MIXTURE[ key ] = ''

	def gthen(self, tshow, cc='', *colors):
		for color in colors:
			cc += color
		print( "%s[>]%s %s" % ( cc, self.END, tshow ) )

	def lthen(self, tshow, cc='', *colors):
		for color in colors:
			cc += color
		print( "%s[<]%s %s" % ( cc, self.END, tshow ) )

	def uprun(self, tshow, cc='', *colors):
		for color in colors:
			cc += color
		print( "%s[^]%s %s" % ( cc, self.END, tshow ) )

	def info(self, tshow, cc='', *colors):
		for color in colors:
			cc += color
		print( "%s[*]%s %s" % ( cc, self.END, tshow ) )

	def ask(self, tshow, cc='', *colors):
		for color in colors:
			cc += color
		return input( "%s[?]%s %s" % (cc, self.END, tshow) )

	def halt(self, tshow, cc='', exit=1, *colors):
		for color in colors:
			cc += color
		print( "%s[~]%s %s" % ( cc, self.END, tshow ) )
		if exit:
			sys.exit(-1)