import sys
from winpwnage.core.prints import print_info
from winpwnage.core.scanner import scanner, function
from winpwnage.core.utils import information

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
	#
	# Scanner
	#
	if sys.argv[1].lower() == "-scan" and sys.argv[2].lower() == "-uac":
		scanner(uac=True, persist=False, elevate=False, execute=False).start()
	elif sys.argv[1].lower() == "-scan" and sys.argv[2].lower() == "-persist":
		scanner(uac=False, persist=True, elevate=False, execute=False).start()
	elif sys.argv[1].lower() == "-scan" and sys.argv[2].lower() == "-elevate":
		scanner(uac=False, persist=False, elevate=True, execute=False).start()
	elif sys.argv[1].lower() == "-scan" and sys.argv[2].lower() == "-execute":
		scanner(uac=False, persist=False, elevate=False, execute=True).start()

	#
	# UAC bypass
	#
	elif sys.argv[1].lower() == "-use" and sys.argv[2].lower() == "-uac":
		function(uac=True, persist=False, elevate=False,
				execute=False).run(id=sys.argv[3], payload=sys.argv[4])		

	#
	# Persistence
	#
	elif sys.argv[1].lower() == "-use" and sys.argv[2].lower() == "-persist" and sys.argv[3].lower() == "-add":
		function(uac=False, persist=True, elevate=False,
				execute=False).run(id=sys.argv[4], payload=sys.argv[5], add=True)

	elif sys.argv[1].lower() == "-use" and sys.argv[2].lower() == "-persist" and sys.argv[3].lower() == "-remove":
		function(uac=False, persist=True, elevate=False,
				execute=False).run(id=sys.argv[4], payload=sys.argv[5], add=False)

	#
	# Elevate
	#
	elif sys.argv[1].lower() == "-use" and sys.argv[2].lower() == "-elevate":
		function(uac=False, persist=False, elevate=True,
				execute=False).run(id=sys.argv[3], payload=sys.argv[4])		

	#
	# Execute
	#
	elif sys.argv[1].lower() == "-use" and sys.argv[2].lower() == "-execute":
		function(uac=False, persist=False, elevate=False,
				execute=True).run(id=sys.argv[3], payload=sys.argv[4])

if __name__ == "__main__":
	main()