from distutils.core import setup
import py2exe
import sys

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
		"bundle_files": 1,
	}
}

setup(console=[args], options=opts, zipfile=None)