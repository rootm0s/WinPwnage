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

# https://docs.python.org/3/library/platform.html#platform.architecture
is_64bits = sys.maxsize > 2**32
print("Building for Win{}...".format(64 if is_64bits else 32))

opts = {
	"py2exe": {
		"compressed": 2,
		"optimize": 2,
		"bundle_files": 3 if is_64bits else 1,
	}
}

setup(console=[args], options=opts, zipfile=None)
