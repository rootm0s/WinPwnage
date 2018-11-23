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
		if sys.argv[1].lower() == "-scan":
				scanner().start()
		elif sys.argv[1].lower() == "-uac":
				function(uac=True, persist=False).run(id=sys.argv[2], payload=sys.argv[3])
		elif sys.argv[1].lower() == "-add_persist":
				function(uac=False, persist=True).run(id=sys.argv[2], payload=sys.argv[3], name=sys.argv[4], add=True)
		elif sys.argv[1].lower() == "-remove_persist":
				function(uac=False, persist=True).run(id=sys.argv[2], payload=sys.argv[3], name=sys.argv[4], add=False)
	except Exception as error:
		pass

if __name__ == "__main__":
	main()
