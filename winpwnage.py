import sys
from winpwnage.core.prints import print_info
from winpwnage.core.scanner import scanner, function
from winpwnage.core.utils import information

banner = """
        _                               
  _ _ _|_|___ ___ _ _ _ ___ ___ ___ ___ 
 | | | | |   | . | | | |   | .'| . | -_|
 |_____|_|_|_|  _|_____|_|_|__,|_  |___|
             |_|               |___|
"""

print(banner)

print_info("UAC level: {}".format(information().uac_level()))
print_info("Build number: {}".format(information().build_number()))
print_info("Running elevated: {}\n".format(information().admin()))

def main():
	try:
		if sys.argv[1].lower() == "-scan" and sys.argv[2].lower() == "-all":
			scanner(uac=True, persist=True).start()
		elif sys.argv[1].lower() == "-scan" and sys.argv[2].lower() == "-uac":
			scanner(uac=True, persist=False).start()
		elif sys.argv[1].lower() == "-scan" and sys.argv[2].lower() == "-persist":
			scanner(uac=False, persist=True).start()
			
		elif sys.argv[1].lower() == "-use" and sys.argv[2].lower() == "-uac":
			function(uac=True, persist=False).run(id=sys.argv[3], payload=sys.argv[4])
		elif sys.argv[1].lower() == "-use" and sys.argv[2].lower() == "-persist" and sys.argv[3].lower() == "-add":
			function(uac=False, persist=True).run(id=sys.argv[4], payload=sys.argv[5], name=sys.argv[6], add=True)
		elif sys.argv[1].lower() == "-use" and sys.argv[2].lower() == "-persist" and sys.argv[3].lower() == "-remove":
			function(uac=False, persist=True).run(id=sys.argv[4], payload=sys.argv[5], name=sys.argv[6], add=False)
	except Exception as error:
		pass

if __name__ == "__main__":
	main()
