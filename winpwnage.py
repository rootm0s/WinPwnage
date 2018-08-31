import sys
from core.prints import *
from core.scanner import *
from core.utils import *

print """
        _                               
  _ _ _|_|___ ___ _ _ _ ___ ___ ___ ___ 
 | | | | |   | . | | | |   | .'| . | -_|
 |_____|_|_|_|  _|_____|_|_|__,|_  |___|
             |_|               |___|
 """

print_info("UAC level: {}".format(information().uac_level()))
print_info("Build number: {}".format(information().build_number()))
print_info("Running elevated: {}\n".format(information().admin()))

def main():
	try:
		if (sys.argv[1].lower() == "-scan"):
			scanner().start()
		elif (sys.argv[1].lower() == "-use"):
			function().run(sys.argv[2],sys.argv[3])
		else:
			pass
	except Exception as error:
		pass

if __name__ == "__main__":
	main()