from distutils.core import setup
import sys

import py2exe  # noqa: F401

try:
	args = sys.argv[1]
except Exception as error:
	sys.exit()

sys.argv.pop()
sys.argv.append("py2exe")
sys.argv.append("-q")

opts = {
	"py2exe": {
		"compressed": 2,
		"optimize": 2,
		# "bundle_files": 1,  # Win32
		"bundle_files": 3,    # Win64
	}
}

setup(console=[args], options=opts, zipfile=None)
