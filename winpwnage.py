from __future__ import print_function
from winpwnage.core.prints import print_info
from winpwnage.core.scanner import scanner, function
from winpwnage.core.utils import *
import argparse
import sys

__version__ = "1.0"

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
	scan_cmds = ["uac",
		        "persist",
			"elevate",
			"execute"]

	parser = argparse.ArgumentParser()
	parser.add_argument("-s", "--scan", nargs="+", required=False)
	parser.add_argument("-u", "--use", nargs="+", required=False)
	parser.add_argument("-i", "--id", nargs="+", required=False)
	parser.add_argument("-p", "--payload", nargs="+", required=False)
	parser.add_argument("-a", "--add", action="store_true", required=False)
	parser.add_argument("-r", "--remove", action="store_true", required=False)

	args = parser.parse_args()

	if args.scan:
		if scan_cmds[0] in args.scan:
			scanner(uac=True, persist=False, elevate=False, execute=False).start()
		elif scan_cmds[1] in args.scan:
			scanner(uac=False, persist=True, elevate=False, execute=False).start()
		elif scan_cmds[2] in args.scan:
			scanner(uac=False, persist=False, elevate=True, execute=False).start()
		elif scan_cmds[3] in args.scan:
			scanner(uac=False, persist=False, elevate=False, execute=True).start()
		else:
			parser.print_help()

	if args.use:
		if scan_cmds[0] in args.use:
			if args.id:
				if args.payload:
					function(uac=True, persist=False, elevate=False,
						execute=False).run(id=args.id[0], payload=args.payload[0])
		elif scan_cmds[1] in args.use:		
			if args.add:
				function(uac=False, persist=True, elevate=False,
						execute=False).run(id=args.id[0], payload=args.payload[0], add=True)							
			elif args.remove:
				function(uac=False, persist=True, elevate=False,
						execute=False).run(id=args.id[0], payload=args.payload[0], add=False)
		elif scan_cmds[2] in args.use:
			if args.id:
				if args.payload:
					function(uac=False, persist=False, elevate=True,
						execute=False).run(id=args.id[0], payload=args.payload[0])
		elif scan_cmds[3] in args.use:
			if args.id:
				if args.payload:
					function(uac=False, persist=False, elevate=False,
						execute=True).run(id=args.id[0], payload=args.payload[0])
		else:
			parser.print_help()

if __name__ == '__main__':
	main()
