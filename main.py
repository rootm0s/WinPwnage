from winpwnage.core.prints import print_info
from winpwnage.core.scanner import scanner, function
from winpwnage.core.utils import *
import argparse
import sys

print("""
        _
  _ _ _|_|___ ___ _ _ _ ___ ___ ___ ___
 | | | | |   | . | | | |   | .'| . | -_|
 |_____|_|_|_|  _|_____|_|_|__,|_  |___|
             |_|               |___|
""")

print_info("UAC level: {}".format(information().uac_level()))
print_info("Build number: {}".format(information().build_number()))
print_info("Running elevated: {}".format(information().admin()))
print_info("Python version: {}.{}.{}\n".format(*sys.version_info))

def main():
	scan_cmds = ["uac", "persist", "elevate"]

	parser = argparse.ArgumentParser()
	parser.add_argument("-s", "--scan", nargs="+", required=False, help="Scan for either uac, persist or elevate method")
	parser.add_argument("-u", "--use", nargs="+", required=False, help="Use either uac, persist or elevate method")
	parser.add_argument("-i", "--id", nargs="+", required=False, help="Id of method")
	parser.add_argument("-p", "--payload", nargs="+", required=False, help="Full path to payload, can include params")
	parser.add_argument("-r", "--remove", action="store_true", required=False, help="Removes installed persistence")
	args = parser.parse_args()

	if args.scan:
		if not all([_ in scan_cmds for _ in args.scan]):
			parser.print_help()

		scanner(**{scan_cmds[_]: scan_cmds[_] in args.scan for _ in range(3)}).start()

	if args.use and args.id:
		if not all([_ in scan_cmds for _ in args.use]):
			parser.print_help()

		if scan_cmds[0] in args.use and args.payload:
			function(uac=True, persist=False, elevate=False).run(id=args.id[0], payload=args.payload)

		if scan_cmds[1] in args.use:		
			function(uac=False, persist=True, elevate=False).run(id=args.id[0], payload=args.payload,
			add=(False if args.remove else True))

		if scan_cmds[2] in args.use and args.payload:
			function(uac=False, persist=False, elevate=True).run(id=args.id[0], payload=args.payload)

if __name__ == "__main__":
	main()