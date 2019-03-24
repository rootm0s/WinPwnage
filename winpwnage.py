from __future__ import print_function
import sys
from winpwnage.core.prints import print_info
from winpwnage.core.scanner import function, function_groups, scanner
from winpwnage.core.utils import information

print("""
        _
  _ _ _|_|___ ___ _ _ _ ___ ___ ___ ___
 | | | | |   | . | | | |   | .'| . | -_|
 |_____|_|_|_|  _|_____|_|_|__,|_  |___|
             |_|               |___|
""")

print_info("Python {}.{}.{}".format(*sys.version_info))
print_info("UAC level: {}".format(information().uac_level()))
print_info("Build number: {}".format(information().build_number()))
print_info("Running elevated: {}\n".format(information().admin()))

    
def main():
    try:  # Each of the next 4 lines can raise IndexError
        verb = sys.argv[1].lstrip("-").lower()
        verb in ("scan", "use")
        function_group = sys.argv[2].lstrip("-").lower()
        function_group in function_groups

        if verb == "scan":
            scanner(function_group).start()
        # verb == "use"
        elif function_group == "persist":  # use Persistence
            # False if "-remove", True if "-add", raise ValueError on all other values
            add = bool(("-remove", "-add").index(sys.argv[3].lower()))
            function(function_group).run(id=sys.argv[4], payload=sys.argv[5], add=add)
        else:  # use User Account Control or Elevate or Execute
            function(function_group).run(id=sys.argv[3], payload=sys.argv[4])
    except (IndexError, ValueError) as e:
        print(str(e))
        print("winpwnage [-scan, -use] [-uac, -persist, -elevate, -execute] ...")
        sys.exit(1)


if __name__ == "__main__":
    main()
