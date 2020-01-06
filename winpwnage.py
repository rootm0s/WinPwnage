from __future__ import print_function
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
	scan_cmds = ["uac",
			"persist",
			"elevate",
			"execute"]

	parser = argparse.ArgumentParser()
	parser.add_argument("-s", "--scan", nargs="+", required=False)
	parser.add_argument("-u", "--use", nargs="+", required=False)
	parser.add_argument("-i", "--id", nargs="+", required=False)
	parser.add_argument("-p", "--payload", nargs="+", required=False)
	parser.add_argument("-r", "--remove", action="store_true", required=False)

	args = parser.parse_args()

	if args.scan:
		if not all([_ in scan_cmds for _ in args.scan]):
			parser.print_help()
		scanner(**{scan_cmds[_]: scan_cmds[_] in args.scan for _ in range(4)}).start()

	if args.use and args.id:
		if not all([_ in scan_cmds for _ in args.scan]):
			parser.print_help()

		if scan_cmds[0] in args.use and args.payload:
			function(uac=True, persist=False, elevate=False,
				execute=False).run(id=args.id[0], payload=args.payload[0])

		if scan_cmds[1] in args.use:		
			function(uac=False, persist=True, elevate=False,
					execute=False).run(id=args.id[0], payload=args.payload[0], add=(False if args.remove else True))

		if scan_cmds[2] in args.use and args.payload:
			function(uac=False, persist=False, elevate=True,
				execute=False).run(id=args.id[0], payload=args.payload[0])

		if scan_cmds[3] in args.use and args.payload:
			function(uac=False, persist=False, elevate=False,
				execute=True).run(id=args.id[0], payload=args.payload[0])
	

if __name__ == '__main__':
	main()
