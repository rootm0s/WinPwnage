from distutils.core import setup
import py2exe
import sys

arg = [sys.argv[1]]

sys.argv.pop()
sys.argv.append('py2exe')
sys.argv.append('-q')

opts = {'py2exe':{'compressed': 2,'optimize': 2,'bundle_files': 1,}}

try:
	setup(console=arg,options=opts,zipfile=None)
except Exception as error:
	print error